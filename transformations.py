from ingredient import Ingredient
from step import Step
from recipe import Recipe
import re

def meat_to_vegetarian(recipe):
    new_ings = []
    meat_words = []
    ing_list = recipe.ingredients
    for ing in ing_list:
        veggie = ""
        ing_words = ing.ingredient.lower().split()
        for word in ing_words:
            if word in meat_to_vegetarian_words:
                meat_words.append(word)
                veggie = meat_to_vegetarian_words[word]
                print("Changing: " + word + " -> " + veggie)
        if veggie != "":
            new_ings.append(ing.amount + " " + ing.unit + " " + veggie)
        else:
            new_ings.append(ing.raw)
    new_steps = []
    step_list = recipe.steps
    for step in step_list:
        new_text = step.text
        for word in meat_words:
            if word in new_text:
                new_text = re.sub(word, meat_to_vegetarian_words[word], new_text)
        new_steps.append(new_text)
    print("")
    return Recipe(new_ings, new_steps)

def meat_to_vegan(recipe):
    new_ings = []
    meat_words = []
    ing_list = recipe.ingredients
    for ing in ing_list:
        veggie = ""
        ing_words = ing.ingredient.lower().split()
        for word in ing_words:
            if word in meat_to_vegan_words:
                if word == "cheese":
                    found = False
                    for new_word in ing_words:
                        if new_word in cheeses and not found:
                            meat_words.append(new_word)
                            veggie = cheeses[new_word]
                            found = True
                            print("Changing: " + new_word + " -> " + veggie)
                    if not found:
                        meat_words.append(word)
                        veggie = meat_to_vegan_words[word]
                else:
                    meat_words.append(word)
                    veggie = meat_to_vegan_words[word]
                print("Changing: " + word + " -> " + veggie)
        if veggie != "":
            new_ings.append(ing.amount + " " + ing.unit + " " + veggie)
        else:
            new_ings.append(ing.raw)
    new_steps = []
    step_list = recipe.steps
    for step in step_list:
        new_text = step.text
        for word in meat_words:
            if word in new_text:
                new_text = re.sub(word, meat_to_vegan_words[word], new_text)
        new_steps.append(new_text)
    print("")
    return Recipe(new_ings, new_steps)

def make_kosher(recipe):
    new_ings = []
    un_kosher = []
    ing_list = recipe.ingredients
    for ing in ing_list:
        kosh = ""
        ing_words = ing.ingredient.lower().split()
        for word in ing_words:
            if word in make_kosher_words:
                un_kosher.append(word)
                kosh = make_kosher_words[word]
                print("Changing: " + word + " -> " + kosh)
        if kosh != "":
            new_ings.append(ing.amount + " " + ing.unit + " " + kosh)
        else:
            new_ings.append(ing.raw)
    new_steps = []
    step_list = recipe.steps
    for step in step_list:
        new_text = step.text
        for word in un_kosher:
            if word in new_text:
                new_text = re.sub(word, make_kosher_words[word], new_text)
        new_steps.append(new_text)
    print("")
    return Recipe(new_ings, new_steps)

def make_healthy(recipe):
    new_ings = []
    un_healthy = []
    ing_list = recipe.ingredients
    for ing in ing_list:
        health = ""
        ing_words = ing.ingredient.lower().split()
        for word in ing_words:
            if word in make_healthy_words:
                un_healthy.append(word)
                health = make_healthy_words[word]
                print("Changing: " + word + " -> " + health)
        if health != "":
            new_ings.append(ing.amount + " " + ing.unit + " " + health)
        else:
            new_ings.append(ing.raw)
    new_steps = []
    step_list = recipe.steps
    for step in step_list:
        new_text = step.text
        for word in un_healthy:
            if word in new_text:
                new_text = re.sub(word, make_healthy_words[word], new_text)
        new_steps.append(new_text)
    print("")
    return Recipe(new_ings, new_steps)


