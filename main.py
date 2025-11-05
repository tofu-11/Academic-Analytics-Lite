import ingest


choice = input("Pl")

match choice:
    case "View Files":
        print(list_files())
    case "Create new file":

    case _: