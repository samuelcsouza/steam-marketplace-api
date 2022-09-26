import pandas as pd
from fastapi.exceptions import HTTPException
from src.utils.api_errors import ErrorResourceNotFound
from src.repositories.steam import SteamRepository
from mock.mock import Mock, patch
from unittest import TestCase


class TestSteamRepository(TestCase):

    def setup_method(self, test_method):
        self.steam_repository = SteamRepository(
            steam_url_marketplace="url-test.com"
        )

    @patch("requests.get")
    def test_get_observations__get_observations_with_fill__expected_observations(
        self, requests_mock: Mock
    ):
        # Fixtures
        appid = 730
        item = "Awesome Item"
        fill = True

        _html_page = 'var line1=[\
            ["Jul 01 2016 01: +0",10.0,"1"],\
            ["Jul 05 2016 01: +0",50.0,"1"],\
            ["Jul 10 2016 01: +0",100.0,"1"]\
        ];'

        requests_mock.return_value.text = _html_page

        _return_value = pd.DataFrame(
            {
                "date": ["2016-07-01",
                         "2016-07-02",
                         "2016-07-03",
                         "2016-07-04",
                         "2016-07-05",
                         "2016-07-06",
                         "2016-07-07",
                         "2016-07-08",
                         "2016-07-09",
                         "2016-07-10"],
                "value": [10,
                          10,
                          10,
                          10,
                          50,
                          50,
                          50,
                          50,
                          50,
                          100]
            }
        )

        # Exercise
        result = self.steam_repository.get_observations(
            appid=appid, item=item, fill=fill
        )

        # Asserts
        assert _return_value["date"].all() == result["date"].all()
        assert _return_value["value"].all() == result["value"].all()

    @patch("requests.get")
    def test_get_observations__get_observations_without_fill__expected_observations(
        self, requests_mock: Mock
    ):
        # Fixtures
        appid = 730
        item = "Awesome Item"
        fill = False

        _html_page = 'var line1=[\
            ["Jul 01 2016 01: +0",10.0,"1"],\
            ["Jul 05 2016 01: +0",50.0,"1"],\
            ["Jul 10 2016 01: +0",100.0,"1"]\
        ];'

        requests_mock.return_value.text = _html_page

        _return_value = pd.DataFrame(
            {
                "date": ["2016-07-01",
                         "2016-07-05",
                         "2016-07-10"],
                "value": [10,
                          50,
                          100]
            }
        )

        # Exercise
        result = self.steam_repository.get_observations(
            appid=appid, item=item, fill=fill
        )

        # Asserts
        assert _return_value["date"].all() == result["date"].all()
        assert _return_value["value"].all() == result["value"].all()

    @patch("requests.get")
    def test_get_observations__invalid_appid__expected_error(
        self, requests_mock: Mock
    ):
        # Fixtures
        appid = -1
        item = "Awesome Item"
        fill = False

        _html_page = ""

        requests_mock.return_value.text = _html_page

        # Exercise
        with self.assertRaises(HTTPException) as context:
            self.steam_repository.get_observations(
                appid=appid, item=item, fill=fill
            )

        error = context.exception

        # Asserts
        assert ErrorResourceNotFound.status_code == error.status_code
        assert ErrorResourceNotFound.error == error.detail

    @patch("requests.get")
    def test_get_observations__invalid_item_name__expected_error(
        self, requests_mock: Mock
    ):
        appid = 730
        item = "Invalid!"
        fill = False

        _html_page = ""

        requests_mock.return_value.text = _html_page

        # Exercise
        with self.assertRaises(HTTPException) as context:
            self.steam_repository.get_observations(
                appid=appid, item=item, fill=fill
            )

        error = context.exception

        # Asserts
        assert ErrorResourceNotFound.status_code == error.status_code
        assert ErrorResourceNotFound.error == error.detail
