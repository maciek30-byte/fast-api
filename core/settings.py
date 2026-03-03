from pydantic import BaseModel


class Settings(BaseModel):
    SECRET_KEY: str = "1582ff93129c91ba6ab67ab0408c385a9f4a8a91307adcf5499c636b4a40f525"
    ALGORITHM: str = "HS256"

settings = Settings()