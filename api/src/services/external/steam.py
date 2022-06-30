import re
from bs4 import BeautifulSoup
import requests


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

        # Return URL
        return URL

    def get_item_marketplace_values(self, item: str) -> list:

        URL = self._url_item(item=item)

        # Get the page
        html_page = requests.get(url=URL).text
        soup = BeautifulSoup(html_page, "html.parser")

        # Pattern to extract values
        pattern = re.compile(r"(line1)\=([^)]+)\;")

        # Extract the pattern string
        data = pattern.search(str(soup.getText)).groups()[1]
        data = data[2:len(data)-2].split(sep="],[")

        # Auxiliar variable
        final_data = []

        for sale in data:
            # Split data
            date, value, count = sale.split(',')

            # Make date format
            month, day, year, hour, utc = date.split(' ')
            date = day + '-' + month.replace('"', "") + '-' + year
            utc = utc.replace('"', "")

            sales_data = {
                'date': date,
                'hour': hour + "00",
                'utc': utc,
                'value_dollar': value,
                'count': count.replace('"', "")
            }

            final_data.append(sales_data)

        return final_data
