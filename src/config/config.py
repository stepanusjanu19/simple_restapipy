from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    mongo_uri: str
    token_secret: str
    xcustom: str
    browser_api_calls_xhr_only: bool
    debugging: bool
    passthrough_errors: bool
    use_debugger: bool
    use_reloader: bool

    class Config:
        env_file = ".env"


setting = Setting()
