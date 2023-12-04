# cs337-project2

Group composed of Kyle Soni and Anges Vu
https://github.com/kylesoni/cs337-project2

## To run:
- Run web_scraper.py for interface and do similar things to video
- Run main.py after changing url to get direct output from parsing

## Requirements:
- Python version: 3.11.5
- pip requirements: bs4, requests, re, and spacy

## Supported Questions
- What is/are x?
- How do I x?
- How do I do that? (conditional on complicated method present in step)
- How much/many -ingredient(s)- do I need? (step must contain the inquired ingredient)
- What are the tools in this step?/What tools do I need?
- What are the cooking methods of this step?
- How do I prepare -ingredient-?/What is the needed preparation for -ingredient-?
- What is the temperature?
- What is the heat setting?
- How long is this step?/What is the time needed for this step?

## Supported Transformations
- Vegan
- Vegetarian
- Kosher
- Healthy

## Supported Operations
- start
- next/continue
- repeat/current step
- quit
- go back
- go to nth step
    - go from here
    - return/go back
- y/yes/n/no

## Recipes from Videos
- [https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/]
- [https://www.allrecipes.com/mexican-polenta-pizza-recipe-7508449]