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

def test_vision_api() -> bool:
    """
    Test Google Cloud Vision API connectivity and credentials by OCRing a test image.
    Returns True if successful, raises exception if failed.
    """
    # Go up one directory from actions/ to src/, then find test_ocr.png
    test_image_path = os.path.join(os.path.dirname(__file__), '..', 'test_ocr.png')

    try:
        with open(test_image_path, 'rb') as f:
            test_image_content = f.read()
    except FileNotFoundError:
        raise Exception(f'Test image not found at {test_image_path}')

    # Use the actual OCR function to test
    result = detect_text_image_data(test_image_content)

    if not result:
        raise Exception('Vision API test returned no text annotation')

    # Verify the expected text
    ocr_text = result.text.strip()
    if ocr_text != 'ASHIRT':
        raise Exception(f'Vision API test expected "ASHIRT" but got "{ocr_text}"')

    return True


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
