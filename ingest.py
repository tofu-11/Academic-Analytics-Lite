from pathlib import Path

base_dir = Path.cwd()        # Current working directory
data_dir = base_dir / "LMS Files" # Subfolder "data"
data_dir.mkdir(exist_ok=True)

#file_path = data_dir / "students.csv"

print(data_dir)
name = input("Enter file name: ")
file_path = data_dir / name
print(file_path)

def list_files():
    folder = Path(data_dir)

    for file in folder.iterdir():
        print(file.name)
        test
