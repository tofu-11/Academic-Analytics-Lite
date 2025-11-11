from ingest import load_students_csv
from settings import CONFIG


def _normalized_weights(weights: dict) -> dict:
    # Ensure weights sum to 1 by normalizing if necessary
    total = sum(weights.values()) if weights else 0
    if total == 0:
        return weights
    return {k: (v / total) for k, v in weights.items()}


def calculate_final_grade(student):
    """Compute final percentage grade based on CONFIG.

    Student dict is expected to contain numeric raw scores (not percentages):
      - quiz_1..quiz_5 as raw scores out of quiz_max_score
      - midterm as raw score out of midterm_max_score
      - final_exam as raw score out of final_max_score
      - attendance as percent (0-100) or a raw value intended to be percent
    """
    grading = CONFIG.get("grading", {})
    weights = _normalized_weights(grading.get("weights", {}))
    quiz_max = grading.get("quiz_max_score", 20)
    midterm_max = grading.get("midterm_max_score", 100)
    final_max = grading.get("final_max_score", 100)
    missing_policy = grading.get("missing_data_policy", "mark_invalid")

    # Collect quiz scores
    quiz_scores = [student.get(f"quiz_{i}") for i in range(1, 6) if student.get(f"quiz_{i}") is not None]

    if not quiz_scores and weights.get("quiz", 0) > 0:
        if missing_policy == "mark_invalid":
            return None
        else:
            quiz_avg_pct = 0.0
    else:
        # Average raw quiz score -> convert to percent using quiz_max
        quiz_avg = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
        quiz_avg_pct = (quiz_avg / quiz_max) * 100 if quiz_max else 0.0

    # Midterm
    mid_raw = student.get("midterm")
    if mid_raw is None:
        if missing_policy == "mark_invalid":
            return None
        mid_pct = 0.0
    else:
        mid_pct = (mid_raw / midterm_max) * 100 if midterm_max else 0.0

    # Final
    final_raw = student.get("final_exam")
    if final_raw is None:
        if missing_policy == "mark_invalid":
            return None
        final_pct = 0.0
    else:
        final_pct = (final_raw / final_max) * 100 if final_max else 0.0

    # Attendance expected to be percent already; treat None according to policy
    attendance_raw = student.get("attendance")
    if attendance_raw is None:
        if missing_policy == "mark_invalid":
            return None
        attendance_pct = 0.0
    else:
        attendance_pct = attendance_raw

    # Weighted sum
    weighted = 0.0
    weighted += quiz_avg_pct * weights.get("quiz", 0)
    weighted += mid_pct * weights.get("midterm", 0)
    weighted += final_pct * weights.get("final_exam", 0)
    weighted += attendance_pct * weights.get("attendance", 0)

    return round(weighted, 2)


def convert_to_letter_grade(final_grade):
    if final_grade is None:
        return 'N/A'

    if not (0 <= final_grade <= 100):
        return 'N/A'

    thresholds = CONFIG.get("letter_grade_thresholds", {})
    # Sort thresholds by cutoff descending
    sorted_thresholds = sorted(thresholds.items(), key=lambda kv: kv[1], reverse=True)
    for letter, cutoff in sorted_thresholds:
        try:
            if final_grade >= float(cutoff):
                return letter
        except Exception:
            continue

    return 'F'
        
def for_improvements(file):
    """Load students from CSV file and calculate grades"""
    try:
        # Convert Path object to string if needed
        file_path = str(file) if not isinstance(file, str) else file
        stud_rec = load_students_csv(file_path)   # {section: {student_id: student_dict}}
        
        if not isinstance(stud_rec, dict):
            print(f"Error: load_students_csv returned {type(stud_rec).__name__} instead of dict")
            return {}

        for section in stud_rec.keys():
            for student_id, student_data in stud_rec[section].items():
                final_grade = calculate_final_grade(student_data)
                student_data['final_grade'] = final_grade
                student_data['letter_grade'] = convert_to_letter_grade(final_grade)
        
        return stud_rec
    except Exception as e:
        print(f"Error in for_improvements: {e}")
        return {}


        
def main(file_path):
    """
    Load sectioned student records, compute final & letter grades for each student,
    insert them into each student's dict under keys "final grade" and "letter grade",
    and return the updated sectioned dictionary.

    Input format expected:
      { "BSIT 1-2": { "2021001": { ...student fields... }, ... }, ... }
    """
    try:
        # Convert Path object to string if needed
        file_path_str = str(file_path) if not isinstance(file_path, str) else file_path
        stud_rec = load_students_csv(file_path_str)   # {section: {student_id: student_dict}}
        
        if not isinstance(stud_rec, dict):
            print(f"Error: load_students_csv returned {type(stud_rec).__name__} instead of dict")
            return {}

        for section in stud_rec.keys():
            for student_id, student_data in stud_rec[section].items():
                final_grade = calculate_final_grade(student_data)
                student_data['final_grade'] = final_grade
                student_data['letter_grade'] = convert_to_letter_grade(final_grade)
        
        return stud_rec
    except Exception as e:
        print(f"Error in transform.main: {e}")
        return {}

