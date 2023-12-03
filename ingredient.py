import re
import copy
import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

class Ingredient:

    def __init__(self, ingredient_info):
        
        if not isinstance(ingredient_info, str):
            raise(Exception("Expected ingredient information to be a string."))
        
        self.raw = ingredient_info
        self.amount = str(0)
        self.amount_clar = ""
        self.get_amount(ingredient_info)
        self.unit = ""
        self.get_unit(ingredient_info)
        self.ingredient = ""
        self.get_ingredient(ingredient_info)
        self.prep = ""
        self.desc = ""
        self.tools = []
        self.get_prep_and_descriptor()

    def get_amount(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        amount_candidate = [ingredient_words[0], ingredient_words[1]]
        if not re.search('^[a-zA-Z,.?]+$', amount_candidate[0]) and "(" not in amount_candidate[0] and ")" not in amount_candidate[0]:
            self.amount = amount_candidate[0]
            if not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]) and "(" not in amount_candidate[1] and ")" not in amount_candidate[1]:
                self.amount += " " + amount_candidate[1]
        elif not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]) and "(" not in amount_candidate[1] and ")" not in amount_candidate[1]:
            self.amount = amount_candidate[1]
        if re.search("\(([^)]+)\)", ingredient_info):
            self.amount_clar = re.search("\(([^)]+)\)", ingredient_info).group(0)
        if "to taste" in ingredient_info:
            self.amount_clar = "to taste"

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
        ingredient_words = re.sub("\(([^)]+)\)", "", ingredient_info).split()
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
        prep_words = ""
        prep_candidates = []
        desc_words = []
        ingredient_words = self.ingredient.split()
        actual_ingredient_words = copy.deepcopy(ingredient_words)
        doc = spacy_model(self.ingredient)

        for word in ingredient_words:
            word = re.sub(r'[^\w\s]', '', word)
            if word in common_prep:
                for token in doc:
                    if token.text == word:
                        tracker = [token]
                        while len(tracker) > 0:
                            t = tracker.pop()
                            for child in t.children:
                                tracker.append(child)
                                if child.dep_ != "dobj" and child.pos_ != "VERB" and child.dep_ != "nsubj" and child.head.dep_ != "dobj":
                                    if child.text not in prep_candidates:
                                        prep_candidates.append(child.text)
                            if t.text not in prep_candidates:
                                prep_candidates.append(common_prep[token.text])
            else:
                for desc in list(common_descriptor.keys()):
                    if desc in self.raw:
                        if "not " + desc in self.raw:
                            if "not " + desc not in desc_words:
                                desc_words.append("not " + desc)
                            if "not" in actual_ingredient_words:
                                actual_ingredient_words.remove("not")
                            if desc in actual_ingredient_words:
                                actual_ingredient_words.remove(desc)
                        else:
                            if desc not in desc_words:
                                desc_words.append(desc)
                            if desc in actual_ingredient_words:
                                actual_ingredient_words.remove(desc)

        for word in ingredient_words:
            raw_word = re.sub(r'[,.!?@#$%^&*_~]', '', word)
            if raw_word in prep_candidates and raw_word != "or" and raw_word != "to" and raw_word != "taste":
                if prep_words == "":
                    prep_words = raw_word
                else:
                    prep_words += " " + raw_word
                if word in actual_ingredient_words:
                    actual_ingredient_words.remove(word)
                if word in prep_tools:
                    self.tools.append(prep_tools[word])
        self.prep = prep_words

        if "or" in actual_ingredient_words and "to" in actual_ingredient_words and "taste" in actual_ingredient_words:
            actual_ingredient_words.remove("or")

        if "to" in actual_ingredient_words and "taste" in actual_ingredient_words:
            actual_ingredient_words.remove("to")
            actual_ingredient_words.remove("taste")

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
    'lb': 'lb',
    'lbs': 'lb',
    'pound': 'pound',
    'pounds': 'pounds',
    'g': 'g',
    'gram': 'g',
    'grams': 'g',
    'oz.': 'oz',
    'oz': 'oz',
    'ounce': 'oz',
    'ounces': 'oz',

    'L' : 'L',
    'l' : 'L',
    'liter' : 'L',
    'liters' : 'L',

    'inches': 'in',
    'in': 'in',
    
    'tsp': 'tsp',
    'tsp.': 'tsp',
    'teaspoon': 'tsp',
    'teaspoons': 'tsp',
    'tbsp': 'Tbsp',
    'Tbsp': 'Tbsp',
    'Tbsp.': 'Tbsp',
    'tablespoons': 'Tbsp',
    'tablespoon': 'Tbsp',
    
    'quarts': 'quarts',
    'quart' : 'quart',
    'qt' : 'qt',
    'qts' : 'qt',
    'cup' : 'cup',
    'cups' : 'cups',
    'gallon' : 'gal',
    'gal' : 'gal',
    'gallons' : 'gal',
    'gals' : 'gal',
    'pint' : 'pint',
    'pt' : 'pint',
    'pts' : 'pints',
    'pints' : 'pint',

    'sheet': 'sheet',
    'package': 'package',
    'clove': 'clove',
    'cloves': 'cloves',
    'bottle': 'bottle',
    'bottles': 'bottle',
    'pinch' : 'pinch',
    'pinches' : 'pinch',
    'dash' : 'dash',
    'dashes' : 'dashes',
    'slice' : 'slice',
    'slices' : 'slice',
    'bushel': 'bushel',
    'bushels': 'bushel',
    'carton': 'carton',
    'cartons': 'carton',
    'can': 'can',
    'cans': 'can',
    'jar': 'jar',
    'jars': 'jar',
    'stalk': 'stalk',
    'stalks': 'stalk',

    'to taste' : 'to taste'
    }

