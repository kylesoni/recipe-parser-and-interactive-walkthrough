import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

doc = spacy_model("In a large, oven-safe skillet, heat olive oil and butter over medium heat.")

for token in doc:
    print([child for child in token.children])