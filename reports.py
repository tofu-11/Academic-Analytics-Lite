#i only need the data_record dictionary
#variable data_record
#and the mean median mode, minimum, maximum, standard deviation for each section dictionary
#variable section_record
import analyze
import transform
from ingest import load_students_csv
from settings import CONFIG
from pathlib import Path
import csv
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_final_grades(section_data, section_name="Section"):
    """
    section_data: dict of students for a specific section
    section_name: optional, used for title
    """
    # Collect all final grades
    final_grades = [student['final_grade'] for student in section_data.values()]

    # Plot histogram
    plt.hist(final_grades, bins=10, color='skyblue', edgecolor='black')
    plt.title(f"Final Grades Distribution - {section_name}")
    plt.xlabel("Final Grade")
    plt.ylabel("Number of Students")
    plt.show()


def _export_atrisk_to_csv(atrisk_students):
    """
    Export at-risk students to a CSV file in the data directory.
    If the file exists, append new students; otherwise create it.
    
    CSV columns: student_id, last_name, first_name, final_grade, rating, percentile, status
    """
    if not atrisk_students:
        return
    
    base_dir = Path.cwd()
    data_dir = base_dir / CONFIG.get("data_dir", "LMS Files")
    atrisk_path = data_dir / "at-risk.csv"
    
    try:
        # Check if file exists to determine if we need to write headers
        file_exists = atrisk_path.exists()
        
        with open(atrisk_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers if file is new
            if not file_exists:
                writer.writerow([
                    'student_id',
                    'last_name',
                    'first_name',
                    'final_grade',
                    'rating',
                    'percentile',
                    'status'
                ])
            
            # Write each at-risk student
            for student in atrisk_students:
                writer.writerow([
                    student['student_id'],
                    student['last_name'],
                    student['first_name'],
                    student['final_grade'],
                    student['rating'],
                    student['percentile'],
                    student['status']
                ])
        
        print(f"\n✓ At-risk students exported to: {atrisk_path}")
    
    except Exception as e:
        print(f"\n✗ Error exporting at-risk students: {e}")

def plot_all_final_grades(data_record):
    """
    data_record: dict structured as {section_name: {student_id: {....}}}
    Collects final grades from all sections and plots a histogram.
    """
    final_grades = []

    # Iterate through all sections and students
    for section, students in data_record.items():
        for student_id, student_data in students.items():
            if 'final_grade' in student_data:  # safety check
                final_grades.append(student_data['final_grade'])

    if not final_grades:
        print("No final grades found in the data.")
        return

    # Plot histogram
    plt.hist(final_grades, bins=10, color='lightgreen', edgecolor='black')
    plt.title("Final Grades Distribution - All Sections")
    plt.xlabel("Final Grade")
    plt.ylabel("Number of Students")
    plt.show()


def analysis_report_output(file_path):
    try:
        # Get transformed data
        transformed_data = transform.main(file_path)
        if not transformed_data:
            print("Error: No data to analyze")
            return
            
        # Add analysis data
        data_record = analyze.analyze_report_output(transformed_data)
        section_record = {}
        
        # Calculate statistics for each section
        for section in data_record.keys():
            if section in data_record:
                section_record[section] = analyze.get_basic_stats_numpy(data_record[section], section)
        
        table_separator = (f"{' _________________ _______________ ____________________ _____________ ________ ______________ ________'}\n")

        def atrisk_table(student_list, table_separator):
            print(f"\n{'AT RISK STUDENTS':^101}\n")
            print(table_separator)
            print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     | FINAL GRADE | RATING |  PERCENTILE  | STATUS |\n")
            print(table_separator)
            
            # Collect at-risk students for CSV export
            atrisk_students = []
            for student_id, student in student_list.items():
                if student['final_grade'] < 75:
                    print(f"|{student_id:^17}|"
                          f"{student['last_name']:^15}|"
                          f"{student['first_name']:^20}|"
                          f"{student['final_grade']:^13}|"
                          f"{student['letter_grade']:^8}|"
                          f"{student['percentile']:^14}|"
                          f"{student['status']:^8}|\n")
                    print(table_separator)
                    atrisk_students.append({
                        'student_id': student_id,
                        'last_name': student['last_name'],
                        'first_name': student['first_name'],
                        'final_grade': student['final_grade'],
                        'rating': student['letter_grade'],
                        'percentile': student['percentile'],
                        'status': student['status']
                    })
            
            # Export at-risk students to CSV
            _export_atrisk_to_csv(atrisk_students)

        def section_statistics(section_record, section_name):
            table_separator = (f"{' ______ ________ ______ _________ _________ ____________________ '}\n")
            print(f"\n{'SECTION STATISTICS':^65}\n")
            print(table_separator)
            print("| MEAN | MEDIAN | MODE | MINIMUM | MAXIMUM | STANDARD DEVIATION |\n")
            print(table_separator)
            
            for section, section_data in section_record.items():
                if section == section_name:
                    print(f"|{section_data['mean']:^6}|"
                          f"{section_data['median']:^8}|"
                          f"{section_data['mode']:^6}|"
                          f"{section_data['min']:^9}|"
                          f"{section_data['max']:^9}|"
                          f"{section_data['std']:^20}|\n")
                    print(table_separator)

        for section, student_list in data_record.items():
            print(f"{'ANALYSIS REPORT':^101}\n")
            print(f"{section:^101}\n")
            print(table_separator)
            print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     | FINAL GRADE | RATING |  PERCENTILE  | STATUS |\n")
            print(table_separator)

            for student_id, student in student_list.items():
                print(f"|{student_id:^17}|"
                      f"{student['last_name']:^15}|"
                      f"{student['first_name']:^20}|"
                      f"{student['final_grade']:^13}|"
                      f"{student['rating']:^8}|"
                      f"{student['percentile']:^14}|"
                      f"{student['status']:^8}|\n")
                print(table_separator)

            atrisk_table(student_list, table_separator)
            section_statistics(section_record, section)
    except Exception as e:
        print(f"Error in analysis_report_output: {e}")
        import traceback
        traceback.print_exc()
    while True:
        print("1. View Histogram of a Section\n2. View Histogram of all Sections\n3.Exit")
        user = input("\n")
        if user == "1":
            print("Please choose a section")
            i = 1
            for section in data_record.keys():
                print(i, ". ", section)
                i += 1
            while True:
                choice = int(input())
                if choice > len(data_record.keys()) or choice <= 0:
                    print("Please choose a proper number!")
                else:
                    break
            section_name = list(data_record.keys())[choice-1]
            plot_final_grades(data_record[section_name], section_name)
        elif user == "3":
            break
        elif user == "2":
            plot_all_final_grades(data_record)
        else:
            print("Please choose a proper number!")
                



def compare_output(section_choices, file_path=None):
    if not section_choices:
        return
        
    # Get and analyze data
    data = transform.main(file_path) if file_path else {}
    data_record = analyze.analyze_report_output(data)
    section_record = {}
    
    # Calculate stats for selected sections
    for section in section_choices:
        if section in data_record:
            section_record[section] = analyze.get_basic_stats_numpy(data_record[section], section)

    table_separator = (f"{' _____________ ______ ________ ______ _________ _________ ____________________ '}\n")

    print(f"\n{'COMPARE OUTPUT':^79}\n")
    print(table_separator)                          
    print("|   SECTION   | MEAN | MEDIAN | MODE | MINIMUM | MAXIMUM | STANDARD DEVIATION |\n")
    print(table_separator)
    
    sorted_sections = sorted(section_record.items(), key=lambda x: x[1]['mean'], reverse=True)

    for section_name, stats in sorted_sections:
        print(f"|{section_name:^13}|"
              f"{stats['mean']:^6}|"
              f"{stats['median']:^8}|"
              f"{stats['mode']:^6}|"
              f"{stats['min']:^9}|"
              f"{stats['max']:^9}|"
              f"{stats['std']:^20}|")
        print(table_separator)

def improvement_output(file_choices):
    try:
        # Get and analyze both files with percentiles
        data1 = transform.for_improvements(file_choices[0])
        data2 = transform.for_improvements(file_choices[1])
        
        if not data1 or not data2:
            print("Error: Failed to load one or both files")
            return
        
        # Calculate improvements with percentile differences
        data_record = analyze.improvements_output(data1, data2)
        
        table_separator = (f"{' _________________ _______________ ____________________ __________ __________ __________ __________ __________ ___________ ____________ ____________ _____________ ________ ____________ '}\n")

        print(f"\n{'IMPROVEMENTS REPORT':^183}\n")
        for section, student_list in data_record.items():
            print(f"{section:^183}\n")
            print(table_separator)
            #              17               15                 20              10         10         10        10          10         11           12           12           13          8          12
            print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     |  QUIZ 1  |  QUIZ 2  |  QUIZ 3  |  QUIZ 4  |  QUIZ 5  |  MIDTERM  | FINAL EXAM | ATTENDANCE | FINAL GRADE | RATING | PERCENTILE |\n")
            print(table_separator)

            for student_id, student in student_list.items():
                    # Format differences with +/- prefix
                    quiz_1_diff = f"{'+' if student.get('quiz_1', 0) >= 0 else ''}{student.get('quiz_1', 0)}"
                    quiz_2_diff = f"{'+' if student.get('quiz_2', 0) >= 0 else ''}{student.get('quiz_2', 0)}"
                    quiz_3_diff = f"{'+' if student.get('quiz_3', 0) >= 0 else ''}{student.get('quiz_3', 0)}"
                    quiz_4_diff = f"{'+' if student.get('quiz_4', 0) >= 0 else ''}{student.get('quiz_4', 0)}"
                    quiz_5_diff = f"{'+' if student.get('quiz_5', 0) >= 0 else ''}{student.get('quiz_5', 0)}"
                    midterm_diff = f"{'+' if student.get('midterm', 0) >= 0 else ''}{student.get('midterm', 0)}"
                    final_exam_diff = f"{'+' if student.get('final_exam', 0) >= 0 else ''}{student.get('final_exam', 0)}"
                    attendance_diff = f"{'+' if student.get('attendance', 0) >= 0 else ''}{student.get('attendance', 0)}"
                    final_grade_diff = f"{'+' if student.get('final_grade', 0) >= 0 else ''}{student.get('final_grade', 0)}"
                    percentile_diff = f"{'+' if student.get('percentile', 0) >= 0 else ''}{student.get('percentile', 0)}"
                    
                    print(f"|{student_id:^17}|"
                          f"{student['last_name']:^15}|"
                          f"{student['first_name']:^20}|"
                          f"{quiz_1_diff:^10}|"
                          f"{quiz_2_diff:^10}|"
                          f"{quiz_3_diff:^10}|"
                          f"{quiz_4_diff:^10}|"
                          f"{quiz_5_diff:^10}|"
                          f"{midterm_diff:^11}|"
                          f"{final_exam_diff:^12}|"
                          f"{attendance_diff:^12}|"
                          f"{final_grade_diff:^13}|"
                          f"{student.get('rating', 'N/A'):^8}|"
                          f"{percentile_diff:^12}|\n")
                    print(table_separator)

        invalid_table_separator = (f'{" _________________ _______________ ____________________ _________\n"}')
        print(f"\n{'INVALID STUDENTS':^65}\n")
        print(invalid_table_separator)
        print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     | SECTION |\n")
        print(invalid_table_separator)

        for section, student_list in data_record.items():
            for student_id, student in student_list.items():
                if student.get('status', '').lower() == "invalid":
                    print(f"|{student_id:^17}|"
                          f"{student.get('last_name', 'N/A'):^15}|"
                          f"{student.get('first_name', 'N/A'):^20}|"
                          f"{section:^9}|\n")
                    print(invalid_table_separator)
    except Exception as e:
        print(f"Error in improvement_output: {e}")
        import traceback
        traceback.print_exc()


def export_per_section(file_path):
    """
    Analyze a CSV file and export per-section statistics to individual CSV files.
    
    For each section in the file:
      - Compute: mean, median, mode, min, max, standard_deviation of final grades
      - Write to CSV: <section_name>.csv with columns:
        section_name, student_population, mean, median, mode, minimum, maximum, standard_deviation
    
    Output files are written to the data directory (CONFIG['data_dir']).
    """
    try:
        # Load and transform the data
        data = transform.main(file_path)
        if not data:
            print("Error: No data to analyze")
            return
        
        data_record = analyze.analyze_report_output(data)
        
        # Output directory
        base_dir = Path.cwd()
        data_dir = base_dir / CONFIG.get("data_dir", "LMS Files")
        
        # For each section, compute stats and export
        for section_name, students in data_record.items():
            # Extract final grades (only valid ones)
            final_grades = [
                s.get('final_grade') 
                for s in students.values() 
                if s.get('final_grade') is not None
            ]
            
            if not final_grades:
                print(f"Warning: Section '{section_name}' has no valid grades. Skipping.")
                continue
            
            # Compute statistics
            final_grades.sort()
            student_count = len(final_grades)
            mean_val = round(sum(final_grades) / student_count, 2)
            median_val = round(final_grades[student_count // 2], 2)
            
            # Mode (most common grade; if tie, take first)
            from collections import Counter
            grade_counts = Counter(final_grades)
            mode_val = round(grade_counts.most_common(1)[0][0], 2)
            
            min_val = round(min(final_grades), 2)
            max_val = round(max(final_grades), 2)
            
            # Standard deviation
            if student_count > 1:
                variance = sum((g - mean_val) ** 2 for g in final_grades) / (student_count - 1)
                std_dev = round(variance ** 0.5, 2)
            else:
                std_dev = 0.0
            
            # Write CSV
            safe_section_name = section_name.replace('/', '_').replace('\\', '_').strip()
            output_path = data_dir / f"{safe_section_name}.csv"
            
            try:
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'section_name',
                        'student_population',
                        'mean',
                        'median',
                        'mode',
                        'minimum',
                        'maximum',
                        'standard_deviation'
                    ])
                    writer.writerow([
                        section_name,
                        student_count,
                        mean_val,
                        median_val,
                        mode_val,
                        min_val,
                        max_val,
                        std_dev
                    ])
                
                print(f"✓ Exported: {output_path}")
            except Exception as e:
                print(f"✗ Error writing {output_path}: {e}")
        
        print("\nExport complete!")
    
    except Exception as e:
        print(f"Error in export_per_section: {e}")
        import traceback
        traceback.print_exc()

