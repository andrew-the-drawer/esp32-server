import time
import os
from config.logger import setup_logging
from typing import Optional, Tuple, List
from core.providers.asr.dto.dto import InterfaceType
from core.providers.asr.base import ASRProviderBase
from core.utils.lovielab_auth import LovieLabAuth

import requests

TAG = __name__
logger = setup_logging()

class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool):
        self.interface_type = InterfaceType.NON_STREAM
        self.language = config.get("language", "en")
        self.output_dir = config.get("output_dir")
        self.delete_audio_file = delete_audio_file

        os.makedirs(self.output_dir, exist_ok=True)

    def requires_file(self) -> bool:
        return True

    async def speech_to_text(self, opus_data: List[bytes], session_id: str, audio_format="opus", artifacts=None) -> Tuple[Optional[str], Optional[str]]:
        file_path = None
        try:
            if artifacts is None:
                return "", None
            file_path = artifacts.file_path

            logger.bind(tag=TAG).info(f"file path: {file_path}")
            token = LovieLabAuth.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }

            data = {
                "language": self.language
            }

            with open(file_path, "rb") as audio_file:
                files = {
                    "file": ("recording.wav", audio_file, "audio/wav")
                }

                start_time = time.time()
                response = requests.post(
                    f"{LovieLabAuth.get_base_url()}/audio/transcriptions",
                    files=files,
                    data=data,
                    headers=headers
                )
                logger.bind(tag=TAG).debug(
                    f"语音识别耗时: {time.time() - start_time:.3f}s | 结果: {response.text}"
                )

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict):
                    text = result.get("text", result.get("transcription", str(result)))
                else:
                    text = str(result)
                return text, file_path
            else:
                raise Exception(f"API请求失败: {response.status_code} - {response.text}")

        except Exception as e:
            logger.bind(tag=TAG).error(f"语音识别失败: {e}")
            return "", None
