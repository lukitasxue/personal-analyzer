import pandas as pd
import os

csv_file = "schedule_log.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Date", "Time", "Event Name", "Category"])
    df.to_csv(csv_file, index=False)

def log_event():
    """Logs a new schedule event"""
    date = input("Enter event date (YYYY-MM-DD): ")
    time = input("Enter event time (HH:MM AM/PM): ")
    event_name = input("Enter event name: ")
    category = input("Enter category (Work, Study, Personal, etc.): ")

    new_entry = pd.DataFrame([[date, time, event_name, category]], columns=["Date", "Time", "Event Name", "Category"])

    new_entry.to_csv(csv_file, mode='a', header=False, index= False)
    print("\nEvent logged succesfully")

log_event()