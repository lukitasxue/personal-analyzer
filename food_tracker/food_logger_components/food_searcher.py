import os
import pandas as pd
import spacy
import requests

nlp = spacy.load("en_core_web_sm")
API_KEY = "my_api"
csv_file = "food_log.csv"

# Step 1: Ask for Meal Type
def select_meal():
    meal_options = ["Breakfast", "Lunch", "Dinner", "Snack"]
    
    print("\n🍽️ Select the meal you want to log:")
    for i, meal in enumerate(meal_options, 1):
        print(f"{i}. {meal}")

    choice = int(input("\nEnter the number of the meal (1-4): ")) - 1
    return meal_options[choice] if 0 <= choice < len(meal_options) else None

# Step 2: Ask if the user ate something during that meal
def confirm_meal_entry(meal_type):
    response = input(f"\nDid you eat anything for {meal_type}? (yes/no): ").strip().lower()
    return response == "yes"

# Step 3: NLP to Extract Multiple Foods
def extract_food_items(food_sentence):
    doc = nlp(food_sentence.lower())

    food_items = []
    current_food = []

    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:
            current_food.append(token.lemma_)
        elif token.text in [",", "and"]:
            if current_food:
                food_items.append(" ".join(current_food))
                current_food = []

    if current_food:
        food_items.append(" ".join(current_food))

    return food_items

# Step 4: Search USDA API for Each Food Item
def search_food_api(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&pageSize=3&dataType=Branded,Survey%20(FNDDS)&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("foods", [])

# Step 5: Let User Select the Best Food Match
def select_food_from_results(food_results, food_name):
    while True:
        print(f"\n✅ Food options found for '{food_name}':")
        
        for i, food in enumerate(food_results[:5]):
            print(f"{i + 1}. {food['description']}")

        print("\n(R) Retry with a new search")
        print("(B) Go back and skip this food")

        choice = input("\nEnter the number of the food you want to select (1-5), 'R' to retry, or 'B' to go back: ").strip().lower()

        if choice == "r":
            new_query = input("\n🔍 Enter a new food name to search: ").strip()
            new_results = search_food_api(new_query)
            if new_results:
                food_results = new_results  # Update with new results
                continue
            else:
                print("❌ No new results found. Try again.")
                continue
        
        elif choice == "b":
            print(f"🔙 Skipping '{food_name}'.")
            return None

        elif choice.isdigit() and 1 <= int(choice) <= len(food_results):
            return food_results[int(choice) - 1]

        else:
            print("❌ Invalid choice. Please try again.")


# Step 6: Log All Foods as a Single Meal in CSV
def log_meal_to_csv(meal_type, meal_name, selected_foods=None):
    columns = ["Date", "Meal Type", "Meal Description", "Food Items", "Total Calories"]

    # Ensure CSV exists
    if not os.path.exists(csv_file):
        print("⚠️ CSV file not found. Creating a new one...")
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_file, index=False)

    # Read existing CSV
    df = pd.read_csv(csv_file)

    if selected_foods:
        # Combine selected foods into one meal
        meal_foods = ", ".join([food["description"] for food in selected_foods])
        total_calories = sum(food.get("foodNutrients", [{}])[0].get("value", 0) for food in selected_foods)
    else:
        # If no food was eaten, log "N/A"
        meal_foods = "N/A"
        total_calories = 0

    # Append new meal entry
    new_entry = pd.DataFrame([[pd.Timestamp.today().strftime("%Y-%m-%d"), meal_type, meal_name, meal_foods, total_calories]], columns=columns)
    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(csv_file, index=False)
    print(f"✅ {meal_type} logged successfully!")


# Step 7: Full Food Logging System with Meal Selection
def food_tracking():
    meal_type = select_meal()
    
    if not meal_type:
        print("❌ Invalid meal selection. Exiting...")
        return

    if not confirm_meal_entry(meal_type):
        print(f"❌ No food logged for {meal_type}. Marking as 'N/A'...")
        log_meal_to_csv(meal_type, "N/A", None)  # Log as "N/A"
        return

    user_input = input(f"🍛 Enter everything you ate for {meal_type} in one sentence: ")
    detected_foods = extract_food_items(user_input)
    selected_foods = []

    for food_name in detected_foods:
        food_results = search_food_api(food_name)

        if food_results:
            selected_food = select_food_from_results(food_results, food_name)
            if selected_food:
                selected_foods.append(selected_food)
        else:
            print(f"❌ No results found for '{food_name}'. Skipping...")

    if selected_foods:
        log_meal_to_csv(meal_type, user_input, selected_foods)
    else:
        print(f"❌ No valid food selected for {meal_type}. Marking as 'N/A'.")
        log_meal_to_csv(meal_type, user_input, None)


# Run the program
food_tracking()