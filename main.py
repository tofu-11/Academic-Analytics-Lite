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
        print("5. Export per Section")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            ingest.list_files()
            
        
        elif choice == "2":
            print("Which file?")
            ingest.list_files()
            try:
                num = int(input())
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            reports.analysis_report_output(file_list[num-1])

        elif choice == "3":
            print("Which file?")
            ingest.list_files()
            try:
                num = int(input())
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            print("Which sections?")
            section_choice = []
            section_list = ingest.list_sections(file_list[num-1])
            while True:
                for j in range(len(section_list)):
                    print(j+1, ". ", section_list[j])
                print("Type 0 if done.")
                try:
                    sec_choice = int(input())
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if sec_choice == 0:
                    break
                if sec_choice < 1 or sec_choice > len(section_list):
                    print("Choice out of range. Try again.")
                    continue
                selected = section_list[sec_choice-1]
                if selected in section_choice:
                    print("You've already selected that section. Choose a different one.")
                    continue
                section_choice.append(selected)
            reports.compare_output(section_choice, file_list[num-1])
        
        elif choice == "4":
            file_choice = []
            print("Please choose two files to view improvements: ")
            chosen_indices = set()
            while len(file_choice) < 2:
                ingest.list_files()
                try:
                    num = int(input())
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if num < 1 or num > len(file_list):
                    print("Choice out of range. Try again.")
                    continue
                if num in chosen_indices:
                    print("You've already chosen that file. Please pick a different file.")
                    continue
                chosen_indices.add(num)
                file_choice.append(file_list[num-1])
            
            reports.improvement_output(file_choice)
            
        elif choice == "5":
            print("Please choose a file to export per-section statistics: ")
            ingest.list_files()
            try:
                num = int(input())
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if num < 0 or num > len(file_list):
                print("Choice out of range. Try again.")
                continue
            reports.export_per_section(file_list[num-1])
            
        elif choice == "6":
            print("\nExiting program... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        enter = input("\nPress Enter to continue...")

