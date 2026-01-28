from typing import Optional
import requests

from .ashirt_base_class import AShirtService
from . import (
    RequestConfig as RC,
)


class AShirtRequestsService(AShirtService):
    """
    AShirtRequestsService is a subclass of AShirtService that makes requests using the Requests
    library. This is a synchronous library, and so care needs to be taken when using this service.
    """
    def __init__(self, api_url: str, access_key: str, secret_key_b64: str):
        super().__init__(api_url, access_key, secret_key_b64)

    def _make_request(self, cfg: RC, headers: dict[str, str], body: Optional[bytes])->bytes:
        url = self._route_to(cfg.path)
        # Only use stream=True for raw content (large files)
        use_stream = cfg.return_type == 'raw'

        print(f"[DEBUG] Making request: {cfg.method} {url}", flush=True)
        print(f"[DEBUG] Headers: {headers}", flush=True)

        resp = requests.request(
            cfg.method, url, headers=headers, data=body, stream=use_stream)

        print(f"[DEBUG] Response: {resp.status_code} {resp.reason}", flush=True)
        print(f"[DEBUG] Response headers: {dict(resp.headers)}", flush=True)

        if cfg.return_type == 'json':
            text = resp.text
            print(f"[DEBUG] Response body: {text[:500] if text else '(empty)'}", flush=True)
            if not resp.ok or not text:
                print(f"[DEBUG] API Error or empty response!", flush=True)
            return resp.json()
        elif cfg.return_type == 'status':
            return resp.status_code
        elif cfg.return_type == 'text':
            return resp.text

        return resp.content

    def _route_to(self, path: str):
        return f'{self.api_url}{path}'
