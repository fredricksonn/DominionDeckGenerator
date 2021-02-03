# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:26:34 2021

@author: Robert
"""
import pandas as pd
import re
from random import randint
import collections

from gui.tkinter import get_selection

EDITION_RE = re.compile('^(.*), (\d)E')

def unique(seq):
    """
    Return unique list maintaining order
    https://stackoverflow.com/a/480227
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def downselect_sets( deck, override=[]):
    # Get all sets in deck
    all_sets = unique(deck['Set'])
    set_w_editions = {}
    for dom_set in all_sets:
        match = EDITION_RE.match(dom_set)
        if match:
            set_w_editions.setdefault(match.group(1),[])
            set_w_editions[match.group(1)].append(match.group(2))
    
    # Remove base name from sets with editions (you dont want Base, Base1E and Base2E)
    for dom_set in set_w_editions:
        all_sets.remove(dom_set)
    
    # Make sure editons are sorted properly
    # TODO
    print(all_sets)
    
    
    if not override:
        # Get selected decks from GUI
        selected_decks = get_selection('Deck Selection',all_sets)
    else:
        # Use override as deck selection
        selected_decks = override
    
    # Check for selected sets with additions (you need to add back in the base name)
    for dom_set in selected_decks:
        match = EDITION_RE.match(dom_set)
        if match:
            base = match.group(1)
            if base not in selected_decks:
                selected_decks.append(base)
            
    
    # Build slice
    slice_ = []
    for sel in selected_decks:
        print(sel)
        if len(slice_)>0:
            slice_ = slice_ | (deck['Set']==sel)
        else:
            slice_ = deck['Set']==sel
    
    # Downselect
    if len(slice_)>0:
        downselect = deck[slice_]
    else:
        downselect = deck
    return downselect

Stats = collections.namedtuple('Stats',['min','max','mean'])

def getStats (df):
    S = Stats(min=df['Cost'].min(),max=df['Cost'].max(),mean=-1)
    return S

if __name__=='__main__':
    deck = pd.read_csv('data/dominion_cards.csv')
    override = ['Base, 2E', 'Intrigue, 2E']#'Base, 2E', 'Intrigue, 2E', 'Seaside', 'Prosperity']
    deck = downselect_sets( deck, override=override )

    #stats = getStats(deck)
    #print(stats.min)
    #print(stats.max)
    
    # deck, supply = separate_supply( desk )
    deck.to_csv('temp.csv')
