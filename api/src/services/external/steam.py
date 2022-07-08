import re
from bs4 import BeautifulSoup
from fastapi import HTTPException
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from src.utils.api_errors import ErrorInvalidParameters, ErrorResourceNotFound, raise_error_response


class SteamService:
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

    def _url_item(self, item: str) -> str:
        """
        Get URL for a Steam item.

        Parameters: 
            item (str): Full name of an item of CS:GO on steam community market.

        Example:
            ★ StatTrak™ Flip Knife | Freehand (Factory New)

        URL Format: 
            https://steamcommunity.com/market/listings/730/ +
              StatTrak%E2%84%A2%20 (If it StatTrak) +
              Item Name (With character escape for URL) +
              WEAR

        Returns:
            str: This function returns the full URL for a requested item.
        """

        # Base URL from CS:GO Items
        URL = self._steam_url_marketplace

        if not item:
            raise ErrorInvalidParameters

        # Escape from html
        if "★" in item:
            URL += "%E2%98%85%20"

        if "StatTrak™" in item:
            URL += "StatTrak%E2%84%A2%20"

        # Final URL for item
        URL += item\
            .replace("★ ", "")\
            .replace("StatTrak™ ", "")\
            .replace(" ", "%20")\
            .replace("|", "%7C")\
            .replace("(", "%28")\
            .replace(")", "%29")

        return URL

    def _make_date_format(self, date: str) -> str:
        """
        Format date string to YYYY-MM-DD pattern.

        Parameters:
            date (str): A date on steam's format e.g `Nov 30 2011`

        Returns:
            This function returns the date in the format `2011-11-30`
        """

        month, day, year = date.split(' ')

        date = day + '-' + month.replace('"', "") + '-' + year
        date = datetime.strptime(date, "%d-%b-%Y").date()

        return date

    def _get_steam_historical_values(self, item: str) -> list:
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
            item (str): The name of the item (skin) you want.

        Returns:
            list: A list with all historical sell of requested item on Steam's Marketplace.
        """

        # Steam endpoint
        URL = self._url_item(item=item)

        # Get the page
        html_page = requests.get(url=URL).text
        soup = BeautifulSoup(html_page, "html.parser")

        # Pattern to extract values
        pattern = re.compile(r"(line1)\=([^)]+)\;")

        # Extract the pattern string
        try:
            data = pattern.search(str(soup.getText)).groups()[1]
            data = data[2:len(data)-2].split(sep="],[")
        except Exception as e:
            raise_error_response(error=ErrorResourceNotFound)

        return data

    def get_item_marketplace_values(self, item: str, fill: bool = True) -> list:
        """
        Get a time series from a requested item.

        Parameters:
            item (str): The full name of requested item (Includes special characters).
            fill (bool): If True, fill values with the last observation (Default is True).

        Examples:
            item="AK-47 | Safari Mesh (Factory New)"
            item="★ StatTrak™ Flip Knife | Freehand (Factory New)"

        Returns:
            list: A list (json) with the date and value of sell.

        """
        # Array with item data
        data = str(self._get_steam_historical_values(item=item))

        # Extract `date` and `value` from array (converted to string)
        item_dates = re.compile(r"[a-zA-Z]+ \d+ \d+").findall(data)
        item_values = re.compile(r"\d+\.\d+").findall(data)

        # Build a pandas dataframe
        steam_dataframe = pd.DataFrame(
            list(zip(item_dates, item_values)),
            columns=["date", "value"]
        )

        # Standard date format
        steam_dataframe = steam_dataframe.assign(
            date=lambda dataframe: dataframe["date"].map(
                lambda date: self._make_date_format(date))
        )

        # Changing type of columns
        steam_dataframe["value"] = steam_dataframe["value"].astype(float)
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
                new_dataframe, steam_dataframe, on="date", how="outer")

            steam_dataframe = steam_dataframe.fillna(method="ffill")

        steam_dataframe["value"] = steam_dataframe["value"].round(2)

        return steam_dataframe.to_dict("records")
