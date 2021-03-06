# This class is for checking prices in realtor.ca
import requests
import re
DEBUG_MODE = True



class RealtorCa:
    def __init__(self, url, previous_price, user_agent=None):
        self.url = url
        self.previous_price = previous_price

        if user_agent is None:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
            }
        else:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'User-Agent': user_agent
            }

        if 'https' in url:
            url = url.replace('https', 'http')
        response = requests.get(url, headers=headers)

        if DEBUG_MODE and 'robot' in response.text.lower():
            print("Robot was detected!")

        plist = re.findall("price: '(.*)'", response.text)
        plist = list(float(x) for x in plist)
        self.current_price = max(plist)

    def get_updates(self):
        if self.previous_price != self.current_price:
            has_updates = True
        else:
            has_updates = False

        return {
            'link': self.url,
            'previous-price': self.previous_price,
            'current-price': self.current_price,
            'updates': has_updates
        }
