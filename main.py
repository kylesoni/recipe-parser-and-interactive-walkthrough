from bs4 import BeautifulSoup
import requests
from recipe import Recipe
from ingredient import Ingredient
import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

url = "https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.text
body = soup.body.text

ingredient_list = []
ing_results = soup.find(id="mntl-structured-ingredients_1-0")
list_of_ing = ing_results.find_all("li")
for list in list_of_ing:
    ingredient_list.append(list.get_text().strip(' \n\r\t'))

steps = []
steps_results = soup.find(id="recipe__steps_1-0")
directions = steps_results.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
for step in directions:
    steps.append(step.get_text().strip(' \n\r\t'))

#print(scraper.ingredients())
#print(scraper.instructions_list())

test_recipe = Recipe(ingredient_list, steps)
test_recipe.test_ingredients()
# print(test_recipe.progress_step().text)
# print(test_recipe.ingredients[-1].ingredient)