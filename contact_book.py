# Imports
import json
import csv
import os
from colorama import Fore, init
init(autoreset=True)

# Global variable and colors
CONTACTS_FILE = "contacts.json"
TITLE = Fore.CYAN
OPTION = Fore.YELLOW
SUCCESS = Fore.GREEN
ERROR = Fore.RED
WARNING = Fore.MAGENTA
INFO = Fore.BLUE
TEXT = Fore.LIGHTBLACK_EX

# Class definition
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


# Functions
def add_contact(contacts):
    print(TITLE + "\n=== Add New Contact ===")

    #Take informations
    name = input(TEXT + "Enter full name: ").strip()
    phone = input(TEXT + "Enter phone number: ").strip()
    email = input(TEXT + "Enter email address: ").strip()

    # Check all fiels filled
    if not name or not phone or not email:
        print(ERROR + "All fields are required.")
        return
    
    # Check if contact already exists
    for c in contacts:
        if c.name.lower() == name.lower():
            print(WARNING + f'Error: Contact "{name}" already exists.')
            return
    
    # Check valid email
    if "@" not in email or "." not in email:
        print(ERROR + "Invalid email format. Example: hello@world.com")
        return
    
    # Check phone number
    if not (phone.startswith("+") and phone[1:].isdigit()):
        print(ERROR + "Invalid phone number format. Example: +123456789")
        return
    
    # Then add contact
    new_contact = Contact(name, phone, email)
    contacts.append(new_contact)

    # Save after adding
    save_contacts(contacts)
    
    print(SUCCESS + f'Contact "{name}" added successfully!')


def view_contacts(contacts):
    print(TITLE + "\n=== All Contacts ===")

    if not contacts:
        print(WARNING + "No contacts found.")
        return

    # Order contacts by name
    sorted_contacts = sorted(contacts, key=lambda c: c.name.lower())

    for i, c in enumerate(sorted_contacts, start=1):
        print(f"{i}. {c.name} | {c.phone} | {c.email}")

    print(INFO + "=======================")
    if len(sorted_contacts)==1:
        print(INFO + f"Total: {len(sorted_contacts)} contact")
    else :
        print(INFO + f"Total: {len(sorted_contacts)} contacts")
    

def search_contact(contacts):
    print(TITLE + "\n=== Search Contact ===")
    name = input(TEXT + "Enter name to search: ").strip()

    if not name:
        print(WARNING + "Search term cannot be empty.")
        return

    # Recherche insensible à la casse
    matches = [c for c in contacts if name.lower() in c.name.lower()]

    if not matches:
        print(ERROR + f'No contact found with name containing "{name}".')
        return

    # Affichage des résultats
    if len(matches)==1:
        print(INFO + f'\nFound {len(matches)} result:')
    else:
        print(INFO + f'\nFound {len(matches)} results:')
    
    for i, c in enumerate(matches, start=1):
        print(OPTION + f"{i}. {c.name} | {c.phone} | {c.email}")


def edit_contact(contacts):
    print(TITLE + "\n=== Edit a Contact ===")
    name = input(TEXT + "Enter the name of the contact to edit: ").strip()

    # Searching contacts
    matches = [c for c in contacts if name.lower() in c.name.lower()]

    if not matches:
        print(WARNING + f'No contact found with name containing "{name}".')
        return

    # Show if several contacts are found
    if len(matches) > 1:
        print(INFO + f'Found {len(matches)} contacts:')
        for i, c in enumerate(matches, start=1):
            print(OPTION + f"{i}. {c.name} | {c.phone} | {c.email}")

        try:
            choice = int(input(TEXT + "Enter the number of the contact to edit: "))
            if choice < 1 or choice > len(matches):
                print(ERROR + "Invalid selection.")
                return
            contact_to_edit = matches[choice - 1]
        except ValueError:
            print(ERROR + "Invalid input.")
            return
    else:
        contact_to_edit = matches[0]

    # Show current info
    print(TITLE + "\nCurrent contact info:")
    print(INFO + f"Name:  {contact_to_edit.name}")
    print(INFO + f"Phone: {contact_to_edit.phone}")
    print(INFO + f"Email: {contact_to_edit.email}")

    # Ask for new info
    new_name = input(TEXT + "Enter new name (leave blank to keep current): ").strip()
    new_phone = input(TEXT + "Enter new phone (leave blank to keep current): ").strip()
    new_email = input(TEXT + "Enter new email (leave blank to keep current): ").strip()

    # Update and if blank, do not change
    if new_name:
        contact_to_edit.name = new_name
    if new_phone:
        if not (new_phone.startswith("+") and new_phone[1:].isdigit()):
            print(ERROR + "Invalid phone number format. Example: +123456789")
            return
        contact_to_edit.phone = new_phone
    if new_email:
        if "@" not in new_email or "." not in new_email:
            print(ERROR + "Invalid email format.")
            return
        contact_to_edit.email = new_email

    # Save modifications
    save_contacts(contacts)

    print(SUCCESS + f'\nContact "{contact_to_edit.name}" updated!')


