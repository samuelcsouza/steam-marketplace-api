import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import numpy as np


class SteamService:

    def __init__(self, steam_url_marketplace: str) -> None:
        self._steam_url_marketplace = steam_url_marketplace

    def _url_item(self, item: str) -> str:
        """ GET URL FOR A STEAM ITEM.

        Param: item = Full name of an item of CS:GO on steam community market.
        Example: ★ StatTrak™ Flip Knife | Freehand (Factory New)

        URL Format: https://steamcommunity.com/market/listings/730/ +
              StatTrak%E2%84%A2%20 (If it StatTrak) +
              Item Name (With character escape for URL) +
              WEAR

        This function returns the full URL for a requested item.
        """

        # Base URL from CS:GO Items
        URL = self._steam_url_marketplace

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
        FORMAT DATE STRING TO YYYY-MM-DD PATTERN.

        Param: date = A date on steam's format e.g `Nov 30 2011`

        This function returns the date in the format `2011-11-30`
        """

        month, day, year = date.split(' ')

        date = day + '-' + month.replace('"', "") + '-' + year
        date = datetime.strptime(date, "%d-%b-%Y").date()

        return date

    def _get_steam_historical_values(self, item: str) -> list:
        """ GET HISTORICAL VALUES FROM A STEAM'S ITEM.

        Param: item = The name of the item (skin) you want.

        The web crawler goes to the Steam's Marketplace and return a list
        with the date and historical values (in Dollar) from the item.

        Each element of the list is a string that contains three elments split by comma e.g:
            '"Nov 30 2013 01: +0",20.402,"1"'

        Where:
            - 1st: Date (Month, Day, Year, Hour and UTC)
            - 2nd: Value (American Dollar by default)
            - 3rd: Sold Amount at this price (Integer value)

        """

        # Steam endpoint
        URL = self._url_item(item=item)

        # Get the page
        html_page = requests.get(url=URL).text
        soup = BeautifulSoup(html_page, "html.parser")

        # Pattern to extract values
        pattern = re.compile(r"(line1)\=([^)]+)\;")

        # Extract the pattern string
        data = pattern.search(str(soup.getText)).groups()[1]
        data = data[2:len(data)-2].split(sep="],[")

        return data

    def get_item_marketplace_values(self, item: str) -> list:

        data = self._get_steam_historical_values(item=item)

        all_data = []

        for sale in data:
            # Split data
            date, value, count = sale.split(',')

            # Make date format
            month, day, year, hour, utc = date.split(' ')

            date = day + '-' + month.replace('"', "") + '-' + year
            date = datetime.strptime(date, "%d-%b-%Y").date()

            sales_data = {
                'date': date,
                'value': value,
            }

            all_data.append(sales_data)

        steam_dataframe = pd.DataFrame(all_data)
        steam_dataframe = steam_dataframe[[
            "date", "value"]].sort_values(by="date")

        start = steam_dataframe.date[0]
        end = steam_dataframe.date[len(steam_dataframe.date) - 1]

        new_dataframe = pd.DataFrame({
            "date": pd.period_range(start, end, freq="D")
        })

        new_dataframe["date"] = new_dataframe["date"].astype("str")

        steam_dataframe["date"] = steam_dataframe["date"].astype("str")

        skin_dataframe = pd.merge(
            new_dataframe, steam_dataframe, on="date", how="outer")

        skin_dataframe["value"] = skin_dataframe["value"].astype("float64")
        skin_dataframe["date"] = skin_dataframe["date"].astype("str")

        skin_dataframe = skin_dataframe.groupby(
            by="date", as_index=False).aggregate(np.mean)

        skin_dataframe = skin_dataframe.fillna(method="ffill")

        skin_dataframe["value"] = skin_dataframe["value"].round(2)

        return skin_dataframe.to_dict("records")