common_prep = {
    'diced': 'diced',
    'cubed': 'cubed',
    'beaten': 'beaten',
    'peeled': 'peeled',
    'softened': 'softened',
    'chopped': 'chopped',
    'cut' : 'cut',
    'sliced' : 'sliced',
    'minced' : 'minced',
    'grated' : 'grated',
    "braised" : "braised",
    "brewed" : "brewed",
    "boiled" : "boiled",
    "broiled" : "broiled",
    "browned" : "browned",
    "caramelized" : "caramelized",
    "chopped" : "chopped",
    "pulverized" : "pulverized",
    "whipped" : "whipped",
    "pitted" : "pitted"
}

common_descriptor = {
    'all-purpose': 'all-purpose',
    'extra-virgin': 'extra-virgin',
    'large': 'large',
    'small': 'small',
    'boneless' : 'boneless',
    'skinless' : 'skinless',
    'drained' : 'drained',
    'lean' : 'lean',

    "acidic" : "acidic",
    "acrid" : "acrid",
    "airy" : "airy",
    "a la carte" : "a la carte",
    "a la king" : "a la king",
    "a la mode" : "a la mode",
    "alcoholic" : "alcoholic",
    "al dente" : "al dente",
    "almond flavored" : "almond flavored",
    "ambrosial" : "ambrosial",
    "appetizing" : "appetizing",
    "aroma" : "aroma",
    "aromatic" : "aromatic",
    "au fromage" : "au fromage",
    "au gratin" : "au gratin",
    "au jus" : "au jus",
    "balsamic" : "balsamic",
    "barbecue" : "barbecue",
    "battered" : "battered",
    "bite-size" : "bite-size",
    "biting" : "biting",
    "bitter" : "bitter",
    "blackened" : "blackened",
    "blah" : "blah",
    "blanched" : "blanched",
    "bland" : "bland",
    "blended" : "blended",
    "bold" : "bold",
    "boned" : "boned",
    "brackish" : "brackish",
    "briny" : "briny",
    "brittle" : "brittle",
    "bubbly" : "bubbly",
    "burning" : "burning",
    "bursting" : "bursting",
    "butterflied" : "butterflied",
    "cacciatore" : "cacciatore",
    "cakey" : "cakey",
    "candied" : "candied",
    "canned" : "canned",
    "caustic" : "caustic",
    "chalky" : "chalky",
    "charcuterie" : "charcuterie",
    "charred" : "charred",
    "cheesy" : "cheesy",
    "chewy" : "chewy",
    "chilled" : "chilled",
    "chipotle" : "chipotle",
    "chocolaty" : "chocolaty",
    "chowder" : "chowder",
    "clarified" : "clarified",
    "classical" : "classical",
    "condensed" : "condensed",
    "condiment" : "condiment",
    "course" : "course",
    "creamed" : "creamed",
    "creamery" : "creamery",
    "creamy" : "creamy",
    "creole" : "creole",
    "crisscrossed" : "crisscrossed",
    "crispy" : "crispy",
    "crumbly" : "crumbly",
    "crunchy" : "crunchy",
    "crusty" : "crusty",
    "crystalized" : "crystalized",
    "cuisine" : "cuisine",
    "curd" : "curd",
    "curdled" : "curdled",
    "cured" : "cured",
    "curried" : "curried",
    "dash" : "dash",
    "decadent" : "decadent",
    "deglaze" : "deglaze",
    "dehyrated" : "dehyrated",
    "delectable" : "delectable",
    "delicious" : "delicious",
    "delightful" : "delightful",
    "dense" : "dense",
    "devein" : "devein",
    "deviled" : "deviled",
    "dietary" : "dietary",
    "diluted" : "diluted",
    "dipping" : "dipping",
    "disagreeable" : "disagreeable",
    "disgusting" : "disgusting",
    "distasteful" : "distasteful",
    "distinctive" : "distinctive",
    "divine" : "divine",
    "doughy" : "doughy",
    "dredged" : "dredged",
    "drenched" : "drenched",
    "dripping" : "dripping",
    "dried out" : "dried out",
    "drizzled" : "drizzled",
    "dry" : "dry",
    "dull" : "dull",
    "dusted" : "dusted",
    "earthy" : "earthy",
    "eatable" : "eatable",
    "edible" : "edible",
    "enjoyable" : "enjoyable",
    "enticing" : "enticing",
    "entrée" : "entrée",
    "escalloped" : "escalloped",
    "etouffee" : "etouffee",
    "evaporated" : "evaporated",
    "exquisite" : "exquisite",
    "fatty" : "fatty",
    "fermented" : "fermented",
    "fine" : "fine",
    "finger licking good" : "finger licking good",
    "fibrous" : "fibrous",
    "filled" : "filled",
    "filling" : "filling",
    "fiery" : "fiery",
    "fishy" : "fishy",
    "fizzy" : "fizzy",
    "flakey" : "flakey",
    "flambé" : "flambé",
    "flavorless" : "flavorless",
    "flavorful" : "flavorful",
    "flavorsome" : "flavorsome",
    "florentine" : "florentine",
    "floury" : "floury",
    "fluffy" : "fluffy",
    "foie gras" : "foie gras",
    "folded" : "folded",
    "fondant" : "fondant",
    "foul" : "foul",
    "fra diablo" : "fra diablo",
    "fragrant" : "fragrant",
    "feathery" : "feathery",
    "fresh" : "fresh",
    "fricasseed" : "fricasseed",
    "fried" : "fried",
    "frosty" : "frosty",
    "frozen" : "frozen",
    "fruity" : "fruity",
    "fudgy" : "fudgy",
    "full-bodied" : "full-bodied",
    "full-flavored" : "full-flavored",
    "gamy" : "gamy",
    "garlicky" : "garlicky",
    "garnish" : "garnish",
    "gastric" : "gastric",
    "gingery" : "gingery",
    "glazed" : "glazed",
    "glopy" : "glopy",
    "glossy" : "glossy",
    "gluteny" : "gluteny",
    "golden" : "golden",
    "good" : "good",
    "gooey" : "gooey",
    "gourmet" : "gourmet",
    "grainy" : "grainy",
    "granulated" : "granulated",
    "grated" : "grated",
    "gratifying" : "gratifying",
    "greasy" : "greasy",
    "griddled" : "griddled",
    "grilled" : "grilled",
    "gritty" : "gritty",
    "gross" : "gross",
    "hardboiled" : "hardboiled",
    "heady" : "heady",
    "heat" : "heat",
    "heavy" : "heavy",
    "healthy" : "healthy",
    "hearty" : "hearty",
    "heavenly" : "heavenly",
    "herbaceous" : "herbaceous",
    "hint" : "hint",
    "homogenized" : "homogenized",
    "honeyed" : "honeyed",
    "hors d’oeuvre" : "hors d’oeuvre",
    "hot" : "hot",
    "hot sauce" : "hot sauce",
    "icy" : "icy",
    "infused" : "infused",
    "intense" : "intense",
    "inviting" : "inviting",
    "jiggly" : "jiggly",
    "juicy" : "juicy",
    "julienne" : "julienne",
    "kick" : "kick",
    "kneaded" : "kneaded",
    "kosher" : "kosher",
    "laced" : "laced",
    "laden" : "laden",
    "laiche" : "laiche",
    "layered" : "layered",
    "lemony" : "lemony",
    "light" : "light",
    "limp" : "limp",
    "lip-smacking" : "lip-smacking",
    "liquid" : "liquid",
    "low-fat" : "low-fat",
    "lumpy" : "lumpy",
    "luscious" : "luscious",
    "lusty" : "lusty",
    "lyonnaise" : "lyonnaise",
    "malodorous" : "malodorous",
    "malted" : "malted",
    "marinate" : "marinate",
    "marvelous" : "marvelous",
    "mashed" : "mashed",
    "mealy" : "mealy",
    "medium" : "medium",
    "mellow" : "mellow",
    "melting" : "melting",
    "messy" : "messy",
    "microwave" : "microwave",
    "mild" : "mild",
    "milky" : "milky",
    "minced" : "minced",
    "minty" : "minty",
    "mixed" : "mixed",
    "mixture" : "mixture",
    "moist" : "moist",
    "moldy" : "moldy",
    "morsel" : "morsel",
    "mouth-watering" : "mouth-watering",
    "muddy" : "muddy",
    "mushy" : "mushy",
    "nasty" : "nasty",
    "natural" : "natural",
    "nauseating" : "nauseating",
    "nectarous" : "nectarous",
    "nosey" : "nosey",
    "nourishing" : "nourishing",
    "noxious" : "noxious",
    "nuked" : "nuked",
    "nutriment" : "nutriment",
    "nutritious" : "nutritious",
    "nutty" : "nutty",
    "odoriferous" : "odoriferous",
    "odorless" : "odorless",
    "orgasmically-delicious" : "orgasmically-delicious",
    "oily" : "oily",
    "oniony" : "oniony",
    "oozing" : "oozing",
    "organic" : "organic",
    "overpowering" : "overpowering",
    "packed" : "packed",
    "palatable" : "palatable",
    "parboiled" : "parboiled",
    "parched" : "parched",
    "parfait" : "parfait",
    "pasteurized" : "pasteurized",
    "pasty" : "pasty",
    "pâté" : "pâté",
    "peanut butter" : "peanut butter",
    "peck" : "peck",
    "penetrating" : "penetrating",
    "peppered" : "peppered",
    "peppery" : "peppery",
    "perfumed" : "perfumed",
    "perishable" : "perishable",
    "piccata" : "piccata",
    "pickled" : "pickled",
    "piping" : "piping",
    "piquant" : "piquant",
    "pleasant" : "pleasant",
    "plump" : "plump",
    "powdered" : "powdered",
    "powdery" : "powdery",
    "potent" : "potent",
    "pouched" : "pouched",
    "preserved" : "preserved",
    "puffy" : "puffy",
    "pulp" : "pulp",
    "pungent" : "pungent",
    "puréed" : "puréed",
    "ragout" : "ragout",
    "rancid" : "rancid",
    "rank" : "rank",
    "rare" : "rare",
    "raw" : "raw",
    "redolent" : "redolent",
    "reduced" : "reduced",
    "reeking" : "reeking",
    "refrigerated" : "refrigerated",
    "refreshing" : "refreshing",
    "relish" : "relish",
    "rich" : "rich",
    "rib sticking" : "rib sticking",
    "ripe" : "ripe",
    "roasted" : "roasted",
    "robust" : "robust",
    "rolled" : "rolled",
    "rotten" : "rotten",
    "roux" : "roux",
    "ruined" : "ruined",
    "runny" : "runny",
    "saline" : "saline",
    "salted" : "salted",
    "salty" : "salty",
    "saturated" : "saturated",
    "sapid" : "sapid",
    "saporous" : "saporous",
    "sauté" : "sauté",
    "savory" : "savory",
    "scalded" : "scalded",
    "scented" : "scented",
    "scorched" : "scorched",
    "scrambled" : "scrambled",
    "scrumptious" : "scrumptious",
    "seared" : "seared",
    "seasoned" : "seasoned",
    "sharp" : "sharp",
    "shredded" : "shredded",
    "sizzling" : "sizzling",
    "simmering" : "simmering",
    "skimmed" : "skimmed",
    "skunky" : "skunky",
    "slathered" : "slathered",
    "slimy" : "slimy",
    "slippery" : "slippery",
    "slivered" : "slivered",
    "smelly" : "smelly",
    "smokey" : "smokey",
    "smooth" : "smooth",
    "smothered" : "smothered",
    "snappy" : "snappy",
    "snappy" : "snappy",
    "soaked" : "soaked",
    "sodden" : "sodden",
    "soft" : "soft",
    "soft-boiled" : "soft-boiled",
    "soggy" : "soggy",
    "solid" : "solid",
    "solidify" : "solidify",
    "sordid" : "sordid",
    "soufflé" : "soufflé",
    "soupy" : "soupy",
    "sparkling" : "sparkling",
    "spicy" : "spicy",
    "spirited" : "spirited",
    "spoiled" : "spoiled",
    "spongy" : "spongy",
    "spread" : "spread",
    "sprinkled" : "sprinkled",
    "spritzed" : "spritzed",
    "stale" : "stale",
    "starchy" : "starchy",
    "steamy" : "steamy",
    "stewed" : "stewed",
    "sticky" : "sticky",
    "stiff" : "stiff",
    "stinging" : "stinging",
    "stringy" : "stringy",
    "stinky" : "stinky",
    "strong" : "strong",
    "stuffed" : "stuffed",
    "subdued" : "subdued",
    "succulent" : "succulent",
    "sunnyside up" : "sunnyside up",
    "sugar-coated" : "sugar-coated",
    "sugary" : "sugary",
    "syrupy" : "syrupy",
    "tainted" : "tainted",
    "tangy" : "tangy",
    "tantalizing" : "tantalizing",
    "tart" : "tart",
    "tasteless" : "tasteless",
    "tasty" : "tasty",
    "tempting" : "tempting",
    "tender" : "tender",
    "tepid" : "tepid",
    "texture" : "texture",
    "thick" : "thick",
    "titillating" : "titillating",
    "toasted" : "toasted",
    "toothsome" : "toothsome",
    "tough" : "tough",
    "tumaceous" : "tumaceous",
    "umami" : "umami",
    "unsavory" : "unsavory",
    "vanilla" : "vanilla",
    "velvety" : "velvety",
    "viscous" : "viscous",
    "vinegary" : "vinegary",
    "warm" : "warm",
    "watery" : "watery",
    "well-done" : "well-done",
    "wet" : "wet",
    "whey" : "whey",
    "wholesome" : "wholesome",
    "wild" : "wild",
    "wilted" : "wilted",
    "wrapped" : "wrapped",
    "yucky" : "yucky",
    "yummy" : "yummy",
    "zest" : "zest",
    "zestful" : "zestful",
    "zesty" : "zesty",
    "zippy" : "zippy",
}

prep_tools = {
    'diced': 'knife',
    'cubed': 'knife',
    'beaten': 'fork or whisk',
    'peeled': 'peeler',
    'chopped': 'knife',
    'cut' : 'knife',
    'sliced' : 'knife',
    'minced' : 'knife',
    'grated' : 'cheese grater'
}