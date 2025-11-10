from ingest import load_students_csv

"""
Grading System:
    Quizzes = 50%
    Midterm = 20%
    Final = 20%
    Attendance = 10%
"""

def calculate_final_grade(student):
    quiz_scores = [student[f"quiz_{i}"] for i in range(1, 6) if student.get(f"quiz_{i}") is not None]
    if not quiz_scores:
        return None
    quiz_avg = sum(quiz_scores) / len(quiz_scores)
    
    # Check if required fields exist and are not None
    if any(student.get(field) is None for field in ['midterm', 'final_exam', 'attendance']):
        return None
        
    weighted_quiz = quiz_avg * 0.50
    weighted_midterm = student['midterm'] * 0.20
    weighted_final = student['final_exam'] * 0.20
    weighted_attendance = student['attendance'] * 0.10
    
    final_grade = weighted_quiz + weighted_midterm + weighted_final + weighted_attendance
    
    return round(final_grade, 2)

def convert_to_letter_grade(final_grade):
    if final_grade is None:
        return 'N/A'
    
    if not (0 <= final_grade <= 100):
        return 'N/A'

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
        
def for_improvements(file):
    stud_rec = load_students_csv(file)   # {section: {student_id: student_dict}}

    for section in stud_rec.keys():
        for student_id, student_data in stud_rec[section].items():
            final_grade = calculate_final_grade(student_data)
            student_data['final_grade'] = final_grade
            student_data['letter_grade'] = convert_to_letter_grade(final_grade)
    
    return stud_rec


        
def main(file_path):
    """
    Load sectioned student records, compute final & letter grades for each student,
    insert them into each student's dict under keys "final grade" and "letter grade",
    and return the updated sectioned dictionary.

    Input format expected:
      { "BSIT 1-2": { "2021001": { ...student fields... }, ... }, ... }
    """
    stud_rec = load_students_csv(file_path)   # {section: {student_id: student_dict}}

    for section in stud_rec.keys():
        for student_id, student_data in stud_rec[section].items():
            final_grade = calculate_final_grade(student_data)
            student_data['final_grade'] = final_grade
            student_data['letter_grade'] = convert_to_letter_grade(final_grade)
    
    return stud_rec

