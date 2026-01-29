from request_types import EvidenceCreatedBody
from constants import SupportedContentType
from services import svc
from .types import ProcessResultDTO
from .ocr import detect_text_image_data

def handle_evidence_created(body: EvidenceCreatedBody) -> ProcessResultDTO:
    """
    handle_process is called when a web request comes in, is validated, and indicates that work
    needs to be done on a piece of evidence
    """
    accepted_types = [
        SupportedContentType.IMAGE,
        # SupportedContentType.CODEBLOCK,
        # SupportedContentType.EVENT,
        # SupportedContentType.HTTP_REQUEST_CYCLE,
        # SupportedContentType.TERMINAL_RECORDING,
        # SupportedContentType.NONE,
    ]

    if body.content_type in accepted_types:
        # get the raw image data
        image_data = svc().get_evidence_content(
            operation_slug=body.operation_slug,
            evidence_uuid=body.evidence_uuid,
            content_type='media'
        )
        
        # OCR the data
        try:
            full_text_annotation = detect_text_image_data(image_data)
            if not full_text_annotation:
                return {
                    'action': 'error',
                    'content': 'no data'
                }

            # return text
            return {
                'action': 'processed',
                'content': full_text_annotation.text,
            }
        except Exception as e:
            return {
                'action': 'error',
                'content': f'OCR failed: {str(e)}'
            }
    else:
        return {
            'action': 'rejected'
        }