meat_to_vegetarian_words = {
    "beef" : "beyond meat",
    "steak" : "tofu",
    "veal" : "tofu",

    "pork" : "tofu",
    "bacon" : "tofu",
    "sausage" : "tofu",
    "ham" : "tofu", 

    "chicken" : "tofu",
    "duck" : "tofu",
    "turkey" : "tofu",
    "quail" : "tofu",

    "salami" : "tofu",
    "pastrami" : "tofu",

    "broth" : "vegetable broth",

    "stock" : "vegetable stock",

    "oil" : "vegetable oil",

    "fish" : "tofu",
    "shark" : "tofu",
    "sharkfin" : "tofu",
    "catfish" : "tofu",
    "tilapia" : "tofu",
    "salmon" : "tofu",
    "halibut" : "tofu",
    "bass" : "tofu",
    "carp" : "tofu",
    "mahi-mahi" : "tofu",
    "perch" : "tofu",
    "flounder" : "tofu",
    "snapper" : "tofu",
    "sturgeon" : "tofu",
    "sardines" : "tofu",
    "anchovies" : "tofu",
    "mackerel" : "tofu",
    "cod" : "tofu",
    "herring" : "tofu",
    "trout" : "tofu",
    "tuna" : "tofu",

    "crab" : "imitation crab",
    "shrimp" : "shitake mushrooms",
    "oysters" : "mushrooms",
    "clam" : "mushrooms",
    "mussel" : "mushrooms",
    "crawdad" : "mushrooms",
    "scallop" : "mushrooms",
    "lobster" : "mushrooms",
}

meat_to_vegan_words = {
    "beef" : "beyond meat",
    "steak" : "tofu",
    "veal" : "tofu",

    "pork" : "tofu",
    "bacon" : "tofu",
    "sausage" : "tofu",
    "ham" : "tofu", 

    "chicken" : "tofu",
    "duck" : "tofu",
    "turkey" : "tofu",
    "quail" : "tofu",

    "salami" : "tofu",
    "pastrami" : "tofu",

    "broth" : "vegetable broth",

    "stock" : "vegetable stock",

    "oil" : "vegetable oil",

    "fish" : "tofu",
    "shark" : "tofu",
    "sharkfin" : "tofu",
    "catfish" : "tofu",
    "tilapia" : "tofu",
    "salmon" : "tofu",
    "halibut" : "tofu",
    "bass" : "tofu",
    "carp" : "tofu",
    "mahi-mahi" : "tofu",
    "perch" : "tofu",
    "flounder" : "tofu",
    "snapper" : "tofu",
    "sturgeon" : "tofu",
    "sardines" : "tofu",
    "anchovies" : "tofu",
    "mackerel" : "tofu",
    "cod" : "tofu",
    "herring" : "tofu",
    "trout" : "tofu",
    "tuna" : "tofu",

    "crab" : "imitation crab",
    "shrimp" : "shitake mushrooms",
    "oysters" : "mushrooms",
    "clam" : "mushrooms",
    "mussel" : "mushrooms",
    "crawdad" : "mushrooms",
    "scallop" : "mushrooms",
    "lobster" : "mushrooms",

    "milk" : "almond milk",
    "butter" : "margarine",
    "egg" : "vegan egg",
    "eggs" : "vegan eggs",
    
    "cream" : "vegan cream",
    "yogurt" : "vegan yogurt",
    "greek yogurt" : "vegan yogurt",

    "cheese" : "vegan cheese",
    "ice cream" : "sorbetto",
    "custard" : "vegan custard"
}

cheeses = {
    "cheddar" : "vegan cheese",
    "gouda" : "vegan cheese",
    "mozzarella" : "vegan cheese",
    "parmesan" : "nutritional yeast",
    "swiss" : "nutritional yeast"
}

make_kosher_words = {
    "butter" : "margarine",
    "chocolate" : "carob",
    "frosting" : "marshmallow fluff",
    "yogurt" : "vegan yogurt",
    "cream" : "coconut milk",
    "milk" : "almond milk",

    "sirloin" : "beyond meat",
    "flank" : "beyond meat",
    "round" : "beyond meat",
    "rump cap" : "beyond meat",
    "shank" : "beyond meat",

    "pork" : "tofu",
    "bacon" : "tofu",
    "sausage" : "tofu",
    "ham" : "tofu", 

    "crab" : "imitation crab",
    "shrimp" : "shitake mushrooms",
    "oysters" : "mushrooms",
    "clam" : "mushrooms",
    "mussel" : "mushrooms",
    "crawdad" : "mushrooms",
    "scallop" : "mushrooms",
    "lobster" : "mushrooms",

    "crickets" : "mushrooms",
    "grasshoppers" : "mushrooms",
    "eagles" : "tofu", 
    "owls" : "tofu", 
    "hawks" : "tofu",
    "gulls" : "tofu"
}

make_healthy_words = {
    "beef" : "tofu",
    "steak" : "tofu",
    "veal" : "tofu",

    "pork" : "tofu",
    "bacon" : "tofu",
    "sausage" : "tofu",
    "ham" : "tofu",

    "oil" : "avocado oil",
    "fat" : "avocado oil",
    "butter" : "mashed avocado",

    "broth" : "vegetable broth",

    "milk" : "skim milk",
    "cheese" : "nutritional yeast",

    "sugar" : "stevia",
    
    "refried" : "black beans",

    "potato" : "sweet potato",
}