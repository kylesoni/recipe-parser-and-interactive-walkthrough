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
        ing_words = ing.ingredient.split()
        for word in ing_words:
            if word in meat_to_vegetarian_words:
                meat_words.append(word)
                veggie = meat_to_vegetarian_words[word]
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

    return Recipe(new_ings, new_steps)

def meat_to_vegan(recipe):
    ing_list = recipe.ingredients

def make_kosher(recipe):
    ing_list = recipe.ingredients

meat_to_vegetarian_words = {
    "beef" : "beyond meat"
}

meat_to_vegan = {

}