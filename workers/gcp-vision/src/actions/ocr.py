import os
from typing import Optional
from google.cloud import vision

# uses credential file from GOOGLE_APPLICATION_CREDENTIALS
client = vision.ImageAnnotatorClient()

# Configure "Hints" to help the AI (reusable across all requests)
context = vision.ImageContext(
    language_hints=["en"],  # Force/Prioritize English (helps with accents)
    text_detection_params=vision.TextDetectionParams(
        #enable_text_detection_confidence_score=True # Ask for % confidence scores
    )
)

def detect_text_image_data(content: bytes) -> Optional[vision.TextAnnotation]:
    """Detects text in a local image file."""
    image = vision.Image(content=content)

    # Call the API (DOCUMENT_TEXT_DETECTION is better for dense text like screenshots)
    response = client.document_text_detection(image=image, image_context=context)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    # Print the results
    if os.environ.get('ENABLE_DEV', 'false').lower() == 'true':
        if response.full_text_annotation:
            print(f"Full Text found:\n{response.full_text_annotation.text}\n")
    
    
    # return text
    return response.full_text_annotation
