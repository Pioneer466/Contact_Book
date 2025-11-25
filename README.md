# Project: Contact Book CLI Application
This program is a command-line contact book that allows users to manage and store contacts directly from the terminal.
It supports creating, viewing, searching, editing, deleting, and exporting contacts, all saved locally in a JSON file.

How to Run the Program:
1. Make sure you have Python 3 installed on your system.

2. Open your terminal in the folder containing the file contact_book.py: (>cd 'file_path')
If needed, install the required library:
=> pip install colorama

3. Run the program:
=> python contact_book.py

All data is stored persistently in contacts.json, which is automatically created and updated in the same directory.

Extra Functionality:

    - Colored design (via colorama) for improved visibility.
    - Input validation for emails, phone numbers, and duplicates.
    - Alphabetical sorting of contacts for easier browsing.
    - Export to CSV : Export all contacts to a .csv file.

Files in the Project:

    - contact_book.py => Main Python script (the program).
    - contacts.json => Automatically generated data file for storing your contacts.
    - (Afterwards) contacts.csv => Generated when you export contacts to CSV.
