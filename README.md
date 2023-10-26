# SciOly-TeamAssigner
A console based app that creates sci oly teams based on students' partner preferences and event preferences. The program can consider **overlapping events, a max amount of teams per event, and can detect if there aren't any teams for a certain event.**


## GUI Version
![image](https://github.com/kiran049/SciOly-TeamAssigner/assets/98996914/9c2a393c-fdba-4327-8831-f160db9cad13)
If you wish to use the GUI version of this program use this repository: [GUI Repository](https://github.com/kiran049/SciOly-TeamAssigner/tree/GUI)

## How To Install and Setup

1. extract as zip
2. replace 'SciOly.csv' with your own form answers reference [CSV Formatting](https://github.com/kiran049/SciOly-TeamAssigner#how-to-format-the-csv-file) for help with how to properly do this
3. install the pandas library, used for CSV analysis:
   `pip install pandas`
4. install the openpyxl library, used for Excel creation:
   `pip install openpyxl`

## How to format the CSV file
The CSV file must be formatted a certain way as the code processes specific cells, and if these do not match up then the code will be useless (this will be changed in the future). **Reference the example CSV file provided (form.csv).**
The example CSV file was downloaded from a Google Form, this form can be seen here: [Form Outline](https://forms.gle/mSxMeamCyrZjJw727). The program only supports CSV files extracted from this Google Form.
Make sure in the CSV file that:
* All **names** in the name field are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **events** in the event fields are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **partners in the partner fields reference a name that can be EXACTLY linked back to a name in the name column.** The formatting cannot differ for ANY names wherever they may be.
* Any fields where there is not meant to be any data must be left blank.
**Make sure the example CSV file matches yours. The rows and columns should have identical fields.**

## How to Use the Project
In TeamSorter.py, make sure on this line `form = pd.read_csv('form.csv')` that 'form.csv' is instead the name of your CSV file in the project folder. Ensure that pandas is installed and all formatting is correct, then run the program. The program will create 2 Excel spreadsheets. One with all all the students and the teams that they are on. The other Excel spreadsheet contains all the teams, along with which event they're doing, and the members that belong to the team.

## eventOverlaps.csv
By default, the project uses the overlapping events listed in this image (student cannot have multiple events from the same row). You can use your own overlapping events if you wish by editing the attached `eventOverlaps.csv` file.
![OverlappingEvents](https://github.com/kiran049/SciOly-TeamAssigner/assets/98996914/26288038-c59b-44be-a306-e3be31db71cb)

## allEvents.csv
This project will check that there is at least 1 team for each event, and it will write a warning in `exceptions.txt`.

## exceptions.txt
All warnings will be written here and in the console. Any students who have overlapping events, any teams that were deleted due to being over the max team per event limit, or any events that don't have teams will be documented here.
