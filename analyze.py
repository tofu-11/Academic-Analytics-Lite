"""
analyze.py - zachary - Student Performance Analytics

analyzes student grade data from transform.py
then returns structured data for reports.py to visualize

FEATURES:
1 - Distributions (letter grades, score ranges)
2 - Percentiles (Q1, Median, Q3)
3 - Outliers (high/low performers)
4 - Improvements (compare 2 CSV files by DATE)
5 - Bell Curve (STRETCH FEATURE)
6 - NumPy optimized versions (STRETCH FEATURE)
6 - Compare (WIP)

NOTE: This part (analyze.py) ONLY returns analyzed data.
      reports.py is the one that handles plotting/visualization(output).
"""

import math
import copy
from collections import Counter
# NumPy support for our stretch features, numpy is basically for optimization and process data way way faster than ordinary
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("ERROR!: NumPy is not available. using standard library.") ##handling when numpy is not available, use standard as backup 


# ==================== DISTRIBUTIONS ====================

def get_letter_distribution(student_records):
    """
    D: counts how many students got each letter grade.
    
    REQUIRES: student_records from transform.py with 'letter_grade' key -> carlos branch
    RETURNS: dict with letter grade counts
    """
    distribution = {'S': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    for student in student_records:
        grade = student.get('letter_grade', 'F')
        distribution[grade] += 1
    
    return distribution


def get_score_ranges(student_records):
    """
    D: group scores into ranges: 0-59, 60-69, 70-79, 80-89, 90-100
    
    REQUIRES: student_records from transform.py with 'final_grade' key -> carlos branch
    RETURNS: dict with score range counts
    """
    ranges = {
        '0-59 (F)': 0,
        '60-69 (D)': 0,
        '70-79 (C)': 0,
        '80-89 (B)': 0,
        '90-100 (A/S)': 0
    }
    
    for student in student_records:
        score = student.get('final_grade')
        if score is None:
            continue
            
        if score < 60:
            ranges['0-59 (F)'] += 1
        elif score < 70:
            ranges['60-69 (D)'] += 1
        elif score < 80:
            ranges['70-79 (C)'] += 1
        elif score < 90:
            ranges['80-89 (B)'] += 1
        else:
            ranges['90-100 (A/S)'] += 1
    
    return ranges


# ==================== PERCENTILES ====================

def percentile_of_score(scores, target_score):
    """
    Returns the percentile rank of a specific score in a list of scores.
    
    Percentile rank = percentage of scores less than or equal to the target.
    """
    if not scores:
        raise ValueError("The scores list is empty.")
    
    scores_sorted = sorted(scores)
    count_below = sum(1 for s in scores_sorted if s < target_score)
    count_equal = sum(1 for s in scores_sorted if s == target_score)
    
    # Percentile formula: ((below + 0.5 * equal) / total) * 100
    percentile = ((count_below + 0.5 * count_equal) / len(scores_sorted)) * 100
    return percentile

def calculate_percentile(student_records, percentile):
    """
    Find the score at a given percentile.
    Example: percentile=75 means 75% of students scored below this.
    
    REQUIRES: student_records from transform.py with 'final_grade' key -> carlos
    RETURNS: float score at percentile

    how the algorithm works
    # Step by step:
    # 1. Extract: [85, 92, 78, 65, 88]
    # 2. Sort: [65, 78, 85, 88, 92]
    # 3. Calculate: (75/100) * 5 = 3.75 → int = 3
    # 4. grades[3] = 88
    # Result: 88.0 (75% of students scored below 88)
    """
    grades = [s['final_grade'] for s in student_records 
             if s.get('final_grade') is not None]
    
    if not grades:
        return 0
    
    grades.sort()
    index = int((percentile / 100) * len(grades))
    if index >= len(grades):            #safety check, guardrail to make sure its the valid position
        index = len(grades) - 1
    
    return round(grades[index], 2)


def get_common_percentiles(student_records):
    """
    Get 25th, 50th (median), and 75th percentiles.
    
    REQUIRES: student_records from transform.py with 'final_grade' key -> carlso branch
    RETURNS: dict with Q1, Median, Q3
    """
    return {
        '25th (Q1)': calculate_percentile(student_records, 25),
        '50th (Median)': calculate_percentile(student_records, 50),
        '75th (Q3)': calculate_percentile(student_records, 75)
    }


# ==================== OUTLIERS ====================

def find_outliers(student_records):
    """
    D: find students with unusually high or low grades.
    uses the standard IQR method: outliers are 1.5 * IQR away from Q1/Q3
    
    REQUIRES: student_records from transform.py with 'final_grade', 'student_id', 'first_name', 'last_name' -> carlos branch
    RETURNS: list of dicts with outlier student info
    """
    grades = [s['final_grade'] for s in student_records 
              if s.get('final_grade') is not None]
    
    if len(grades) < 4:
        return []
    
    grades.sort()
    
    # Calculate quartiles
    q1_index = len(grades) // 4
    q3_index = 3 * len(grades) // 4
    q1 = grades[q1_index]
    q3 = grades[q3_index]
    
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Find outlier students
    outliers = []
    for student in student_records:
        grade = student.get('final_grade')
        if grade is None:
            continue
            
        if grade < lower_bound or grade > upper_bound:
            outlier_info = {
                'student_id': student['student_id'],
                'last_name' : student['last_name'],
                'first_name': student['first_name'],
                'section': student.get('section', 'N/A'),
                'final_grade': grade,
                'letter_grade': student['letter_grade'],
                'type': 'low performer' if grade < lower_bound else 'high performer'
            }
            outliers.append(outlier_info)
    
    return outliers


# ==================== IMPROVEMENTS (2 CSV COMPARISON BY DATE) ====================

def compare_by_date(date_a_records, date_b_records, date_a_label="Date A", date_b_label="Date B"):
    """
    D: compare student grades between 2 different dates (2 CSV files).
    matches students by student_id.
    
    REQUIRES: 
        - date_a_records: list from transform.py (earlier date) CSV A
        - date_b_records: list from transform.py (later date) CSV B
        - soon if abot: CSV that combines both or all. medjo complex nga lang to
        - Both must have: student_id, first_name, last_name, final_grade, section -> carlos branch
    
    RETURNS: dict with 3 keys:
        - 'matched': list of students found in BOTH files with improvement status
        - 'incomplete_a': students only in Date A (dropped out or missing from Date B)
        - 'incomplete_b': students only in Date B (new students or missing from Date A)
    """
    
    # Create lookup dictionaries by student_id
    date_a_dict = {}
    for student in date_a_records:
        sid = student.get('student_id')
        if sid:
            date_a_dict[sid] = student
    
    date_b_dict = {}
    for student in date_b_records:
        sid = student.get('student_id')
        if sid:
            date_b_dict[sid] = student
    
    # results structure
    matched = []
    incomplete_a = []  # Students that are in A but not in B
    incomplete_b = []  # Students that are in B but not in A
    
    # find matched students (in both dates)
    for sid in date_a_dict:
        if sid in date_b_dict:
            student_a = date_a_dict[sid]
            student_b = date_b_dict[sid]
            
            grade_a = student_a.get('final_grade')
            grade_b = student_b.get('final_grade')
            
            if grade_a is not None and grade_b is not None:
                change = grade_b - grade_a
                
                # category of improvement based on latest date (Date B)
                if change > 10:
                    status = 'strong improvement'
                elif change > 3:
                    status = 'improving'
                elif change >= -3:
                    status = 'stable'
                elif change > -10:
                    status = 'declining'
                else:
                    status = 'strong decline'
                
                matched.append({
                    'student_id': sid,
                    'name': f"{student_b.get('first_name', '')} {student_b.get('last_name', '')}".strip(),
                    'section': student_b.get('section', 'N/A'),
                    f'{date_a_label}_grade': round(grade_a, 2),
                    f'{date_b_label}_grade': round(grade_b, 2),
                    'change': round(change, 2),
                    'status': status
                })
    
    # fnid students only in Date A (incomplete in B)
    for sid in date_a_dict:
        if sid not in date_b_dict:
            student = date_a_dict[sid]
            incomplete_a.append({
                'student_id': sid,
                'name': f"{student.get('first_name', '')} {student.get('last_name', '')}".strip(),
                'section': student.get('section', 'N/A'),
                'grade': student.get('final_grade'),
                'reason': f'Missing in {date_b_label}'
            })
    
    # find students only in Date B (incomplete in A / new students)
    for sid in date_b_dict:
        if sid not in date_a_dict:
            student = date_b_dict[sid]
            incomplete_b.append({
                'student_id': sid,
                'name': f"{student.get('first_name', '')} {student.get('last_name', '')}".strip(),
                'section': student.get('section', 'N/A'),
                'grade': student.get('final_grade'),
                'reason': f'Missing in {date_a_label} (New student or transfer)'
            })
    
    return {
        'matched': matched,
        'incomplete_a': incomplete_a,
        'incomplete_b': incomplete_b,
        'summary': {
            'total_matched': len(matched),
            'total_incomplete_a': len(incomplete_a),
            'total_incomplete_b': len(incomplete_b),
            'improving_count': sum(1 for s in matched if 'improv' in s['status']),
            'declining_count': sum(1 for s in matched if 'declin' in s['status']),
            'stable_count': sum(1 for s in matched if s['status'] == 'stable')
        }
    }

"""         WAIT TENTATIVE!!!
def get_improvement_by_section(comparison_result):
    
    D: break down improvements by section.
    
    REQUIRES: comparison_result from compare_by_date()
    RETURNS: dict with section-wise improvement breakdown
    
    sections = {}
    
    for student in comparison_result['matched']:
        section = student['section']
        if section not in sections:
            sections[section] = {
                'strong improvement': 0,
                'improving': 0,
                'stable': 0,
                'declining': 0,
                'strong decline': 0,
                'total': 0
            }
        
        status = student['status']
        sections[section][status] += 1
        sections[section]['total'] += 1
    
    return sections
"""

# ==================== BELL CURVE (GRADE CURBVE STRETCH FEATURE) ====================

def apply_curve(student_records, target_average=75):
    """
    D: apply bell curve to adjust grades so class average = target_average.
    usingses simple additive curve: adds/subtracts same amount to all grades.
    
    REQUIRES: student_records from transform.py with 'final_grade' key -> carlos branch
    RETURNS: student_records with added 'curved_grade' and 'curved_letter' keys -> gives the info to cris branch
    """
    grades = [s['final_grade'] for s in student_records
             if s.get('final_grade') is not None]
    
    if not grades:
        return student_records
    
    # calculate current average/mean
    current_avg = sum(grades) / len(grades)
    
    # how much to add to each grade
    adjustment = target_average - current_avg
    
    # apply curve to each student
    for student in student_records:
        if student.get('final_grade') is None:
            continue
            
        curved = student['final_grade'] + adjustment
        
        # Keep grades between 0-100
        curved = max(0, min(100, curved))
        
        student['curved_grade'] = round(curved, 2)
        
        # Recalculate each letter grade
        if curved >= 97:
            student['curved_letter'] = 'S'
        elif curved >= 90:
            student['curved_letter'] = 'A'
        elif curved >= 85:
            student['curved_letter'] = 'B'
        elif curved >= 75:
            student['curved_letter'] = 'C'
        elif curved >= 70:
            student['curved_letter'] = 'D'
        else:
            student['curved_letter'] = 'F'
    
    return student_records


def get_curve_stats(student_records):
    """
    D: Get before/after statistics for curved grades.
    
    REQUIRES: student_records with 'final_grade' and 'curved_grade' keys -> CARLOS BRANCH and Apply_Curve Function
    RETURNS: dict with before/after comparison stats
    """
    original_grades = [s['final_grade'] for s in student_records 
                    if s.get('final_grade') is not None]
    curved_grades = [s['curved_grade'] for s in student_records 
                     if s.get('curved_grade') is not None]
    
    if not curved_grades:   #handling
        return {'error': 'there are no curved grades found. Run apply_curve() first.'}
    
    return {
        'before': {
            'average': round(sum(original_grades) / len(original_grades), 2),
            'highest': round(max(original_grades), 2),
            'lowest': round(min(original_grades), 2)
        },
        'after': {
            'average': round(sum(curved_grades) / len(curved_grades), 2),
            'highest': round(max(curved_grades), 2),
            'lowest': round(min(curved_grades), 2)
        },
        'adjustment': round((sum(curved_grades) / len(curved_grades)) - (sum(original_grades) / len(original_grades)), 2)
    }


# ==================== NUMPY VERSIONS (STRETCH FEATURE) ====================

def get_basic_stats_numpy(section, section_name):
    """
    D: calculate statistics using NumPy (faster for large datasets if we have a lot of students).
    
    REQUIRES: ⚠️⚠️NumPy installed⚠️⚠️ <---, student_records with 'final_grade'
    RETURNS: dict with mean, median, std, min, max, Q1, Q3
    """
    
    stats_out = {}
    
    grades = [student["final_grade"]
                    for student in section.values()]
    counts = Counter(grades)
    stats_out = {
        'section': section_name,
        'mean': round(float(np.mean(grades)), 2),
        'median': round(float(np.median(grades)), 2),
        'mode' : counts.most_common(1)[0][0],
        'std': round(float(np.std(grades, ddof=1)), 2),
        'min': round(float(np.min(grades)), 2),
        'max': round(float(np.max(grades)), 2),
        'q1': round(float(np.percentile(grades, 25)), 2),
        'q3': round(float(np.percentile(grades, 75)), 2),
        'iqr': round(float(np.percentile(grades, 75) - np.percentile(grades, 25)), 2)
    }


    return stats_out




def apply_curve_numpy(student_records, target_average=75):
    """
    D: NumPy-optimized version of bell curve. if NumPy is installed
    
    REQUIRES: NumPy installed, student_records with 'final_grade'
    RETURNS: student_records with 'curved_grade' and 'curved_letter'
    """
    if not NUMPY_AVAILABLE:
        print("⚠️ NumPy not available. Using standard version instead.")
        return apply_curve(student_records, target_average)
    
    # Extract grades as numpy array
    grades_list = [s.get('final_grade', 0) for s in student_records]
    grades = np.array(grades_list)
    valid_mask = np.array([s.get('final_grade') is not None for s in student_records])
    
    if not np.any(valid_mask):
        return student_records
    
    # Calculate adjustment
    current_avg = np.mean(grades[valid_mask])
    adjustment = target_average - current_avg
    
    # Apply curve using numpy
    curved_grades = np.clip(grades + adjustment, 0, 100)
    
    # Update records
    for i, student in enumerate(student_records):
        if valid_mask[i]:
            curved = float(curved_grades[i])
            student['curved_grade'] = round(curved, 2)
            
            # Letter grade
            if curved >= 97:
                student['curved_letter'] = 'S'
            elif curved >= 90:
                student['curved_letter'] = 'A'
            elif curved >= 85:
                student['curved_letter'] = 'B'
            elif curved >= 75:
                student['curved_letter'] = 'C'
            elif curved >= 70:
                student['curved_letter'] = 'D'
            else:
                student['curved_letter'] = 'F'
    
    return student_records





# ==================== BASIC STATS (STANDARD VERSION) ====================

def get_basic_stats(student_records):
    """
    D: calculate simple statistics about the class.
    
    REQUIRES: student_records from transform.py with 'final_grade'
    RETURNS: dict with count, average, highest, lowest, median, passing, failing
    """
    grades = [s['final_grade'] for s in student_records if s.get('final_grade') is not None]
    
    if not grades:
        return {}
    
    grades.sort()
    
    return {
        'count': len(grades),
        'average': round(sum(grades) / len(grades), 2),
        'highest': round(max(grades), 2),
        'lowest': round(min(grades), 2),
        'median': round(grades[len(grades) // 2], 2),
        'passing': sum(1 for g in grades if g >= 70),
        'failing': sum(1 for g in grades if g < 70)
    }


# ==================== FULL ANALYSIS (ALL-IN-ONE) ====================

def analyze_all(student_records):
    """
    D:run all analyses and return results in one dictionary.
    this is what reports.py will call to get all data.
    
    REQUIRES: student_records from transform.py
    RETURNS: dict with all analysis results
    """
    return {
        'basic_stats': get_basic_stats(student_records),
        'letter_distribution': get_letter_distribution(student_records),
        'score_ranges': get_score_ranges(student_records),
        'percentiles': get_common_percentiles(student_records),
        'outliers': find_outliers(student_records)
    }


def analyze_report_output(student_records):
    """
    Analyze student records and add percentile information
    
    Expected input structure:
    {
        'section_name': {
            'student_id': {
                'first_name': str,
                'last_name': str,
                'quiz_1': float,
                'quiz_2': float,
                'quiz_3': float,
                'quiz_4': float,
                'quiz_5': float,
                'midterm': float,
                'final_exam': float,
                'attendance': float,
                'final_grade': float,
                'letter_grade': str
            }
        }
    }
    """
    if not student_records:
        return {}
        
    updated_out = copy.deepcopy(student_records)

    for section in updated_out.keys():
        # Get all valid final grades for the section
        final_grades = [
            student.get("final_grade") 
            for student in updated_out[section].values() 
            if student.get("final_grade") is not None
        ]
        
        # Calculate percentile and set status for each student
        for student in updated_out[section].values():
            final_grade = student.get("final_grade")
            
            if final_grade is not None:
                student["percentile"] = round(percentile_of_score(final_grades, final_grade), 2)
                student["status"] = "valid"
                student["rating"] = student["letter_grade"]  # Use letter_grade as rating
            else:
                student["percentile"] = None
                student["status"] = "invalid"
                student["rating"] = "N/A"
    
    return updated_out

"""stud_rec = {
    '(section name)':
        {'(Student_ID)':
            {'last_name': None,
             'first_name': None,
             'quiz 1': None,
             'quiz 2': None,
             'quiz 3': None,
             'quiz 4': None,
             'quiz 5': None, 
             'midterms': None,
             'finals': None,
             'attendance': None,
             'final_grade':None,
             'letter_grade': None,
             'percentile': None,
             'status': '(valid/invalid)'}}}
"""

def improvements_output(dict1, dict2):
    diff = {}

    for section in dict2:
        diff[section] = {}

        # handle all students that appear in either dictionary
        all_students = set(dict1.get(section, {}).keys()) | set(dict2.get(section, {}).keys())

        for student_id in all_students:
            diff[section][student_id] = {}

            stud1 = dict1.get(section, {}).get(student_id)
            stud2 = dict2.get(section, {}).get(student_id)

            # If student not present in both -> invalid
            if not stud1 or not stud2:
                diff[section][student_id]["status"] = "invalid"
                continue

            # Copy identifying fields
            diff[section][student_id]["last_name"] = stud2.get("last_name")
            diff[section][student_id]["first_name"] = stud2.get("first_name")

            # Compute numeric differences for each score-related key
            for key, val2 in stud2.items():
                if key in ["last_name", "first_name", "status"]:
                    continue

                val1 = stud1.get(key)
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    diff_val = val2 - val1
                    diff[section][student_id][key] = f"{'+' if diff_val > 0 else ''}{diff_val}"
                else:
                    # For non-numeric or missing fields, just copy the latest value
                    diff[section][student_id][key] = None

            diff[section][student_id]["status"] = "valid"
            diff[section][student_id]["letter_grade"] = stud2.get("letter_grade")

    return diff

def compare_output(stats_dict):
    # Sort the items (section, stats) by mean value descending
    sorted_items = sorted(
        stats_dict.items(),
        key=lambda item: item[1]['mean'],
        reverse=True
    )
    
    # Convert back to dictionary to preserve sorted order
    sorted_dict = {section: stats for section, stats in sorted_items}
    
    return sorted_dict