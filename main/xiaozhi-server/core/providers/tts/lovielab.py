import requests
from core.providers.tts.base import TTSProviderBase
from core.utils.lovielab_auth import LovieLabAuth
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        self.voice = config.get("voice", "3fTZRfeclSMoZMOrSplv")
        self.audio_file_type = "mp3"
        self.output_file = config.get("output_dir", "tmp/")

    def generate_filename(self, extension=".mp3"):
        return super().generate_filename(extension)

    async def text_to_speak(self, text, output_file):
        token = LovieLabAuth.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": text,
            "voice": self.voice
        }

        response = requests.post(
            f"{LovieLabAuth.get_base_url()}/audio/speech",
            json=payload,
            headers=headers
        )
        if response.status_code == 200:
            if output_file:
                with open(output_file, "wb") as audio_file:
                    audio_file.write(response.content)
            else:
                return response.content
        else:
            raise Exception(
                f"Lovielab TTS请求失败: {response.status_code} - {response.text}"
            )
