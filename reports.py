#i only need the data_record dictionary
#variable data_record
#and the mean median mode, minimum, maximum, standard deviation for each section dictionary
#variable section_record
import analyze
import transform
from ingest import load_students_csv

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