def delete_contact(contacts):
    print(TITLE + "\n=== Delete a Contact ===")
    name = input(TEXT + "Enter the name of the contact to delete: ").strip()

    # Looking for contacts with this name
    matches = [c for c in contacts if name.lower() in c.name.lower()]

    if not matches:
        print(WARNING + 'Contact not found.')
        return

    # Show if several contacts are found
    if len(matches) > 1:
        print(INFO + f'Found {len(matches)} contacts:')
        for i, c in enumerate(matches, start=1):
            print(OPTION + f"{i}. {c.name} | {c.phone} | {c.email}")

        try:
            choice = int(input(TEXT + "Enter the number of the contact to delete: "))
            if choice < 1 or choice > len(matches):
                print(ERROR + "Invalid selection.")
                return
            contact_to_delete = matches[choice - 1]
        except ValueError:
            print(ERROR + "Invalid input.")
            return
    else:
        # If there is only one name found
        contact_to_delete = matches[0]

    # Confirmation
    confirm = input(TEXT + f'Are you sure you want to delete "{contact_to_delete.name}"? (yes/no): ').strip().lower()
    if confirm != "yes":
        print(ERROR + "Deletion canceled.")
        return

    # Suppression of the contact
    contacts.remove(contact_to_delete)
    save_contacts(contacts)

    print(SUCCESS + 'Contact deleted!')


def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            data = json.load(file)
            return [Contact(c["name"], c["phone"], c["email"]) for c in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(ERROR + "Error reading contacts file. Starting with an empty list.")
        return []


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump([c.to_dict() for c in contacts], file, indent=2)


def export_to_csv(contacts):
    print(TITLE + "\n=== Export Contacts to CSV ===")

    if not contacts:
        print(WARNING + "No contacts to export.")
        return

    filename = input(TEXT + "Enter CSV file name (default: contacts.csv): ").strip()
    if not filename:
        filename = "contacts.csv"

    # Ensure the filename ends with .csv
    if not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Name", "Phone", "Email"])
            # Write each contact
            for c in contacts:
                writer.writerow([c.name, c.phone, c.email])

        print(SUCCESS + f"Contacts successfully exported to '{filename}'.")
    except Exception as e:
        print(ERROR + f"Error exporting contacts: {e}")

# Main program
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(TEXT + "\nPress ENTER to continue...")

def main():
    contacts = load_contacts()
    while True:
        clear()
        print(TITLE + "===============================")
        print(TITLE + "Contact Book")
        print(TITLE + "===============================")
        print(OPTION + "1. Add Contact")
        print(OPTION + "2. View All Contacts")
        print(OPTION + "3. Search Contact by Name")
        print(OPTION + "4. Edit Contact")
        print(OPTION + "5. Delete Contact")
        print(OPTION + "6. Export contacts to .csv")
        print(OPTION + "7. Save and Exit")
        choice = input(TEXT + "Choose an option (1-7): ")

        if choice == "1":
            add_contact(contacts)
            pause()
        elif choice == "2":
            view_contacts(contacts)
            pause()
        elif choice == "3":
            search_contact(contacts)
            pause()
        elif choice == "4":
            edit_contact(contacts)
            pause()
        elif choice == "5":
            delete_contact(contacts)
            pause()
        elif choice == "6":
            export_to_csv(contacts)
            pause()
        elif choice == "7":
            save_contacts(contacts)
            print(INFO + "Saving contacts to file...")
            print(SUCCESS + "Data saved. Goodbye!")
            break

        else:
            print(ERROR + "Invalid choice")

if __name__ == "__main__":
    main()
