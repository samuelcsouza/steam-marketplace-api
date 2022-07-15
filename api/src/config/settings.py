from pydantic import BaseSettings


class Settings(BaseSettings):
    STEAM_MARKETPLACE_URL: str = "https://steamcommunity.com/market/listings"


def get_settings() -> Settings:
    return Settings()
