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
        "quiz_1": 95,
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
        "student_id": "2024-0005",
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
        "student_id": "2024-0006",
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
        "student_id": "2024-0007",
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
    }
]


def identify_sections(data_record):
    sections = []

    for person in data_record:
        if person['section'] not in sections:
            sections.append(person['section'])

    return sections

def status_students_report(data_record):
    for person in data_record:
        if person['final_grade'] >= 75:
            person['status'] = "Passed"

        else:
            person['status'] = "Failed"


def summarize_data_per_section(data_record):
    section_list = identify_sections(data_record) #calls the section lists
    section_data = []

    for section_name in section_list:
        section_data.append({
            'section': section_name,
            'quiz_1': 0,
            'quiz_2': 0,
            'quiz_3': 0,
            'quiz_4': 0,
            'quiz_5': 0,
            'midterms': 0,
            'finals': 0,
            'overall': 0,
            'student_count': 0
        })

    for student in data_record:
        for section_entry in section_data:
            if student['section'] == section_entry['section']:
                section_entry['quiz_1'] += student['quiz_1']
                section_entry['quiz_2'] += student['quiz_2']
                section_entry['quiz_3'] += student['quiz_3']
                section_entry['quiz_4'] += student['quiz_4']
                section_entry['quiz_5'] += student['quiz_5']
                section_entry['midterm'] += student['midterm']
                section_entry['finals'] += student['finals']
                section_entry['student_count'] += 1




def generate_txtreport(data_record):

    section_list = identify_sections(data_record) #calls the section lists

    with open("output.txt", "w") as txt_file:  # clear the file first, and header
        txt_file.write(f"{'DATA REPORTS':^154}\n")

    for section in section_list: 
        
        with open("output.txt", "a") as txt_file:
            txt_file.write(f"\n{'SECTION: '+ section:^154}\n")
            txt_file.write(" _________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________ _______ \n")
            txt_file.write("|   STUDENT ID    |             NAME             | Attendance |           QUIZZES           |  MIDTERM  | FINAL EXAM | FINAL GRADE | RATING | STATUS |\n")
            txt_file.write(" _________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________ _______ |\n")
            txt_file.write("|                 |                              |            |  1  |  2  |  3  |  4  |  5  |           |            |             |        |        |\n")
            txt_file.write(" _________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________ _______ |\n")

            for person in data_record:
                if person['section'] == section:

                    status_students_report()
                    txt_file.write(f"|{person['student_id']:^17}|{person['name']:^30}|{person['attendance']:^12}|{person['quiz_1']:^5}|{person['quiz_2']:^5}|{person['quiz_3']:^5}|{person['quiz_4']:^5}|{person['quiz_5']:^5}|{person['midterm']:^11}|{person['final_exam']:^12}|{person['final_grade']:^13}|{person['rating']:^8}|{person['status']:^8}|\n")
                    txt_file.write(" _________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________\n")


# def section_compare_table(data_record):

#     section_list = identify_sections(data_record) #calls the section lists

#     with open("output.txt", "a") as txt_file:        
#         txt_file.write(" ______________ _____ _____ _____ _____ _____ _________ _______ _________\n")
#         txt_file.write("|   SECTION    |  1  |  2  |  3  |  4  |  5  | MIDTERM | FINALS| OVERALL |\n")
#         txt_file.write(" ______________ _____ _____ _____ _____ _____ _________ _______ _________\n")

#         for person in data_record:
#             if person['section'] == section:

#                 status_students_report()
#                 txt_file.write(f"|{person['student_id']:^17}|{person['name']:^30}|{person['attendance']:^12}|{person['quiz_1']:^5}|{person['quiz_2']:^5}|{person['quiz_3']:^5}|{person['quiz_4']:^5}|{person['quiz_5']:^5}|{person['midterm']:^11}|{person['final_exam']:^12}|{person['final_grade']:^13}|{person['rating']:^8}|{person['status']:^8}|\n")
#                 txt_file.write(" _________________ ______________________________ ____________ _____________________________ ___________ ____________ _____________ ________\n")


generate_txtreport(students)

print("the program runs!!")


