from pydantic import BaseSettings


class Settings(BaseSettings):
    STEAM_MARKETPLACE_CSGO_URL: str = "https://steamcommunity.com/market/listings/730/"
    STEAM_MARKETPLACE_URL: str = "https://steamcommunity.com/market/listings/"
    STEAM_CSGO_GAME_ID: str = "730"


def get_settings() -> Settings:
    return Settings()
