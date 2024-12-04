[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=16989114)

# DATASCI 217 FINAL EXAM
### Belinda Chen

## Question 1: Data Preparation with Command-Line Tools
The goal of part 1 was to clean the raw data (ms_data_dirty.csv) to remove inconsistencies and extract the essential columsn for further analysis. The steps taken included:
- using grep and sed to remove the comments, empty lines, and additional punctuation
- extracted the required columns: patient_id, visit_date, age, education_level, walking_speed
- filtered for rows with walking speed between 2.0 and 8.0 ft/s
- assigned unique insurance types (basic, premium, platinum) to each patient 
- saved the clean data as ms_data.csv


