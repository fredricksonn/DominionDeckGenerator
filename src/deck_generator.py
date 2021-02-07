# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:26:34 2021

@author: Robert
"""
import pandas as pd
import re
from scipy import random
import math
import collections

from gui.tkinter import get_selection

EDITION_RE = re.compile('^(.*), (\d)E')
Stats = collections.namedtuple('Stats',['min','max','mean'])

class DeckGenerator():

    def unique(self, seq):
        """
        Return unique list maintaining order
        https://stackoverflow.com/a/480227
        """
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def downselect_sets(self, deck, override=[]):
        # Get all sets in deck
        all_sets = self.unique(deck['Set'])
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
        #print(all_sets)
        
        
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



    # Given upper and lower bounds, can calculate sigma and mean
    # returns a sorted list of random ints bewteen upper and lower bounds
    def gaussDist(self, upper, lower, sz=10, sigma=-1, mean=-1):
        if mean == -1:
            mean = (upper + lower)/2
            print("Using calculated mean : {}".format(str(mean)))
        if sigma == -1:
            sigma = (mean-lower)/2
            print("Using calculated sigma: {}".format(str(sigma)))

        results = random.default_rng().normal(loc=mean,scale=sigma,size=sz)
        results = [ math.floor(x) for x in results ]
        results = [ lower if x < lower else x for x in results ]
        results = [ upper if x > upper else x for x in results ]
        results.sort()
        return results

    def getStats (self, df, field='Cost'):
        S = Stats(min=df[field].min(),max=df[field].max(),mean=-1)
        return S

    def getCostDistOfKingdomCards(self, df):
        kingdomCards = df[df['CardClass'] != 'Basic']
        stats = self.getStats(kingdomCards,'CostValue')
        return self.gaussDist(int(stats.max), int(stats.min))

    # lambda function to get the value of cost and create a new col for it
    def getValFromCost(self, row):
        cost=row['Cost']
        if type(cost) == int:
            return cost
        if '$' in cost:
            return cost.replace('$','')

    def runMain(self):
        deck = pd.read_csv('data/dominion_cards.csv')
        override = ['Base, 2E', 'Intrigue, 2E']#'Base, 2E', 'Intrigue, 2E', 'Seaside', 'Prosperity']
        deck = self.downselect_sets( deck, override=override )

        # add CostValue column
        deck['CostValue'] = deck.apply(lambda row: self.getValFromCost(row),axis=1)

        Dist = self.getCostDistOfKingdomCards(deck)
        print(Dist)    
        # deck, supply = separate_supply( desk )
        deck.to_csv('temp.csv')    

if __name__=='__main__':
    DG = DeckGenerator()
    DG.runMain()
