from ingest import load_students_csv
from main import num
"""
quiz = 50%
midterm = 20%
final = 20%
attendance = 10%
"""

def calculate_final_grade(student):
    dict = load_students_csv(num)
    quiz_scores = [student[f"quiz{i}"]] for i in range(1, 60)







    return round(final_grade, 2)

def convert_to_letter_grade(final_grade):
    
    if not (0 <= final_grade <= 100):
        raise ValueError("Grade must be between 0 and 100")

    if final_grade >= 97:
        return 'S'
    elif final_grade >= 90:
        return 'A'
    elif final_grade >= 85:
        return 'B'
    elif final_grade >= 75:
        return 'C'
    elif final_grade >= 70:
        return 'D'
    else:
        return 'F'