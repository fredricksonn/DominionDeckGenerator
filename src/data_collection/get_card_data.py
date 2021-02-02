# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:29:47 2021

@author: Robert
"""
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

# Compiled regexs
debt = re.compile('^(\d*)D$')

# Request site
source = requests.get('http://wiki.dominionstrategy.com/index.php/List_of_cards').text

# Parse html with bs4
soup = BeautifulSoup(source, 'lxml')

# Replace all images with alt text (except when alt texts contain .jpg like the card images)
for img in soup.find_all('img'): #find all img elements
    if 'alt' in img.attrs:       #check if img has alt text
        if '$' in img.attrs['alt'] or img.attrs['alt'] in ['VP','P']:
            img.replace_with(img.attrs['alt'])
        elif debt.match(img.attrs['alt']):
            img.replace_with( '<'+debt.match(img.attrs['alt']).group(1)+'Debt>' )
        elif '.jpg' not in img.attrs['alt']:
            print('non-replaced alt text: '+img.attrs['alt'])
            
# Convert back to html
source = str(soup)

# Parse html into pandas dataframe
df = pd.read_html(source)[0]

# Write to csv
df.to_csv('../data/dominion_cards.csv')