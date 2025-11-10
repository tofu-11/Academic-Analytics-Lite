import ingest
from ingest import file_list
import os
import reports
import analyze

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
        clear()
        print("\n==============================")
        print(" Student Record Management ")
        print("==============================")
        print("1. View File List")
        print("2. Produce Report & Analysis")
        print("3. Compare")
        print("4. View Improvements")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            ingest.list_files()
            test = input()
        
        elif choice == "2":
            print("Which file?")
            ingest.list_files()
            num = int(input())
            reports.analysis_report_output(file_list[num-1])

        elif choice == "3":
            print("Which file?")
            ingest.list_files()
            num = int(input())
            print("Which sections?")
            section_choice = []
            section_list = ingest.list_sections(file_list[num-1])
            while True:
                for j in range(len(section_list)):
                    print(j+1, ". ", section_list[j])
                print("Type 0 if done.")
                sec_choice = int(input())
                if sec_choice != 0:
                    section_choice.append(section_list[sec_choice-1])
                else:
                    break
            reports.compare_output(section_choice, file_list[num-1])
        
        elif choice == "4":
            file_choice = []
            print("Please choose two files to view improvements: ")
            for i in range(2):
                ingest.list_files()
                num = int(input())
                file_choice.append(file_list[num-1])
            reports.improvement_output(file_choice)
            
        elif choice == "5":
            print("\nExiting program... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

