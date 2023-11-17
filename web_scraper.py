import bs4
import requests
from bs4 import BeautifulSoup
import re
from recipe import Recipe

# receive URL input from user
url = input("Hello! I can help walk you through a recipe from AllRecipes.com. Please enter a URL:")
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# get recipe title
title = soup.title.text
body = soup.body.text

# get ingredients
ingredient_list = []
ing_results = soup.find(id="mntl-structured-ingredients_1-0")
list_of_ing = ing_results.find_all("li")
for list in list_of_ing:
    ingredient_list.append(list.get_text().strip(' \n\r\t'))

# get steps
steps = []
steps_results = soup.find(id="recipe__steps_1-0")
directions = steps_results.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
for step in directions:
    steps.append(step.get_text().strip(' \n\r\t'))

RECIPE = Recipe(ingredient_list, steps)

print(RECIPE.test_ingredients())

# # get user input for ingredients or steps
# print("Alright! Let's walk through " + title + ". What do you want to do?\n[1] Go over ingredients list\n[2] Go over recipe steps")
# user_input = input()
# if user_input.__contains__('1'):
#     print(ingredient_list)
# elif user_input.__contains__('2'):
#     print(steps)
# else:
#     print("Sorry, I didn't get that. Can you input a selection of 1 or 2?")

# # regex for external info
# query_pattern = '(What is ([^\?]*)|How do I ([^\?]*))'

# i = True
# while i:
#     print("What would you like to do now?")
#     user_input = input()
#     # 
#     query = re.match(query_pattern, user_input)
#     if query:
#         search = user_input.strip().replace(' ','+')
#         url = 'https://google.com/search?q=' + search
#         print('Here is what I found: ' + url)



# ing_name = []
# ing_quantity = []
# ing_measurement = []
# tools = []
# cook_methods = []