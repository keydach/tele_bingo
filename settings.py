from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    api_id: SecretStr
    api_hash: SecretStr
    bot_token: SecretStr

    example_songs: str
    example_card: str
    example_back_card: str

    max_card_cnt: int
    source_dir: str

    class Config:
        env_file = 'local.env'


config = Settings()
