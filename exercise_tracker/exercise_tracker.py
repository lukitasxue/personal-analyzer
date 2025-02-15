import os
import pandas as pd
import datetime

exercise_db = "exercise_tracker/exercise_database.csv"
exercise_db = pd.read_csv(exercise_db)

log_file = "exercise_log.csv"

if not os.path.exists(log_file):
    columns = ["Date", "Exercise Name", "Type", "Duration (mins)", "Repetitions", "Calories Burned"]
    log_df = pd.DataFrame(columns=columns)
    log_df.to_csv(log_file, index=False)


def select_exercise():
    print("\n Select an exercise")
    for i, exercise in enumerate(exercise_db["Exercise Name"], 1):
        print(f"{i}. {exercise}")

    while True:
        try: 
            choice = int(input("\nEnter the number of the exercise: ")) -1 
            if 0<= choice < len(exercise_db):
                return exercise_db.iloc[choice]
            else:
                print("X invalid selection. Please Try Again")
            
        except ValueError:
            print("Enter a valid number")

def log_exercise():
    exercise_data = select_exercise()
    exercise_name = exercise_data["Exercise Name"]
    exercise_type = exercise_data["Type"]

    duration = 0
    repetitions = 0
    calories = 0

    if exercise_type == "Time":
        duration = int(input(f"Enter duration of {exercise_name} in minutes: "))
        calories = duration * float(exercise_data["Calories per Min"])
    elif exercise_type == "Rep":
        repetitions = int(input(f"Enter number of repetitions for {exercise_name}: "))
        calories = repetitions * float(exercise_data["Calories per Rep"])
    else:
        print("X Invalid exercise type detected. Logging skipped.")
        return


    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
            log_df = pd.read_csv(log_file)
    else:
        log_df = pd.DataFrame(columns=["Date", "Exercise Name", "Type", "Duration (mins)", "Repetitions", "Calories Burned"])

    # Append new log entry
    new_entry = pd.DataFrame([[datetime.date.today(), exercise_name, exercise_type, duration, repetitions, calories]],
                            columns=log_df.columns)

    log_df = pd.concat([log_df, new_entry], ignore_index=True)
    log_df.to_csv(log_file, index=False)

    print("Logged succesfully")

log_exercise()