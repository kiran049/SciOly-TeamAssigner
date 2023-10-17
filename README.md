# SciOly-TeamAssigner
Create sci oly teams based on students' partner preferences and event preferences.

## How To Install and Setup

1. extract as zip
2. replace 'form.csv' with your own form answers reference [CSV Formatting](https://github.com/kiran049/SciOly-TeamAssigner#how-to-format-the-csv-file) for help with how to properly do this
3. install the pandas library, used for CSV analysis:
   `pip install pandas`
4. install the openpyxl library, used for Excel creation:
   `pip install openpyxl`

## How to format the CSV file
The CSV file must be formatted a certain way as the code processes specific cells, and if these do not match up then the code will be useless (this will be changed in the future). **Reference the example CSV file provided.**
The example CSV file was downloaded from a Google Form, this form can be seen here: [Form Outline](https://forms.gle/mSxMeamCyrZjJw727)
Make sure in the CSV file that:
* All **names** in the name field are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **events** in the event fields are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **partners in the partner fields reference a name that can be EXACTLY linked back to a name in the name column.** The formatting cannot differ for ANY names wherever they may be.
* Any fields where there is not meant to be any data must be left blank.
**Make sure the example CSV file matches yours. The rows and columns should have identical fields.**

## How to Use the Project
In TeamSorter.py, make sure on this line `form = pd.read_csv('form.csv')` that 'form.csv' is instead the name of your CSV file in the project folder. Ensure that pandas is installed and all formatting is correct, then run the program. The program will create 2 Excel spreadsheets. One with all all the students and the teams that they are on. The other Excel spreadsheet contains all the teams, along with which event they're doing, and the members that belong to the team.
