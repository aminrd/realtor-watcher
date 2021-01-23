# This class is for checking prices in realtor.ca
import requests
import re

class RealtorCa:
    def __init__(self, url, previous_price):
        self.url = url
        self.previous_price = previous_price

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
        }

        if 'https' in url:
            url = url.replace('https', 'http')
        response = requests.get(url, headers=headers)

