import bs4
import requests
from bs4 import BeautifulSoup
import re
from recipe import Recipe
import transformations

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
ing_headings = soup.find(id="mntl-lrs-ingredients_1-0")
list_of_headings = ing_headings.find_all(["p"])
for list in list_of_headings:
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

flag = True
while flag:
    print("What would you like to do now?")
    user_input = input()
    user_input = re.sub(r'[,.!?@#$%^&*_~]', '', user_input)
    
    # if it's a list request
    ing_list_regex = '(ingredients list|^1$)'
    rec_list_regex = '(recipe steps|^2$)'
    ing_list_pattern = ['ingredients list', '1']
    rec_list_pattern = ['recipe steps', '2']

    if re.match(ing_list_regex, user_input):
        for pattern in ing_list_pattern:
            if re.search(pattern, user_input):
                print("Here is the ingredient list:\n")
                for key in RECIPE.ingredient_groups:
                    print(key + ": ")
                    for ing in RECIPE.ingredient_groups[key]:
                        print(ing.raw)
                    print("")
    if re.match(rec_list_regex, user_input):
        for pattern in rec_list_pattern:
            if re.search(pattern, user_input):
                print("Here are the recipe steps:\n")
                for step in RECIPE.steps:
                    print(step.text)

    # first step
    start_query_pattern = 'start'
    if user_input.__contains__(start_query_pattern):
        print('Alright, let\'s start! Here is the first step:')
        print(RECIPE.steps[0].text)
        RECIPE.current_step = RECIPE.current_step + 1

    # current step
    curstep_query_pattern = '((R|r)epeat|current step)'
    if re.match(curstep_query_pattern, user_input):
        print('Here is the current step:')
        print(RECIPE.steps[RECIPE.current_step].text)

    # next step
    nextstep_query_pattern = '((N|n)ext|(N|n)ext step|(C|c)ontinue)'
    query = re.match(nextstep_query_pattern, user_input)
    if query:
        response = RECIPE.progress_step()
        if isinstance(response, str):
            print(response)
        else:
            print('Here is the next step:')
            print(response.text)

    # last step
    laststep_query_pattern = '((G|g)o back|back)'
    query = re.match(laststep_query_pattern, user_input)
    if query:
        response = RECIPE.regress_step()
        if isinstance(response, str):
            print(response)
        else:
            print('Here is the previous step:')
            print(response.text)

    # nth step
    nthstep_query_pattern = '(((\d+)st step)|((\d+)nd step)|((\d+)rd step)|((\d+)th step))'
    if re.match(nthstep_query_pattern, user_input):
        step = int(re.findall(r'\d+', user_input)[0])
        new_current_step = step - 1
        if new_current_step >= (len(RECIPE.steps)-1):
            print('There is no step #' + str(step) + '.')
        else:
            print('Here is step #' + str(step) + ':')
            print(RECIPE.steps[new_current_step].text)
            print('Do you want to go from here or return to where you were before?')
            next_input = input()
            if re.search('((G|g)o from here)', next_input):
                RECIPE.current_step = new_current_step
                print("Okay, let's continue from here!")
            elif re.search('((R|r)eturn|(G|g)o back)', next_input):
                print("Okay, let\'s return to where you were before.")
    
    # if it's an ingredient amount question
    ing_query_pattern = '((H|h)ow much |(H|h)ow many | do I need)'
    query = re.match(ing_query_pattern, user_input)
    if query:
        query = re.split(ing_query_pattern, user_input)
        i = 0
        found = False
        for ing in RECIPE.steps[RECIPE.current_step].ingredients:
            if query[4] in RECIPE.steps[RECIPE.current_step].ingredients[i].ingredient:
                if (RECIPE.steps[RECIPE.current_step].ingredients[i].amount_clar != "") and not found:
                    if "to taste" in RECIPE.steps[RECIPE.current_step].ingredients[i].amount_clar:
                        print(RECIPE.steps[RECIPE.current_step].ingredients[i].amount + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].unit + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].ingredient + ", or to taste")
                    else:
                        print(RECIPE.steps[RECIPE.current_step].ingredients[i].amount + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].amount_clar + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].unit + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].ingredient)
                else:
                    print(RECIPE.steps[RECIPE.current_step].ingredients[i].amount + " " + RECIPE.steps[RECIPE.current_step].ingredients[i].unit)
                found = True
            i += 1
        if not found:
            print("Ingredient not found.")

    # if it's a tools question
    tools_query_pattern = 'tools'
    if user_input.__contains__(tools_query_pattern):
        print('Here are the tools needed in this step:')
        print('These are the prep tools: ' + str(RECIPE.steps[RECIPE.current_step].tools["prep"]).strip("[]").replace("'",""))
        print('These are the cooking tools: ' + str(RECIPE.steps[RECIPE.current_step].tools["step"]).strip("['']").replace("'",""))

    # if it's a methods question
    cook_query_pattern = '(cook|cooking|cooking method|method)'
    query = re.match(cook_query_pattern, user_input)
    if query:
        if len(RECIPE.steps[RECIPE.current_step].methods) == 0:
            print("There are no cooking methods involved in this step.")
        else:
            print('Here are the cooking methods involved with this step:')
            print(str(RECIPE.steps[RECIPE.current_step].methods).strip("[]").replace("'",""))

    # if it's a prep question
    prep_query_pattern = '((H|h)ow do I prep |(H|h)ow do I prepare |(H|h)ow do I prepare for |(W|w)hat is the needed preparation for )'
    query = re.match(prep_query_pattern, user_input)
    if query:
        query = re.split(prep_query_pattern, user_input)
        i = 0
        j = 0
        for ing in RECIPE.steps[RECIPE.current_step].ingredients:
            if re.match(RECIPE.steps[RECIPE.current_step].ingredients[i].ingredient, query[len(query)-1]) != None:
                if len(RECIPE.steps[RECIPE.current_step].ingredients[i].prep) == 0:
                    print('There is no preparation needed for ' + query[len(query)-1] + '.')
                else:
                    print('Here\'s how ' + query[len(query)-1] + ' need(s) to be prepped:')
                    print(RECIPE.steps[RECIPE.current_step].ingredients[i].prep)
                j += 10
            i += 1
            j += 1
            if j == (len(RECIPE.steps[RECIPE.current_step].ingredients)):
                print("Ingredient not found")

    # if it's a settings question
    temp_query_pattern = "((W|w)hat is the temperature|(W|w)hat is temperature|(W|w)hat is the temp|(W|w)hat is temp)"
    query = re.match(temp_query_pattern, user_input)
    if query:
        if RECIPE.steps[RECIPE.current_step].settings["Oven"] != "":
            print("The temperature should be: " + RECIPE.steps[RECIPE.current_step].settings["Oven"])
        elif RECIPE.steps[RECIPE.current_step].current_temp != "":
            print("The temperature should be: " + RECIPE.steps[RECIPE.current_step].current_temp)
        else:
            print("Temperature not found")

    heat_query_pattern = "((W|w)hat is the heat setting|(W|w)hat is heat)"
    query = re.match(heat_query_pattern, user_input)
    if query:
        if RECIPE.steps[RECIPE.current_step].settings["Stove"] != "":
            print("The stove settings should be: " + RECIPE.steps[RECIPE.current_step].settings["Stove"])
        else:
            print("Heat setting not found")

    # if it's a time question
    time_query_pattern = "((H|h)ow long|(W|w)hat is the time needed for)"
    query = re.search(time_query_pattern, user_input)
    if query:
        if RECIPE.steps[RECIPE.current_step].time["Hard"] != "" and RECIPE.steps[RECIPE.current_step].time["Soft"] != "":
            print("The time for this step is: " + RECIPE.steps[RECIPE.current_step].time["Hard"] + " or " + RECIPE.steps[RECIPE.current_step].time["Soft"])
        elif RECIPE.steps[RECIPE.current_step].time["Hard"] != "":
            print("The time for this step is: " + RECIPE.steps[RECIPE.current_step].time["Hard"])
        elif RECIPE.steps[RECIPE.current_step].time["Soft"] != "":
            print("The time for this step is: " + RECIPE.steps[RECIPE.current_step].time["Soft"])
        else:
            print("Time not found")

    # transformation to vegan
    vegan_transform_pattern = '(vegan)'
    query = re.search(vegan_transform_pattern, user_input)
    if query:
        print('Here\'s a vegan option for you:')
        new_recipe = transformations.meat_to_vegan(RECIPE)
        print("Here is the new ingredient list:\n")
        for key in new_recipe.ingredient_groups:
            print(key + ": ")
            for ing in new_recipe.ingredient_groups[key]:
                print(ing.raw)
            print("")
        print("Here are the new recipe steps:\n")
        for step in new_recipe.steps:
            print(step.text)
        print("Would you like to use this new recipe?")
        if re.match('(Y|y|(Y|y)es)', input()):
            RECIPE = new_recipe
            print("Okay, the recipe has been updated!")
            continue
        else:
            print("Okay, let\'s keep the original recipe.")
            continue

    # transformation to vegetarian
    vegetarian_transform_pattern = '(vegetarian)'
    query = re.search(vegetarian_transform_pattern, user_input)
    if query:
        print('Here\'s a vegetarian option for you:')
        new_recipe = transformations.meat_to_vegetarian(RECIPE)
        print("Here is the new ingredient list:\n")
        for key in new_recipe.ingredient_groups:
            print(key + ": ")
            for ing in new_recipe.ingredient_groups[key]:
                print(ing.raw)
            print("")
        print("Here are the new recipe steps:\n")
        for step in new_recipe.steps:
            print(step.text)
        print("Would you like to use this new recipe?")
        if re.match('(Y|y|(Y|y)es)', input()):
            RECIPE = new_recipe
            print("Okay, the recipe has been updated!")
            continue
        else:
            print("Okay, let\'s keep the original recipe.")
            continue

    # transformation to kosher
    kosher_transform_pattern = '(kosher)'
    query = re.search(kosher_transform_pattern, user_input)
    if query:
        print('Here\'s a kosher option for you:')
        new_recipe = transformations.make_kosher(RECIPE)
        print("Here is the new ingredient list:\n")
        for key in new_recipe.ingredient_groups:
            print(key + ": ")
            for ing in new_recipe.ingredient_groups[key]:
                print(ing.raw)
            print("")
        print("Here are the new recipe steps:\n")
        for step in new_recipe.steps:
            print(step.text)
        print("Would you like to use this new recipe?")
        if re.match('(Y|y|(Y|y)es)', input()):
            RECIPE = new_recipe
            print("Okay, the recipe has been updated!")
            continue
        else:
            print("Okay, let\'s keep the original recipe.")
            continue

    # transformation to healthy
    healthy_transform_pattern = '(healthy|healthier)'
    query = re.search(healthy_transform_pattern, user_input)
    if query:
        print('Here\'s a healthier option for you:')
        new_recipe = transformations.make_healthy(RECIPE)
        print("Here is the new ingredient list:\n")
        for key in new_recipe.ingredient_groups:
            print(key + ": ")
            for ing in new_recipe.ingredient_groups[key]:
                print(ing.raw)
            print("")
        print("Here are the new recipe steps:\n")
        for step in new_recipe.steps:
            print(step.text)
        print("Would you like to use this new recipe?")
        if re.match('(Y|y|(Y|y)es)', input()):
            RECIPE = new_recipe
            print("Okay, the recipe has been updated!")
            continue
        else:
            print("Okay, let\'s keep the original recipe.")
            continue
    
    # if it's a vague How to
    vague_pattern = '(H|h)ow do I do that'
    query = re.match(vague_pattern, user_input)
    if query:
        methods = RECIPE.steps[RECIPE.current_step].methods
        if len(methods) < 1:
            print("No method found, sorry! If you add more detail I may be able to help.")
        else:
            for method in methods:
                print("Here is how to " + method + ": " + "https://google.com/search?q=how+do+I+" + method)

    # if it's a Google question
    google_query_pattern = '((W|w)hat is ([^\?]*)|(W|w)hat are ([^\?]*)|(H|h)ow do I ([^\?]*))'
    other_queries = '(prep|tool|vegetarian|vegan|kosher|health|time|temperature|setting|heat|that)'
    query = re.match(google_query_pattern, user_input)
    if query:
        if re.search(other_queries, user_input):
            continue
        search = user_input.strip().replace(' ','+')
        url = 'https://google.com/search?q=' + search
        print('Here is what I found: ' + url)

    # if user wants to quit
    quit_pattern = '((Q|q)uit|(S|s)top)'
    query = re.match(quit_pattern, user_input)
    if query:
        print("Thanks for walking through the recipe with me. Goodbye!")
        break



ing_name = []
ing_quantity = []
ing_measurement = []
tools = []
cook_methods = []