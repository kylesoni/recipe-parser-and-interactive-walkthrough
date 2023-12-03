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
ing_results = soup.find(id="mntl-lrs-ingredients_1-0")
list_of_ing = ing_results.find_all(["p"])
for list in list_of_ing:
    ingredient_list.append(list.get_text().strip(' \n\r\t'))

# get steps
steps = []
steps_results = soup.find(id="recipe__steps_1-0")
directions = steps_results.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
for step in directions:
    steps.append(step.get_text().strip(' \n\r\t'))

RECIPE = Recipe(ingredient_list, steps)

# get user input for ingredients or steps
print("Alright! Let's walk through " + title + ". What do you want to do?\n[1] Go over ingredients list\n[2] Go over recipe steps")
user_input = input()
if user_input.__contains__('1'):
    print("Here is the ingredient list:\n")
    for key in RECIPE.ingredient_groups:
        print(key + ": ")
        for ing in RECIPE.ingredient_groups[key]:
            print(ing.raw)
        print("")
elif user_input.__contains__('2'):
    for step in RECIPE.steps:
        print(step.text)
else:
    print("Sorry, I didn't get that. Can you input a selection of 1 or 2?")

i = True
while i:
    print("What would you like to do now?")
    user_input = input()
    user_input = re.sub(r'[,.!?@#$%^&*_~]', '', user_input)
    
    # if it's a Google question
    google_query_pattern = '((W|w)hat is ([^\?]*)|(W|w)hat are ([^\?]*)|(H|h)ow do I ([^\?]*))'
    query = re.match(google_query_pattern, user_input)
    if query:
        search = user_input.strip().replace(' ','+')
        url = 'https://google.com/search?q=' + search
        print('Here is what I found: ' + url)
    
    # if it's an ingredient amount question
    ing_query_pattern = 'How much |How many | do I need'
    query = re.match(ing_query_pattern, user_input)
    if query:
        query = re.split(ing_query_pattern, user_input)
        for ing in RECIPE.ingredients:
            if re.match(ing.ingredient, query[1]):
                print((ing.amount) + " " + (ing.unit))
                break
            # elseif made it to last ingredient and still no match:
            #     print("Ingredient not found")
    
    # if it's a list request
    list_query_pattern = 'Show me the '
    list_options = ['ingredients list', 'recipe list']
    query = re.match(list_query_pattern, user_input)
    if query:
        query = re.split(list_query_pattern, user_input)
        print(query[1])
        print(list_options[0])
        for list in list_options:
            if re.match(query[1], list_options[0]):
                print("Here is the ingredient list:\n")
                for ing in RECIPE.ingredients:
                    print(ing.amount + " " + ing.unit + " " + ing.ingredient)
            elif re.match(query[1], list[1]):
                print("Here is the recipe list:\n")
                for step in RECIPE.steps:
                    print(step.text)

    # if user wants to quit
    quit_pattern = 'quit'
    query = re.match(quit_pattern, user_input)
    if query:
        print("Thanks for walking through the recipe with me. Goodbye!")
        break



ing_name = []
ing_quantity = []
ing_measurement = []
tools = []
cook_methods = []