
class Ingredient:

    def __init__(self, ingredient_info):
        
        if not isinstance(ingredient_info, str):
            raise(Exception("Expected ingredient information to be a string."))

        ingredient_words = ingredient_info.split()
        
        if len(ingredient_words) > 2:
            self.ingredient = ingredient_words[2]
        else:
            self.ingredient = ingredient_words[1]
        for i in range(3, len(ingredient_words)):
            self.ingredient += " " + ingredient_words[i]

        self.amount = ingredient_info[0]
        self.unit = ingredient_words[1]

test_ingredient = Ingredient("1 sheet nori seaweed, cut into squares")

#print(test_ingredient.ingredient)
#print(test_ingredient.amount)
#print(test_ingredient.unit)

