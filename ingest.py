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

def load_students_csv(file_name):
    """Reads a CSV file of students and returns a dictionary of student data."""
    student_rec = {}

    with open(file_name, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            student_id = row["student_id"]
            
            for key in ["quiz1", "quiz2", "quiz3", "quiz4", "quiz5", "midterm", "final", "attendance_percent"]:
                row[key] = float(row[key]) if row[key] else 0.0

            student_rec[student_id] = row

    return student_rec

