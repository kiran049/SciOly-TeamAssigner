# SciOly-TeamAssigner
Create sci oly teams based on students' partner preferences and event preferences.

## How To Install and Setup

1. extract as zip
2. replace 'form.csv' with your own form answers reference 'CSV Formatting' for help with how to properly do this
3. install the pandas library, used for CSV and XLSX analyzation:
   `pip install pandas`

## How to format the CSV file
The CSV file must be formatted a certain way as the code processes specific cells, and if these do not match up then the code will be useless (this will be changed in the future). **Reference the example CSV file provided.**
Make sure in the CSV file that:
* All **names** in the name field are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **event**s in the event fields are **consistent with their formatting and do not vary** (punctuation, spaces).
* All **partners in the partner fields reference a name that can be EXACTLY linked back to a name in the name column.** The formatting cannot differ for ANY names wherever they may be.
* Any fields where there is not meant to be any data must be left blank.
**Make sure the example CSV file matches yours. The rows and columns should have identical fields.**
