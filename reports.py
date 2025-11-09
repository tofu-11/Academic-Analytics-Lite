#i only need the data_record dictionary
#variable data_record
#and the mean median mode, minimum, maximum, standard deviation for each section dictionary
#variable section_record


def analysis_report_output(data_record, section_record):
            #spaces             17               15                  20             13              8       14              8
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
                      f"{student['rating']:^8}|"
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
                print(f"|{section_data['MEAN']:^6}|"
                      f"{section_data['MEDIAN']:^8}|"
                      f"{section_data['MODE']:^6}|"
                      f"{section_data['MINIMUM']:^9}|"
                      f"{section_data['MAXIMUM']:^9}|"
                      f"{section_data['STANDARD DEVIATION']:^20}|\n")
                print(table_separator)

    for section, student_list in data_record.items():
        print(f"{'ANALYSIS REPORT':^101}\n")
        print(f"{section:^101}\n")
        print(table_separator)                                                     #LETTER GRADE    
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


def compare_output(section_record):
    table_separator = (f"{' _____________ ______ ________ ______ _________ _________ ____________________ '}\n")

    print(f"\n{'COMPARE OUTPUT':^79}\n")
    print(table_separator)                          
    print("|   SECTION   | MEAN | MEDIAN | MODE | MINIMUM | MAXIMUM | STANDARD DEVIATION |\n")
    print(table_separator)
    
    sorted_sections = sorted(section_record.items(), key=lambda x: x[1]['MEAN'], reverse=True)

    for section_name, stats in sorted_sections:
        print(f"|{section_name:^13}|"
              f"{stats['MEAN']:^6}|"
              f"{stats['MEDIAN']:^8}|"
              f"{stats['MODE']:^6}|"
              f"{stats['MINIMUM']:^9}|"
              f"{stats['MAXIMUM']:^9}|"
              f"{stats['STANDARD DEVIATION']:^20}|")
        print(table_separator)

def improvement_output(data_record):
    table_separator = (f"{' _________________ _______________ ____________________ __________ __________ __________ __________ __________ ___________ ____________ ____________ _____________ ________ ____________ '}\n")


    print(f"\n{'SECTION STATISTICS':^183}\n")
    for section, student_list in data_record.items():
        print(f"{section:^183}\n")
        print(table_separator)
        #              17               15                 20              10         10         10        10          10         11           12           12           13          8          12
        print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     |  QUIZ 1  |  QUIZ 2  |  QUIZ 3  |  QUIZ 4  |  QUIZ 5  |  MIDTERM  | FINAL EXAM | ATTENDANCE | FINAL GRADE | RATING | PERCENTILE |\n")
        print(table_separator)

        for student_id, student in student_list.items():
                print(f"|{student_id:^17}|"
                      f"{student['last_name']:^15}|"
                      f"{student['first_name']:^20}|"
                      f"{student['quiz_1']:^10}|"
                      f"{student['quiz_2']:^10}|"
                      f"{student['quiz_3']:^10}|"
                      f"{student['quiz_4']:^10}|"
                      f"{student['quiz_5']:^10}|"
                      f"{student['midterm']:^11}|"
                      f"{student['final_exam']:^12}|"
                      f"{student['attendance']:^12}|"
                      f"{student['final_grade']:^13}|"
                      f"{student['rating']:^8}|"
                      f"{student['percentile']:^12}|\n")
                print(table_separator)


    invalid_table_separator = (f'{" _________________ _______________ ____________________ _________\n"}')
    print(f"\n{'INVALID STUDENTS':^65}\n")
    print(invalid_table_separator)
    print("|   STUDENT ID    |   LAST NAME   |     FIRST NAME     | SECTION |\n")
    print(invalid_table_separator)

    for section, student_list in data_record.items():
        for student_id, student in student_list.items():
            if student['status'].lower() == "invalid":
                print(f"|{student_id:^17}|"
                      f"{student['last_name']:^15}|"
                      f"{student['first_name']:^20}|"
                      f"{section:^9}|\n")
                print(invalid_table_separator)

analysis_report_output(data_record, section_record)
compare_output(section_record)
improvement_output(data_record)

