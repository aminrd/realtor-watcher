import pandas as pd
import numpy as np
import argparse
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-ln', '--links', type=str, default='links.csv', help="Path to the input csv file")
args = parser.parse_args()

links = pd.read_csv(args.links)

# Validating the file
key_list = ['links', 'previous-price', 'new-price']
for key in key_list:
    if not key in links.keys():
        raise ImportError(f"{key} header not exists in the input file! Check again your file")

