from bs4 import BeautifulSoup
import requests
from recipe import Recipe
from ingredient import Ingredient
import transformations
import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

url = "https://www.allrecipes.com/chicken-fra-diavolo-recipe-8383615"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.text
body = soup.body.text

ingredient_list = []
ing_results = soup.find(id="mntl-structured-ingredients_1-0")
list_of_ing = ing_results.find_all("li")
ing_headings = soup.find(id="mntl-lrs-ingredients_1-0")
list_of_headings = ing_headings.find_all(["p"])
# for list in list_of_ing:
#     ingredient_list.append(list.get_text().strip(' \n\r\t'))
for list in list_of_headings:
    ingredient_list.append(list.get_text().strip(' \n\r\t'))
#print(ingredient_list)

steps = []
steps_results = soup.find(id="recipe__steps_1-0")
directions = steps_results.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
for step in directions:
    steps.append(step.get_text().strip(' \n\r\t'))

#print(scraper.ingredients())
#print(scraper.instructions_list())

test_recipe = Recipe(ingredient_list, steps)
# test_recipe.test_ingredient_groups()
#test_recipe.test_ingredients()
#test_recipe.test_steps()
# print(test_recipe.progress_step().text)
# print(test_recipe.ingredients[-1].ingredient)

veggie_recipe = transformations.make_healthy(test_recipe)
veggie_recipe.test_ingredients()