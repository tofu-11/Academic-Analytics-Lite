students = [
    {
        "student_id": "2024-0001",
        "name": "Ethan Ernacio",
        "section": "BSIT 3A",
        "attendance": "95%",
        "quiz_1": 88,
        "quiz_2": 90,
        "quiz_3": 85,
        "quiz_4": 92,
        "quiz_5": 89,
        "midterm": 91,
        "final_exam": 94,
        "final_grade": 92.5,
        "rating": "A"
    },
    {
        "student_id": "2024-0002",
        "name": "Jedidiah Cruz",
        "section": "BSIT 3A",
        "attendance": "97%",
        "quiz_1": 90,
        "quiz_2": 93,
        "quiz_3": 89,
        "quiz_4": 95,
        "quiz_5": 91,
        "midterm": 92,
        "final_exam": 96,
        "final_grade": 93.8,
        "rating": "A"
    },
    {
        "student_id": "2024-0003",
        "name": "Ava Santos",
        "section": "BSIT 3B",
        "attendance": "98%",
        "quiz_1": 95,  # highest in quiz_1
        "quiz_2": 94,
        "quiz_3": 96,
        "quiz_4": 93,
        "quiz_5": 92,
        "midterm": 94,
        "final_exam": 97,
        "final_grade": 95.2,
        "rating": "A"
    },
    {
        "student_id": "2024-0004",
        "name": "Marco Dizon",
        "section": "BSIT 3B",
        "attendance": "96%",
        "quiz_1": 91,
        "quiz_2": 97,  # highest in quiz_2
        "quiz_3": 92,
        "quiz_4": 90,
        "quiz_5": 91,
        "midterm": 93,
        "final_exam": 95,
        "final_grade": 94.1,
        "rating": "A"
    },
    {
        "student_id": "2024-0005",
        "name": "Burat Sex",
        "section": "BSIT 3C",
        "attendance": "85%",
        "quiz_1": 70,
        "quiz_2": 75,
        "quiz_3": 80,
        "quiz_4": 78,
        "quiz_5": 72,
        "midterm": 74,
        "final_exam": 76,
        "final_grade": 75.0,
        "rating": "C"
    },
    {
        "student_id": "2024-0006",
        "name": "Carlos Dela Cruz",
        "section": "BSIT 3D",
        "attendance": "90%",
        "quiz_1": 85,
        "quiz_2": 82,
        "quiz_3": 80,
        "quiz_4": 88,
        "quiz_5": 84,
        "midterm": 86,
        "final_exam": 89,
        "final_grade": 86.0,
        "rating": "B"
    },
    {
        "student_id": "2024-0007",
        "name": "Lara Mendoza",
        "section": "BSIT 3D",
        "attendance": "93%",
        "quiz_1": 90,
        "quiz_2": 91,
        "quiz_3": 92,
        "quiz_4": 94,
        "quiz_5": 93,
        "midterm": 95,
        "final_exam": 97,
        "final_grade": 94.0,
        "rating": "A"
    },
    {
        "student_id": "2024-0008",
        "name": "Noel Pascual",
        "section": "BSIT 3D",
        "attendance": "88%",
        "quiz_1": 75,
        "quiz_2": 78,
        "quiz_3": 80,
        "quiz_4": 77,
        "quiz_5": 79,
        "midterm": 81,
        "final_exam": 84,
        "final_grade": 81.0,
        "rating": "B"
    },
    {
        "student_id": "2024-0009",
        "name": "Mika Ramos",
        "section": "BSIT 3E",
        "attendance": "94%",
        "quiz_1": 89,
        "quiz_2": 91,
        "quiz_3": 98,  # highest in quiz_3
        "quiz_4": 92,
        "quiz_5": 90,
        "midterm": 93,
        "final_exam": 95,
        "final_grade": 93.4,
        "rating": "A"
    },
    {
        "student_id": "2024-0010",
        "name": "Sean Villanueva",
        "section": "BSIT 3E",
        "attendance": "92%",
        "quiz_1": 87,
        "quiz_2": 88,
        "quiz_3": 90,
        "quiz_4": 97,  # highest in quiz_4
        "quiz_5": 92,
        "midterm": 94,
        "final_exam": 96,
        "final_grade": 94.2,
        "rating": "A"
    },
    {
        "student_id": "2024-0011",
        "name": "Julia Bautista",
        "section": "BSIT 3C",
        "attendance": "91%",
        "quiz_1": 86,
        "quiz_2": 87,
        "quiz_3": 89,
        "quiz_4": 90,
        "quiz_5": 98,  # highest in quiz_5
        "midterm": 92,
        "final_exam": 94,
        "final_grade": 93.0,
        "rating": "A"
    }
]



