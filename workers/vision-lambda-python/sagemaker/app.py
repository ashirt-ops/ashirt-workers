from flask import Flask
import flask
#import spacy
import os
import json
import logging

import io
from typing import Tuple
import onnxruntime_genai as og
import uuid

model = og.Model('/opt/program/model/cpu-int4-rtn-block-32-acc-level-4/')
processor = model.create_multimodal_processor()
tokenizer_stream = processor.create_stream()

# The flask app for serving predictions
app = Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    health = model is not None
    health = True
    status = 200 if health else 404
    return flask.Response(response= '\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    
    #Process input
    input_json = flask.request.get_json()
    resp = input_json['input']
    
    #AI
    results = do_ai(resp)

    # Transform predictions to JSON
    result = {
        'output': resp
        }

    resultjson = json.dumps(result)
    return flask.Response(response=resultjson, status=200, mimetype='application/json')

def do_ai(question, image=None):

    # Initialize the string for the generated text
    generated_text = ""

    # Construct the prompt string
    prompt = "<|user|>\n"

    # If an image is not provided, notify the console
    if not image:
        print("No image provided")
    else:
        print("Loading image...")
        # If an image is provided, include image prompt
        prompt += "<|image_1|>\n"

    # Append the question to the prompt
    prompt += f"{question}<|end|>\n<|assistant|>\n"
    print("Processing image and prompt...")
    # Create input data for the model
    inputs = processor(prompt, images=image)

    print("Generating response...")

    # Set up the model parameters
    params = og.GeneratorParams(model)
    params.set_inputs(inputs)
    # Limit the maximum length of the generated response
    params.set_search_options(max_length=3072)

    # Generate a response using the generator object
    generator = og.Generator(model, params)

    # Generate the response token by token
    while not generator.is_done():
        generator.compute_logits()
        generator.generate_next_token()

        new_token = generator.get_next_tokens()[0]
        decoded_text = tokenizer_stream.decode(new_token)
       # Add each new token to the response string
        generated_text += decoded_text
       # Print each token to the console as it is generated
        print(decoded_text, end='', flush=True)

    # Print some extra newlines for readability
    for _ in range(3):
        print()

    # Strip any leading spaces from the response
    generated_text = generated_text.replace(' ', '')

    # Delete the generator object to free resources
    del generator

   # Return the complete response string
    return generated_text