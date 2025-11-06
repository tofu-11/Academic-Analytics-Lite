from pathlib import Path
import csv
import json

with open("config.json", "r") as f:
    config = json.load(f)

base_dir = Path.cwd()
data_dir = base_dir / config["data_dir"]
data_dir.mkdir(exist_ok=True)

file_list = []
i = 0
folder = Path(data_dir)
for file in folder.iterdir():
    file_list[i] = file
    i += 1

def return_list():
    return file_list

def list_files():
    i = 1
    for file in folder.iterdir():
        print(i, ". ", file.name)

import csv

def load_students_csv(file_name):
    """Reads a CSV file of students and returns a dictionary grouped by section."""
    student_rec = {}

    with open(file_name, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Clean and trim names and section
            row["last_name"] = row["last_name"].strip()
            row["first_name"] = row["first_name"].strip()
            row["section"] = row["section"].strip()

            section = row["section"]
            student_id = row["student_id"].strip()

            # Convert numeric fields to floats or None
            for key in ["quiz1", "quiz2", "quiz3", "quiz4", "quiz5", "midterm", "final", "attendance_percent"]:
                value = row.get(key, "").strip()
                
                if value == "":
                    row[key] = None
                else:
                    try:
                        score = float(value)
                        # Clamp scores between 0 and 100
                        if 0 <= score <= 100:
                            row[key] = score
                        else:
                            row[key] = None
                    except ValueError:
                        row[key] = None

            # Create section key if not exists
            if section not in student_rec:
                student_rec[section] = {}

            # Add student to the section
            student_rec[section][student_id] = row

    return student_rec


