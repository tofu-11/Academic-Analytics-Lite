from pathlib import Path
import csv
import json

with open("config.json", "r") as f:
    config = json.load(f)

base_dir = Path.cwd()
data_dir = base_dir / config["data_dir"]
data_dir.mkdir(exist_ok=True)

file_list = []
folder = Path(data_dir)
for file in folder.iterdir():
    # Only add CSV files to the list
    if file.is_file() and file.suffix.lower() == '.csv':
        file_list.append(file)

def list_files():
    i = 1
    for file in folder.iterdir():
        # Only list CSV files
        if file.is_file() and file.suffix.lower() == '.csv':
            print(i, ". ", file.name)
            i += 1

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
            # Map the CSV column names to our standardized keys
            field_mapping = {
                "quiz1": "quiz_1", "quiz2": "quiz_2", "quiz3": "quiz_3", 
                "quiz4": "quiz_4", "quiz5": "quiz_5",
                "midterm": "midterm", "final": "final_exam",
                "attendance_percent": "attendance"
            }
            
            for csv_key, internal_key in field_mapping.items():
                value = row.get(csv_key, "").strip()
                
                if value == "":
                    row[internal_key] = None
                else:
                    try:
                        score = float(value)
                        # Clamp scores between 0 and 100
                        if 0 <= score <= 100:
                            row[internal_key] = score
                        else:
                            row[internal_key] = None
                    except ValueError:
                        row[internal_key] = None
                
                # Remove the old key if it exists
                if csv_key in row and csv_key != internal_key:
                    del row[csv_key]

            # Create section key if not exists
            if section not in student_rec:
                student_rec[section] = {}

            # Add student to the section
            student_rec[section][student_id] = row
    
    return student_rec

def list_sections(file):
    """Get list of sections from a CSV file"""
    try:
        student_rec = load_students_csv(file)
        section_list = []
        for sec in student_rec.keys():
            section_list.append(sec)
        return section_list
    except Exception as e:
        print(f"Error reading sections from file: {e}")
        return []