def identify_sections(data_record): #identifying each unique section 
    sections = []

    for person in data_record:
        if person['section'] not in sections:
            sections.append(person['section'])

    return sections

def status_students_report(data_record): #identifying status of each student
    for person in data_record:
        if person['final_grade'] >= 75:
            person['status'] = "Passed"

        else:
            person['status'] = "Failed"

    return data_record


def summarize_data_per_section(data_record):
    section_list = identify_sections(data_record) #calls the section lists
    section_data = []

    for section_name in section_list: #initializing list of dictionary per section
        section_data.append({
            'section': section_name,
            'quiz_1': 0,
            'quiz_2': 0,
            'quiz_3': 0,
            'quiz_4': 0,
            'quiz_5': 0,
            'midterm': 0,
            'final_exam': 0,
            'overall': 0,
            'student_count': 0
        })

    for student in data_record: #summation of all student record in a same section into one section data
        for section_entry in section_data:
            if student['section'] == section_entry['section']:
                section_entry['quiz_1'] += student['quiz_1'] 
                section_entry['quiz_2'] += student['quiz_2'] 
                section_entry['quiz_3'] += student['quiz_3'] 
                section_entry['quiz_4'] += student['quiz_4']
                section_entry['quiz_5'] += student['quiz_5'] 
                section_entry['midterm'] += student['midterm'] 
                section_entry['final_exam'] += student['final_exam']
                section_entry['overall'] += student['final_grade'] 
                section_entry['student_count'] += 1

    for section_entry in section_data: #getting the average of records per section
        total_students = section_entry['student_count']
        if total_students > 0:
            section_entry['quiz_1'] = round(section_entry['quiz_1'] / total_students, 2)
            section_entry['quiz_2'] = round(section_entry['quiz_2'] / total_students, 2)
            section_entry['quiz_3'] = round(section_entry['quiz_3'] / total_students, 2)
            section_entry['quiz_4'] = round(section_entry['quiz_4'] / total_students, 2)
            section_entry['quiz_5'] = round(section_entry['quiz_5'] / total_students, 2)
            section_entry['midterm'] = round(section_entry['midterm'] / total_students, 2)
            section_entry['final_exam'] = round(section_entry['final_exam'] / total_students, 2)
            section_entry['overall'] = round(section_entry['overall'] / total_students, 2)


    return section_data

