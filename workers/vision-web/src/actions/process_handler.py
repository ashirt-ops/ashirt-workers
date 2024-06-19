from request_types import EvidenceCreatedBody
from services import AShirtRequestsService
from constants import SupportedContentType
from .types import ProcessResultDTO
import onnxruntime_genai as og
import uuid
import os
import io

model = og.Model('model/cpu-int4-rtn-block-32-acc-level-4/')
processor = model.create_multimodal_processor()
tokenizer_stream = processor.create_stream()

def handle_evidence_created(body: EvidenceCreatedBody) -> ProcessResultDTO:
    """
    handle_process is called when a web request comess in, is validated, and indicates that work
    needs to be done on a piece of evidence
    """
    accepted_types = [
        SupportedContentType.IMAGE
    ]

    if body.content_type in accepted_types:
        ashirt_svc = AShirtRequestsService(
            os.environ.get('ASHIRT_BACKEND_URL', ''),
            os.environ.get('ASHIRT_ACCESS_KEY', ''),
            os.environ.get('ASHIRT_SECRET_KEY', '')
        )
        # Gather content
        evidence_content = ashirt_svc.get_evidence_content(
            body.operation_slug, body.evidence_uuid, 'media'
            )
        if type(evidence_content) == str:
            print("got a string response")
        elif type(evidence_content) != bytes:
            return

        temp_image_path = f"/tmp/{uuid.uuid4()}.png"  # Generate a unique name for the image file in /tmp directory
        with open(temp_image_path, "wb") as f:
            f.write(io.BytesIO(evidence_content).getbuffer())
        img = og.Images.open(temp_image_path)

        default_questions = [
            "What times are shown in the image?",
            "Which applications are open in the image?",
            "Which operating system is being used in the image?",
            "What does the image say?"
        ]
        questions = os.environ.get('VISION_QUESTIONS', ','.join(default_questions))
        questions = questions.split(',') # Convert question(s) to a list

        resp = []
        for q in questions:
            resp.append(do_ai(question=q,image=img)) # Run inference for each question
        chunks = [f'Q:{x[0]}\nA:{x[1]}\n' for x in zip(questions,resp)]
        os.remove(temp_image_path)  # Delete the image file after using it

        return {
            'action': 'processed',
            'content': '\n'.join(chunks)
        }
    else:
        return {
            'action': 'rejected'
        }

def do_ai(question, image=None):
    generated_text = ""
    prompt = "<|user|>\n"
    if not image:
        print("No image provided")
    else:
        print("Loading image...")
        prompt += "<|image_1|>\n"

    prompt += f"{question}<|end|>\n<|assistant|>\n"
    print("Processing image and prompt...")
    inputs = processor(prompt, images=image)

    print("Generating response...")
    params = og.GeneratorParams(model)
    params.set_inputs(inputs)
    params.set_search_options(max_length=3072)

    generator = og.Generator(model, params)

    while not generator.is_done():
        generator.compute_logits()
        generator.generate_next_token()

        new_token = generator.get_next_tokens()[0]
        decoded_text = tokenizer_stream.decode(new_token)
        generated_text += decoded_text
        print(decoded_text, end='', flush=True)
    for _ in range(3):
        print()
    generated_text = generated_text.replace('</s>','')
    # Delete the generator to free the captured graph before creating another one
    del generator
    return generated_text