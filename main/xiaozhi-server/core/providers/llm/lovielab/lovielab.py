import requests
from config.logger import setup_logging
from core.providers.llm.base import LLMProviderBase
from core.utils.lovielab_auth import LovieLabAuth

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.model_name = config.get("model_name", "walle")

    def response(self, session_id, dialogue, **kwargs):
        token = LovieLabAuth.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": dialogue,
            "stream": False
        }

        resp = requests.post(
            f"{LovieLabAuth.get_base_url()}/chat/completions",
            json=payload,
            headers=headers
        )
        resp.raise_for_status()
        result = resp.json()

        if "choices" in result and len(result["choices"]) > 0:
            response_text = result["choices"][0].get("message", {}).get("content", "")
        else:
            response_text = str(result)

        if response_text:
            yield response_text
