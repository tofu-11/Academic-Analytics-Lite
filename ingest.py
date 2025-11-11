from pathlib import Path
import csv
from settings import CONFIG

base_dir = Path.cwd()
data_dir = base_dir / CONFIG.get("data_dir", "LMS Files")
data_dir.mkdir(exist_ok=True)

# Build file list using configured extensions
file_list = []
folder = Path(data_dir)
for file in folder.iterdir():
    if file.is_file():
        if file.suffix.lower() in [ext.lower() for ext in CONFIG.get("file_extensions", [".csv"])]:
            file_list.append(file)

def list_files():
    i = 1
    exts = [ext.lower() for ext in CONFIG.get("file_extensions", [".csv"])]
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in exts:
            print(i, ". ", file.name)
            i += 1

def load_students_csv(file_name):
    """Reads a CSV file of students and returns a dictionary grouped by section.

    Mapping of CSV column names -> internal keys is driven by CONFIG['csv']['field_mapping'].
    Numeric scores are converted to floats; empty or invalid values become None.
    """
    student_rec = {}
    encoding = CONFIG.get("csv", {}).get("encoding", "utf-8")
    field_mapping = CONFIG.get("csv", {}).get("field_mapping", {})

    with open(file_name, mode="r", newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Normalize string fields safely
            for k in ["last_name", "first_name", "section"]:
                if k in row and isinstance(row[k], str):
                    row[k] = row[k].strip()

            section = row.get("section", "").strip()
            student_id = row.get("student_id", "").strip()

            # Map CSV columns to internal keys and convert numeric values
            for csv_key, internal_key in field_mapping.items():
                raw = row.get(csv_key, "")
                val = raw.strip() if isinstance(raw, str) else raw

                if val == "" or val is None:
                    row[internal_key] = None
                else:
                    try:
                        score = float(val)
                        # Accept any non-negative number; normalization to percent happens later
                        if score < 0:
                            row[internal_key] = None
                        else:
                            row[internal_key] = score
                    except Exception:
                        row[internal_key] = None

                # Remove original csv column if different
                if csv_key in row and csv_key != internal_key:
                    del row[csv_key]

            # Create section key if not exists
            if section not in student_rec:
                student_rec[section] = {}

            # Add student to the section (store the full row dict)
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