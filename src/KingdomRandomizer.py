# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:45:36 2021

@author: Robert
"""
import copy
import pandas as pd
# from math import prod
from numpy.random import choice

def prod(iterable):
    cumulative = 1
    for val in iterable:
        cumulative *= val
    return cumulative

def calc_score( cards, 
               cost_group_weights={(1,2):1, (3,):2, (4,):2, (5,):2, (6,7,8):1}, 
               type_multipliers={'isActionSupplier':1.05,'isDrawer':1.05,'isAttack':0},
               ):
    cost_options = set(cards['cost_combined'])
    cost_counts  = {cost:sum(cards['cost_combined']==cost) for cost in cost_options}
    cost_counts_group = {}
    cost_wpc = {}
    weights_tot = sum(cost_group_weights.values())
    num_cards = len(cards)
    for group in cost_group_weights:
        group_cards = sum([(cost_counts[cost] if cost in cost_counts else 0) for cost in group])
        group_weight = cost_group_weights[group]/weights_tot
        weight_per_card = group_weight/group_cards
        for cost in group:
            cost_wpc[cost] = weight_per_card
    cards['score_cost'] = cards.apply(lambda row: cost_wpc[row['cost_combined']], axis=1)
    cards['score_mult'] = cards.apply(lambda row: prod([ type_multipliers[col] for col in type_multipliers if row[col]]), axis=1)
    tempScore = cards.apply(lambda row: row['score_cost']*row['score_mult'], axis=1)
    cumulative_score = sum(tempScore)
    cards['score'] = tempScore/cumulative_score
    return

def select_kingdom( cards, num_cards_in_kingdom ):
    sel_idxs = choice(cards.index, p=cards['score'], size=num_cards_in_kingdom, replace=False)
    return cards.loc[sel_idxs].sort_values(by='cost_combined')

decks_selected = []
decks_selected = ['Dominion II', 'Intrigue II', 'Seaside', 'Prosperity']
all_cards = pd.read_csv('../deck_data/decks/cards.csv')
if 'Unnamed: 0' in all_cards:
    del all_cards['Unnamed: 0']
potion_val = 2
all_cards['cost_combined'] = all_cards['cost_treasure'] + all_cards['cost_debt'] + potion_val*all_cards['cost_potion']
# cost_tuple = cards.apply(lambda row: (row['cost_treasure']+row['cost_debt'],row['cost_potion']), axis=1)

if decks_selected:
    for i, deck in enumerate(decks_selected):
        if i==0:
            deck_slice = all_cards['deck']==deck
        else:
            deck_slice = deck_slice | (all_cards['deck']==deck)
    sel_cards = all_cards[deck_slice]
else:
    sel_cards = copy.deepcopy(all_cards)

calc_score( sel_cards )

kingdom = select_kingdom( sel_cards, num_cards_in_kingdom=10 )

kingdom.to_csv('temp.csv')