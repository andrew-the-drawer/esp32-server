import asyncio
import requests
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class LovieLabAuth:
    """
    Singleton-style class for managing LovieLabAuth authentication.

    Call LovieLabAuth.initialize(config) once at app startup, then
    start the background rotation with:
        asyncio.create_task(LovieLabAuth.start_token_rotation())

    Providers retrieve the current token via LovieLabAuth.get_access_token().
    """

    _access_token: str | None = None
    _email: str | None = None
    _password: str | None = None
    _base_url: str = "https://app.lovielab.com/api/v1"
    _initialized: bool = False

    @classmethod
    def initialize(cls, config: dict) -> None:
        """
        Read lovielab auth credentials from config and perform the initial
        authentication.  Config should contain a top-level ``lovielab`` key:

            lovielab:
              email: your@email.com
              password: your_password
              base_url: https://app.lovielab.com/api/v1   # optional
        """
        lovielab_cfg = config.get("provider", {})
        cls._email = lovielab_cfg.get("email")
        cls._password = lovielab_cfg.get("password")
        cls._base_url = lovielab_cfg.get("base_url", "https://app.lovielab.com/api/v1")

        if not cls._email or not cls._password:
            logger.bind(tag=TAG).warning(
                "Lovielab email/password not configured – skipping authentication"
            )
            return

        try:
            cls._authenticate()
            cls._initialized = True
        except Exception as e:
            logger.bind(tag=TAG).error(f"Lovielab initial authentication failed: {e}")

    @classmethod
    async def start_token_rotation(cls) -> None:
        """
        Async background task that re-authenticates every hour.
        Schedule with asyncio.create_task() after calling initialize().
        """
        if not cls._email or not cls._password:
            return

        while True:
            await asyncio.sleep(3600)  # rotate every hour
            try:
                cls._authenticate()
            except Exception as e:
                logger.bind(tag=TAG).error(f"Lovielab token rotation failed: {e}")

    @classmethod
    def _authenticate(cls) -> None:
        """Call /auths/signin and store the returned token."""
        url = f"{cls._base_url}/auths/signin"
        payload = {"email": cls._email, "password": cls._password}
        headers = {"Content-Type": "application/json"}

        logger.bind(tag=TAG).info("Authenticating to Lovielab…")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        token = response.json().get("token")
        if not token:
            raise ValueError("No token in Lovielab authentication response")

        cls._access_token = token
        logger.bind(tag=TAG).info("Lovielab authentication successful")

    @classmethod
    def get_access_token(cls) -> str | None:
        """Return the current access token, or None if not yet authenticated."""
        if cls._access_token is None:
            logger.bind(tag=TAG).warning(
                "Lovielab access token requested but not yet available"
            )
        return cls._access_token

    @classmethod
    def get_base_url(cls) -> str:
        """Return the configured base URL."""
        return cls._base_url
