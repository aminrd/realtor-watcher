import pandas as pd
import numpy as np
import argparse
import datetime
from tqdm import tqdm
import time
from fake_useragent import UserAgent

# Real estate sites:
from realtor_ca import RealtorCa

parser = argparse.ArgumentParser()
parser.add_argument('-ln', '--links', type=str, default='links.csv', help="Path to the input csv file")
parser.add_argument('-uf', '--update_file', type=str, default='updates.txt', help="Path to the txt update file")
parser.add_argument('--verbose', type=str, default='False', help="Printing the status [True or False]")
args = parser.parse_args()

if args.verbose == 'True':
    verbose = True
else:
    verbose = False

verbose = True
ua = UserAgent()


links = pd.read_csv(args.links)

# Validating the file
key_list = ['links', 'previous-price', 'current-price']
for key in key_list:
    if not key in links.keys():
        raise ImportError(f"{key} header not exists in the input file! Check again your file")

links = links.fillna(0)
links_updated = links.copy()

for i in tqdm(range(links.shape[0]), desc='Checking urls'):

    # =========================================================
    # Waiting 5 seconds to bypass realtor sites robot checkers
    time.sleep(5)
    # =========================================================

    try:
        obj = RealtorCa(
            links['links'][i],
            links['current-price'][i],
            user_agent=ua.random
        )
        out = obj.get_updates()
    except Exception as e:
        if verbose:
            print(f"Error: {str(e)}")

        out = {
            'link': links['links'][i],
            'previous-price': links['previous-price'][i],
            'current-price': links['current-price'][i],
            'updates': False
        }

    prev = out['previous-price']
    curr = out['current-price']
    url = out['link']

    if out.get('updates', False):
        time_now = datetime.datetime.now()
        update_string = f'[{time_now.isoformat()}]\t {prev} -> {curr} \t link: {url}'

        if verbose:
            print(update_string)

        with open(args.update_file, 'a+') as f:
            f.write(update_string)

    links_updated['previous-price'][i] = prev
    links_updated['current-price'][i] = curr

links_updated.to_csv(args.links, index=False)

if verbose:
    print("All links were successfully checked!")
