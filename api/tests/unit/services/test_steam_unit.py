import pytest
from mock.mock import Mock
from src.services.external.steam import SteamService


class TestSteam:
    @classmethod
    def setup_class(cls):
        cls.steam_marketplace_url = "test-url.com"
        cls.steam_service = SteamService(
            cls.steam_marketplace_url
        )

    @pytest.mark.asyncio
    async def test_get_item_marketplace_values__get_item__expected_success(self):
        appid = 730
        item = "AK 47 | Safari Mesh (Factory New)"

        item_values = [
            '"Aug 17 2022 01: +0",4.09,"1"',  '"Aug 17 2022 02: +0",4.08,"2"',  '"Aug 17 2022 03: +0",4.231,"1"',
            '"Aug 17 2022 04: +0",4.28,"2"',  '"Aug 17 2022 05: +0",4.07,"1"',  '"Aug 17 2022 08: +0",4.22,"1"',
            '"Aug 17 2022 10: +0",4.472,"1"', '"Aug 17 2022 11: +0",4.415,"1"', '"Aug 17 2022 12: +0",25.38,"1"',
            '"Aug 17 2022 13: +0",4.084,"1"', '"Aug 17 2022 14: +0",4.085,"2"', '"Aug 17 2022 15: +0",4.769,"2"',
            '"Aug 17 2022 16: +0",4.389,"1"', '"Aug 17 2022 17: +0",4.4,"1"',   '"Aug 17 2022 18: +0",4.387,"1"',
            '"Aug 17 2022 19: +0",4.46,"2"',  '"Aug 17 2022 20: +0",4.346,"2"', '"Aug 17 2022 21: +0",4.11,"1"'
        ]

        all_values = [4.09, 4.28, 4.472, 4.084, 4.389, 4.46,
                      4.08, 4.07, 4.415, 4.085, 4.4, 4.346,
                      4.231, 4.22, 25.38, 4.769, 4.387, 4.11]

        mean_values = round(sum(all_values) / len(all_values), ndigits=2)

        self.steam_service._get_steam_historical_values = Mock()
        self.steam_service._get_steam_historical_values.return_value = item_values

        result = self.steam_service.get_item_marketplace_values(
            appid=appid,
            item=item,
            fill=True
        )

        expected_data = [
            {
                "date": "2022-08-17",
                "value": mean_values
            }
        ]

        assert result[0]["date"] == expected_data[0]["date"]
        assert result[0]["value"] == expected_data[0]["value"]
