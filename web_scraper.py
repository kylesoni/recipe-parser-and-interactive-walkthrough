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
    ing_query_pattern = '((H|h)ow much |(H|h)ow many | do I need)'
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
    # list_query_pattern = '((S|s)how me the |(G|g)o over the |1|2)'
    ing_list_pattern = ['ingredients list', '1']
    rec_list_pattern = ['recipe steps', '2']

    if user_input.__contains__(ing_list_pattern[0])|user_input.__contains__(ing_list_pattern[1]):
        for pattern in ing_list_pattern:
            if re.search(pattern, user_input):
                print("Here is the ingredient list:\n")
                for key in RECIPE.ingredient_groups:
                    print(key + ": ")
                    for ing in RECIPE.ingredient_groups[key]:
                        print(ing.raw)
                    print("")
    if user_input.__contains__(rec_list_pattern[0])|user_input.__contains__(rec_list_pattern[1]):
        for pattern in rec_list_pattern:
            if re.search(pattern, user_input):
                print("Here are the recipe steps:\n")
                for step in RECIPE.steps:
                    print(step.text)

    # first step
    start_query_pattern = 'start'
    if user_input.__contains__(start_query_pattern):
        print('Alright, let\'s start! Here is the first step:')
        print(RECIPE.progress_step().text)

    # current step
    curstep_query_pattern = '(repeat|step again)'
    if user_input.__contains__(curstep_query_pattern):
        print('Here is the current step:')
        print(RECIPE.steps[RECIPE.current_step].text)

    # next step
    nextstep_query_pattern = '(next|next step)'
    query = re.match(nextstep_query_pattern, user_input)
    if query:
        print('Here is the next step:')
        print(RECIPE.progress_step().text)

    # if user wants to quit
    quit_pattern = '(quit|stop)'
    query = re.match(quit_pattern, user_input)
    if query:
        print("Thanks for walking through the recipe with me. Goodbye!")
        break



ing_name = []
ing_quantity = []
ing_measurement = []
tools = []
cook_methods = []