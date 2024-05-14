import re

TAG_1, TAG_2, TAG_3, TAG_4 = "\n"+"-"*50+"\n", "\n\t- ", "\n\t- ", ": "

def export_contacts(contacts):
    x_file = input("Enter name of export file: ")
    with open(x_file,"w") as file:
        file.write("CONTACT BOOK" + TAG_1)
        for email,data in contacts.items():
            file.write(email + TAG_2 + TAG_3.join(field+TAG_4+info for field,info in data.items()) + TAG_1)
        file.write(" "*47 + "END")

def import_contacts(contacts):
    i_file = input("Enter name of import file: ")
    with open(i_file,"r") as file:
        for line in file.read().split(TAG_1)[1:-1]:
            email,data = line.split(TAG_2,1)
            if email not in contacts:
                contacts[email] = {}
            for field, info in (x.split(TAG_4,1) for x in data.split(TAG_3)):
                if field not in contacts[email]:
                    contacts[email][field] = info

def valid_email(email):
    return bool(re.match(r"^\w[\+\.\w-]*@([\w-]+\.)*\w+[\w-]*\.([a-z]{2,4}|\d+)$", email))

def add_contact(contacts):
    email = input("Enter contact email: ").lower().strip()
    if not valid_email(email):
        print("Inavalid email...")
        return
    if email in contacts:
        print("A contact already exists with that email...")
        return
    name = input("Enter contact name: ").strip()
    contacts[email] = {"name": name}
    while True:
        command = input("Enter additional info (y/n)?").strip().lower()
        if command and command[0] == "y":
            field = input("What field would you like to add: ").strip().lower()
            info = input("What would you like to enter: ")
            contacts[email][field] = info
        else:
            break

def delete_contact(contacts):
    to_del = input("Enter email of contact to delete: ").lower().strip()
    if to_del in contacts:
        del contacts[to_del]
    else:
        print("No contact found with that email...")

def run_update(contacts, email):
    while True:
        command = input("add, edit, or delete field; or cancel? ").strip().lower()
        if command == "delete":
            field = input("Enter field: ").strip().lower()
            if field in contacts[email]:
                del contacts[email][field]
                break
            else:
                print("Field not found...")
        elif command == "add":
            field = input("Enter field: ").strip().lower()
            if field not in contacts[email]:
                info = input("Enter info: ")
                contacts[email][field] = info
                break
            else:
                print("Field already exists...")
        elif command == "edit":
            field = input("Enter field: ").strip().lower()
            if field in contacts[email]:
                info = input("Enter updated info: ")
                contacts[email][field] = info
                break
            else:
                print("Field not found...")
        elif command == "cancel":
            break
        else:
            print("Command unrecognized...")


def update_contact(contacts):
    while True:
        email = input("Enter email of contact or cancel: ").strip().lower()
        if email == "cancel":
            break
        elif email in contacts:
            run_update(contacts, email)
            break
        else:
            print("Email not found...")

def view_contacts(contacts):
    command = input("all or search: ").strip().lower()
    if command == "all":
        for email, data in contacts.items():
            print(email)
            for field, info in data.items():
                print(f" - {field}: {info}")
    elif command == "search":
        email = input("Enter email: ").strip().lower()
        if email in contacts:
            for field, info in contacts[email].items():
                print(f" - {field}: {info}")
        else:
            print("Email not found...")

def contact_app():
    try:
        with open(".contact_dict.txt", "r") as file:
            try:
                contacts = eval(file.read())
            except Exception:
                print("Saved contact data in unreadable...")
                command = input("Proceed and overwrite contact_dict (y/n)? ").lower()
                if command and command[0] == "y":
                    contacts = {}
                else:
                    return
    except Exception:
        contacts = {}
    while True:
        command = input("add, update, delete, view, export, import, or quit? ")

        if command == "add":
            add_contact(contacts)
        elif command == "update":
            update_contact(contacts)
        elif command == "delete":
            delete_contact(contacts)
        elif command == "view":
            view_contacts(contacts)
        elif command == "export":
            export_contacts(contacts)
        elif command == "import":
            import_contacts(contacts)
        elif command == "quit":
            with open(".contact_dict.txt", "w") as file:
                file.write(str(contacts))
            break
        else:
            print("Command unrecognized...")

contact_app()