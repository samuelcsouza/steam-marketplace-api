from typing import Callable, Type, Any
from fastapi import Depends

from src.config.settings import get_settings
from src.services.steam import SteamService
from src.repositories.steam import SteamRepository


def get_repository(repository_type: Type[Any]) -> Callable:
    if repository_type == SteamRepository:
        def __get_repo(
            settings=Depends(get_settings)
        ):
            return repository_type(settings.STEAM_MARKETPLACE_URL)

        return __get_repo


def get_service(serivce_type: Type[Any]) -> Callable:
    if serivce_type == SteamService:
        def __get_service(
            steam_repository=Depends(get_repository(SteamRepository))
        ):
            return serivce_type(steam_repository)

        return __get_service
