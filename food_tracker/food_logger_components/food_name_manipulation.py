import spacy


nlp = spacy.load("en_core_web_sm")

def extract_food_items(food_sentence):
    doc = nlp(food_sentence.lower())

    food_items = []
    current_food = []

    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:  # Keep only food-related words
            current_food.append(token.lemma_)  # Lemmatize words
        elif token.text in [",", "and"]:  # Separator found, store previous food
            if current_food:
                food_items.append(" ".join(current_food))
                current_food = []

    if current_food:  # Add last item if any
        food_items.append(" ".join(current_food))

    return food_items

sentence = "Rice with grilled chicken and broccoli"
detected_foods = extract_food_items(sentence)
print("✅ Detected Food Items:", detected_foods)
