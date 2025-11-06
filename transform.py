from ingest import load_students_csv
from main import num

"""
Grading System:
    Quizzes = 50%
    Midterm = 20%
    Final = 20%
    Attendance = 10%
"""

def calculate_final_grade(student):
    quiz_scores = [student[f"quiz{i}"] for i in range(1, 6)]
    quiz_avg = sum(quiz_scores) / len(quiz_scores)
    
    weighted_quiz = quiz_avg * 0.50
    weighted_midterm = student['midterm'] * 0.20
    weighted_final = student['final'] * 0.20
    weighted_attendance = student['attendance_percent'] * 0.10
    
    final_grade = weighted_quiz + weighted_midterm + weighted_final + weighted_attendance
    
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
        
        
def main():
    final_stud_rec = []
    stud_rec = load_students_csv(num)

    for student_id, student in stud_rec.items():
        final_grade = calculate_final_grade(student)
        letter_grade = convert_to_letter_grade(final_grade)
        
        record_with_grade = student.copy()
        record_with_grade["final_grade"] = final_grade
        record_with_grade["letter_grade"] = letter_grade
        
        final_stud_rec.append(record_with_grade)
    
    return final_stud_rec
