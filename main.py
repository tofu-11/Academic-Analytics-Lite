import ingest

file_list = ingest.return_list
while True:
        print("\n==============================")
        print(" Student Record Management ")
        print("==============================")
        print("1. View File List")
        print("2. Produce Report & Analysis")
        print("3. Compare")
        print("4. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            ingest.list_files()
        
        elif choice == "2":
            print("Which file?")
            num = input(int(ingest.list_files()))

        elif choice == "3":
             
        elif choice == "4":
            print("\nExiting program... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

