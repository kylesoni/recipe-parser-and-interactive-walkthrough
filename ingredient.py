import re
import copy

class Ingredient:

    def __init__(self, ingredient_info):
        
        if not isinstance(ingredient_info, str):
            raise(Exception("Expected ingredient information to be a string."))

        ingredient_words = ingredient_info.split()

        self.amount = str(0)
        self.get_amount(ingredient_info)
        self.unit = ""
        self.get_unit(ingredient_info)
        self.ingredient = ""
        self.get_ingredient(ingredient_info)
        self.prep = ""
        self.desc = ""
        self.get_prep_and_descriptor()

    def get_amount(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        amount_candidate = [ingredient_words[0], ingredient_words[1]]
        if not re.search('^[a-zA-Z,.?]+$', amount_candidate[0]):
            self.amount = amount_candidate[0]
            if not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]):
                self.amount += amount_candidate[1]
        elif not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]):
            self.amount = amount_candidate[1]

    def get_unit(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        unit_candidates = ingredient_words[1:]
        actual_units = []
        for can in unit_candidates:
            if can in common_units:
                actual_units.append(common_units[can])
        if len(actual_units) >= 1:
            self.unit = actual_units[0]
        else:
            self.unit = ""
    
    def get_ingredient(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        first = True
        for word in ingredient_words:
            if word not in self.amount and word not in common_units:
                if "(" not in word and ")" not in word:
                    if first:
                        self.ingredient = word
                        first = False
                    else:
                        self.ingredient += " " + word

    def get_prep_and_descriptor(self):
        prep_words = []
        desc_words = []
        ingredient_words = self.ingredient.split()
        actual_ingredient_words = copy.deepcopy(ingredient_words)

        for word in ingredient_words:
            if word in common_prep:
                prep_words.append(common_prep[word])
                actual_ingredient_words.remove(word)
            elif word in common_descriptor:
                desc_words.append(common_descriptor[word])
                actual_ingredient_words.remove(word)

        if len(prep_words) > 0:
            self.prep = prep_words[0]
        for i in range(1, len(prep_words)):
            self.prep += ", " + prep_words[i]

        if len(desc_words) > 0:
            self.desc = desc_words[0]
        for i in range(1, len(desc_words)):
            self.desc += ", " + desc_words[i]

        for i in range(len(actual_ingredient_words)):
            actual_ingredient_words[i] = re.sub(r'[,.!?@#$%^&*_~]', '', actual_ingredient_words[i])
        self.ingredient = ' '.join(actual_ingredient_words)
        
common_units = {
    'kg': 'kg',
    'lb.': 'lb',
    'g': 'g',
    'oz.': 'oz',
    'oz': 'oz',

    'inches': 'in',
    'in': 'in',
    
    'tsp': 'tsp',
    'tsp.': 'tsp',
    'teaspoon': 'tsp',
    'tbsp': 'Tbsp',
    'Tbsp': 'Tbsp',
    'Tbsp.': 'Tbsp',
    'tablespoons': 'Tbsp',
    
    'quarts': 'quarts',
    'quart' : 'quart',
    'cup' : 'cup',
    'cups' : 'cups',

    'sheet': 'sheet'
    }

common_prep = {
    'diced': 'diced',
    'diced,': 'diced',
    'cubed': 'cubed',
    'cubed,': 'cubed',
    'beaten': 'beaten',
    'beaten,': 'beaten',
    'peeled': 'peeled',
    'peeled,': 'peeled',
    'softened': 'softened',
    'softened,': 'softened',
    'chopped': 'chopped',
    'chopped, ': 'chopped'
}

common_descriptor = {
    'packed': 'packed',
    'all-purpose': 'all-purpose',
    'extra-virgin': 'extra-virgin',
    'large': 'large'
}


#test_ingredient = Ingredient("1 sheet nori seaweed, cut into squares")

#print(test_ingredient.ingredient)
#print(test_ingredient.amount)
#print(test_ingredient.unit)

