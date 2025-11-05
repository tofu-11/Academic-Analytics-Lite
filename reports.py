

def space_counter(data):
    for person in data:
        N_spaces = len(person["name"])
        #checker
        print(f"Name spaces = {N_spaces}")

def generate_report(data_record):

    with open("output.txt", "w") as txt_file:
        txt_file.write(" ---------------------------------------------------------------------DATA REPORTS---------------------------------------------------------------------")
        txt_file.write(" _________________ ______________________________ ______________________ _____________________________ ___________ ____________ _____________ ________ ")
        txt_file.write("|   STUDENT ID    |            NAME              |      SECTION         | Attendance_present|           QUIZZES           |  MIDTERM  | FINAL EXAM | FINAL GRADE | RATING |")
        txt_file.write("|                 |                              |                      |__1__|__2__|__3__|__4__|__5__|           |            |             |        |")
        txt_file.write("|_2024-00000-CM-0_|_Sample-name-30-characters____|_Program+year_section_|_000_|_000_|_000_|_000_|_000_|____001____|_____001____|___001.00____|_PASSED_|")

        for person in data_record:
            txt_file.write(f"{person[student_id]^17}|{person[name]^30}|{person[section]^22}|{person[quiz_1]^5}|{person[quiz_2]^5}|{person[quiz_3]^5}|{person[quiz_4]^5}|{person[quiz_5]^5}|{person[midterm]^11}|{person[final_exam]^12}|{person[final_grade]^13}|")
        


print("the program runs!!")


