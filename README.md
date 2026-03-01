## Overview
This project demonstrates two approaches to solving a data aggregation problem:
1. A pure SQL-based solution
2. A Pandas-based solution

Both solutions extract total item quantities purchased by customers aged 18–35
and export the results to CSV format.

## Technologies Used
- Python 3
- SQLite
- Pandas

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```
## How to Run the Scripts
All scripts must be run from the project root directory:
cd data-engineer-assignment

## Run SQL Solution
- python sql_solution.py
This generates output_sql.csv (in the same directory)

## Run Pandas Solution
- python pandas_solution.py
This generates output_pandas.csv (in the same directory)

## Output Format
Both scripts produce CSV files
