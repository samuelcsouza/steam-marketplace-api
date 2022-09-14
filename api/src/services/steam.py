from typing import Dict, List
from src.repositories.steam import SteamRepository


class SteamService():

    def __init__(self, steam_repository: SteamRepository) -> None:
        self._steam_repository = steam_repository

    def get_item_marketplace_values(self, appid: int, item: str, fill: bool = True) -> List[Dict]:
        item_data = self._steam_repository.get_observations(appid, item, fill)

        return item_data.to_dict("records")
