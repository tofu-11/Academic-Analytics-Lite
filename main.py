import ingest

file_list = ingest.return_list
while True:
        print("\n==============================")
        print(" Student Record Management ")
        print("==============================")
        print("1. View File List")
        print("2. Produce Report & Analysis")
        print("3. Compare")
        print("4. View Improvements")
        print("4. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            ingest.list_files()
        
        elif choice == "2":
            print("Which file?")
            num = input(int(ingest.list_files()))
            
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

            
        elif choice == "4":
            print("\nExiting program... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

