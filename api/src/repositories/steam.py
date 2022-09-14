import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from src.utils.api_errors import (
    ErrorInvalidParameters,
    ErrorResourceNotFound,
    raise_error_response
)


class SteamRepository():
    """
    This is a class for handle with Steam Marketplace data.

    Those methods goes to steam's endpoint and get a time serie from an requested item.
    """

    def __init__(self, steam_url_marketplace: str) -> None:
        """
        Constructor of SteamService class.

        You need to provide an URL to steam's marketplace including your Steam Application ID.

        All Steam Application IDs you can access here: https://developer.valvesoftware.com/wiki/Steam_Application_IDs

        Parameters:
            steam_url_marketplace: Base URL from Steam's marketplace

        Example:
            CS:GO only: https://steamcommunity.com/market/listings/730/
        """
        self._steam_url_marketplace = steam_url_marketplace

    def _get_url_item(self, appid: int, item: str) -> str:
        """
        Get URL for a Steam item.

        Parameters:
            appid (int): App game id on steam.
            item (str): Full name of any item on steam community market.

        Example:
            appid = 730
            item = ★ StatTrak™ Flip Knife | Freehand (Factory New)

        Notes:
        - You can find all Ids here: https://developer.valvesoftware.com/wiki/Steam_Application_IDs

        URL Format: 
            https://steamcommunity.com/market/listings/730/ +
              StatTrak%E2%84%A2%20 (If it StatTrak) +
              Item Name (With character escape for URL) +
              WEAR

        Returns:
            str: This function returns the full URL for a requested item.
        """

        URL = self._steam_url_marketplace + f"/{appid}/"

        if not item:
            raise ErrorInvalidParameters

        if "★" in item:
            URL += "%E2%98%85%20"

        if "StatTrak™" in item:
            URL += "StatTrak%E2%84%A2%20"

        URL += item\
            .replace("★ ", "")\
            .replace("StatTrak™ ", "")\
            .replace(" ", "%20")\
            .replace("|", "%7C")\
            .replace("(", "%28")\
            .replace(")", "%29")

        return URL

    def _format_date(self, date: str) -> str:
        """
        Format date string to YYYY-MM-DD pattern.

        Parameters:
            date (str): A date on steam's format e.g `Nov 30 2011`

        Returns:
            This function returns the date in the format `2011-11-30`
        """

        month, day, year = date.split(' ')

        new_date = day + '-' + month.replace('"', "") + '-' + year
        new_date = datetime.strptime(new_date, "%d-%b-%Y").date()

        return new_date

    def get_observations(self, appid: int, item: str, fill: bool = True) -> pd.DataFrame:
        """ 
        Get historical values from a Steam's item.

        The web crawler goes to the Steam's Marketplace and return a list
        with the date and historical values (in Dollar) from the item.

        Each element of the list is a string that contains three elments split by comma e.g:
            '"Nov 30 2013 01: +0",20.402,"1"'

        Where:
            - 1st: Date (Month, Day, Year, Hour and UTC)
            - 2nd: Value (American Dollar by default)
            - 3rd: Sold Amount at this price (Integer value)

        Parameters:
            appid (int): App game id on steam.
            item (str): The name of the item you want.
            fill (bool): Fill missing values with the last observation?

        Notes:
        - You can find all Ids here: https://developer.valvesoftware.com/wiki/Steam_Application_IDs

        Returns:
            DataFrame: A DataFrame with all historical sell of requested item on Steam's Marketplace.
        """

        URL = self._get_url_item(appid=appid, item=item)

        html_page = requests.get(url=URL).text
        soup = BeautifulSoup(html_page, "html.parser")

        pattern = re.compile(r"(line1)\=([^)]+)\;")

        try:
            data = pattern.search(str(soup.getText)).groups()[1]
            data = data[2:len(data)-2].split(sep="],[")
            data = str(data)
        except Exception as e:
            raise_error_response(error=ErrorResourceNotFound)

        date_list = re.compile(r"[a-zA-Z]+ \d+ \d+").findall(data)
        value_list = re.compile(r"\d+\.\d+").findall(data)

        steam_dataframe = pd.DataFrame(
            list(zip(date_list, value_list)),
            columns=["date", "value"]
        )

        steam_dataframe = steam_dataframe.assign(
            date=lambda dataframe: dataframe["date"].map(
                lambda date: self._format_date(date))
        )

        steam_dataframe["value"] = steam_dataframe["value"].astype(
            float).round(2)
        steam_dataframe["date"] = steam_dataframe["date"].astype(str)

        steam_dataframe = steam_dataframe.groupby(
            by="date", as_index=False).aggregate(np.mean)

        if fill:
            # If param `fill` is True,
            # We build an auxiliary dataframe specifying a date range that
            # takes into account the lowest and hightest values of dates
            # coming from Steam.

            start = steam_dataframe.date[0]
            end = steam_dataframe.date[len(steam_dataframe.date) - 1]

            new_dataframe = pd.DataFrame({
                "date": pd.period_range(start, end, freq="D")
            })

            new_dataframe["date"] = new_dataframe["date"].astype(str)
            steam_dataframe["date"] = steam_dataframe["date"].astype(str)

            steam_dataframe = pd.merge(
                new_dataframe, steam_dataframe,
                on="date", how="outer"
            )

            steam_dataframe = steam_dataframe.fillna(method="ffill")

        return steam_dataframe
