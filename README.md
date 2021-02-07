# DominionDeckGenerator
This is a package to create playable decks for Dominion, based on what Expansions are available, and what style of game you want to play.
# Development notes
## Packages required for development
## Web Scraping Tutorial
https://medium.com/analytics-vidhya/web-scraping-a-wikipedia-table-into-a-dataframe-c52617e1f451
## Wiki Table of all cards
http://wiki.dominionstrategy.com/index.php?title=List_of_cards&action=edit

# ToDo list
Create QT Gui
- Blank Gui
- Add user options
- Add/animate images
- Interact with Algorithm

Create interface for Django
Develop Weightings
Decide on user options
- Number of cards (10/12)
- +2 Action
- +2 Buy
- +2+ Cards
- Mean of distribution
- Attack (y/n)
- - Reaction (y/n)
- Choose Distribution type

# Engine
Steps 2 and 3a/3b can be done in parallel

1. Downselect Deck to chosen expansions
2. Create cost distribution (based on input)
3a. Generate weightings
3b. Draw X cards from weighted deck
4. Fill cost distribution