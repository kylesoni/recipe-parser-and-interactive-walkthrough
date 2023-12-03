import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

doc = spacy_model("Bake in the preheated oven until topping is lightly browned, about 30 minutes.")

for token in doc:
    if token.text == "topping":
        print([child for child in token.children])
    # print([child for child in token.children])