def compare_per_section_record(data_record): #defining who is the highest scorer in each record per section 

    section_data = summarize_data_per_section(data_record)

    default_value = {
        'section': 'none',
        'quiz_1': 0,
        'quiz_2': 0,
        'quiz_3': 0,
        'quiz_4': 0,
        'quiz_5': 0,
        'midterm': 0,
        'final_exam': 0,
    }

    temp_holder = {
        'section': 'none',
        'quiz_1': 0,
        'quiz_2': 0,
        'quiz_3': 0,
        'quiz_4': 0,
        'quiz_5': 0,
        'midterm': 0,
        'final_exam': 0,
    }

    for section in section_data: #quiz1
        if  section['quiz_1'] >= temp_holder['quiz_1']:
            temp_holder['section'] = section['section']
            temp_holder['quiz_1'] = section['quiz_1']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['quiz_1'] = str(section['quiz_1']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #quiz2
        if  section['quiz_2'] >= temp_holder['quiz_2']:
            temp_holder['section'] = section['section']
            temp_holder['quiz_2'] = section['quiz_2']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['quiz_2'] = str(section['quiz_2']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #quiz3
        if  section['quiz_3'] >= temp_holder['quiz_3']:
            temp_holder['section'] = section['section']
            temp_holder['quiz_3'] = section['quiz_3']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['quiz_3'] = str(section['quiz_3']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #quiz4
        if  section['quiz_4'] >= temp_holder['quiz_4']:
            temp_holder['section'] = section['section']
            temp_holder['quiz_4'] = section['quiz_4']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['quiz_4'] = str(section['quiz_4']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #quiz5
        if  section['quiz_5'] >= temp_holder['quiz_5']:
            temp_holder['section'] = section['section']
            temp_holder['quiz_5'] = section['quiz_5']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['quiz_5'] = str(section['quiz_5']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #midterm
        if  section['midterm'] >= temp_holder['midterm']:
            temp_holder['section'] = section['section']
            temp_holder['midterm'] = section['midterm']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['midterm'] = str(section['midterm']) + '*'

    temp_holder = default_value.copy()

    for section in section_data: #final_exam
        if  section['final_exam'] >= temp_holder['final_exam']:
            temp_holder['section'] = section['section']
            temp_holder['final_exam'] = section['final_exam']
        
    for section in section_data:    
        if temp_holder['section'] == section['section']:
            section['final_exam'] = str(section['final_exam']) + '*'

    temp_holder = default_value.copy()

    return section_data


# FUNCTIONS BELOW ARE MOSTLY FOR FOR PRINTING

def generate_txtreport(data_record): #generating the main txt report

    section_list = identify_sections(data_record) #calls the section lists
    table_separator = (f"{'_________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________ ________ '}")

    with open("output.txt", "w") as txt_file:  # clear the file first, and header
        txt_file.write(f"{'DATA REPORTS':^154}\n")

    for section in section_list: 
        
        with open("output.txt", "a") as txt_file:
            txt_file.write(f"\n{'SECTION: '+ section:^154}\n")
            txt_file.write(table_separator + "\n")
            txt_file.write("|   STUDENT ID    |             NAME             | Attendance |           QUIZZES           |  MIDTERM  | FINAL EXAM | FINAL GRADE | RATING | STATUS |\n")
            txt_file.write(table_separator + "\n")
            txt_file.write("|                 |                              |            |  1  |  2  |  3  |  4  |  5  |           |            |             |        |        |\n")
            txt_file.write(table_separator + "\n")

            for person in data_record:
                if person['section'] == section:

                    status_students_report(data_record)
                    txt_file.write(f"|{person['student_id']:^17}|{person['name']:^30}|{person['attendance']:^12}|{person['quiz_1']:^5}|{person['quiz_2']:^5}|{person['quiz_3']:^5}|{person['quiz_4']:^5}|{person['quiz_5']:^5}|{person['midterm']:^11}|{person['final_exam']:^12}|{person['final_grade']:^13}|{person['rating']:^8}|{person['status']:^8}|\n")
                    txt_file.write(table_separator + "\n")

        generate_atrisk_table(section,students)

def generate_txt_section_compare_table(data_record):

    table_separator = (f"{'_____________ _____ _____ _____ _____ _____ _________ _______ _________'}")

    section_data = compare_per_section_record(data_record)

    section_data = sorted(section_data, key=lambda x: x['overall'], reverse=True) #sorting the section_data based on the overall record of the section

    with open("output.txt", "a") as txt_file:
        txt_file.write("\n"*2)
        txt_file.write(f"{'DATA REPORTS':^154}\n")        
        txt_file.write(f"{table_separator:^154}\n")
        txt_file.write(f"{'|   SECTION   |  1  |  2  |  3  |  4  |  5  | MIDTERM | FINALS| OVERALL |':^154}\n")
        txt_file.write(f"{table_separator:^154}\n")

        for section_entry in section_data:

            line = (
                f"|{section_entry['section']:^13}|"
                f"{section_entry['quiz_1']:^5}|"
                f"{section_entry['quiz_2']:^5}|"
                f"{section_entry['quiz_3']:^5}|"
                f"{section_entry['quiz_4']:^5}|"
                f"{section_entry['quiz_5']:^5}|"
                f"{section_entry['midterm']:^9}|"
                f"{section_entry['final_exam']:^7}|"
                f"{section_entry['overall']:^9}|"
            )

            txt_file.write(f"{line:^154}\n")
            txt_file.write(f"{table_separator:^154}\n")

def generate_atrisk_table(section,data_record):

    table_separator = (f"{'_________________ ______________________________ ____________ __________________________________ ___________ ____________ _____________ ________ ________ '}")
    status_students_report(data_record)

    with open("output.txt", "a") as txt_file:
        txt_file.write(f"\n{'AT-RISK STUDENTS':^159}\n")
        txt_file.write(table_separator + "\n")
        txt_file.write("|   STUDENT ID    |             NAME             | Attendance |  Q1  |  Q2  |  Q3  |  Q4  |  Q5  |  MIDTERM  | FINAL EXAM | FINAL GRADE | RATING | STATUS |\n")
        txt_file.write(table_separator + "\n")


    for person in data_record:
        if person['section'] == section:
            if person['final_grade'] < 75:
                txt_file.write(f"|{person['student_id']:^17}|{person['name']:^30}|{person['attendance']:^12}|{person['quiz_1']:^6}|{person['quiz_2']:^6}|{person['quiz_3']:^6}|{person['quiz_4']:^6}|{person['quiz_5']:^6}|{person['midterm']:^11}|{person['final_exam']:^12}|{person['final_grade']:^13}|{person['rating']:^8}|{person['status']:^8}|\n")
                txt_file.write(table_separator + "\n")

generate_txtreport(students)
generate_txt_section_compare_table(students)

section = identify_sections(students) #checker
print(section) #checker
print("the program runs!!")


