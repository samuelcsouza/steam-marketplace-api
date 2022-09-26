import pytest
import pandas as pd
from mock.mock import Mock
from src.repositories.steam import SteamRepository
from src.services.steam import SteamService


class TestSteam:
    @classmethod
    def setup_class(cls):
        cls.steam_marketplace_url = "test-url.com"
        cls.steam_repository = Mock()
        cls.steam_service = SteamService(
            cls.steam_repository
        )

    @pytest.mark.asyncio
    async def test_get_item_marketplace_values__get_item__expected_success(self):
        appid = 730
        item = "AK 47 | Safari Mesh (Factory New)"

        _return_value = pd.DataFrame(
            {
                "date": ["2016-07-10",
                         "2016-07-11",
                         "2016-07-12",
                         "2016-07-13",
                         "2016-07-14",
                         "2016-07-15",
                         "2016-07-16",
                         "2016-07-17",
                         "2016-07-18",
                         "2016-07-19"],
                "value": [10,
                          20,
                          30,
                          40,
                          50,
                          60,
                          70,
                          80,
                          90,
                          100]
            }
        )

        self.steam_repository.get_observations = Mock()
        self.steam_repository.get_observations.return_value = _return_value

        result = self.steam_service.get_item_marketplace_values(
            appid=appid,
            item=item,
            fill=True
        )

        expected_data = [
            {
                "date": "2016-07-10",
                "value": 10
            },
            {
                "date": "2016-07-11",
                "value": 20
            },
            {
                "date": "2016-07-12",
                "value": 30
            },
            {
                "date": "2016-07-13",
                "value": 40
            },
            {
                "date": "2016-07-14",
                "value": 50
            },
            {
                "date": "2016-07-15",
                "value": 60
            },
            {
                "date": "2016-07-16",
                "value": 70
            },
            {
                "date": "2016-07-17",
                "value": 80
            },
            {
                "date": "2016-07-18",
                "value": 90
            },
            {
                "date": "2016-07-19",
                "value": 100
            }
        ]

        assert result[0]["date"] == expected_data[0]["date"]
        assert result[0]["value"] == expected_data[0]["value"]

        assert result[-1]["date"] == expected_data[-1]["date"]
        assert result[-1]["value"] == expected_data[-1]["value"]
