# ETL_pipeline_for_Charity
Built an ETL pipeline that cleans, standardises, and merges supporter data (donations, events, campaigns) into one analytics-ready dataset.

**Project Title:**  **Charity Data ETL Pipeline**
**Overview**
This project showcases a complete Extract, Transform, and Load (ETL) pipeline built with Python to process raw, messy data from a fictional charity organization. The goal was to clean, merge, and transform data from three separate sources—donations, events, and campaigns—into a single, unified dataset ready for analytics.

This project uses sample data for demonstration purposes, ensuring full compliance with GDPR and other data privacy regulations.

**Data Sources**
The pipeline processes data from three separate CSV files, each with its own data quality challenges:

donations.csv: Contains donation amounts, dates, and campaign IDs. It has inconsistent data formats and duplicated supporter_id columns.

events.csv: Records supporter participation in events. It has inconsistent supporter ID column names (user_id and User ID) and various date formats.

campaigns.csv: Provides details about each fundraising campaign. This file has inconsistent date formats and trailing whitespace in text fields.

**ETL Process & Key Challenges**
The Python script etl_pipeline.py performs the following steps:

Extract: The script reads the three CSV files into pandas DataFrames.

Transform: This is the core of the project. I implemented logic to handle several real-world data issues:

Inconsistent Column Names: Standardized Supporter ID, user_id, and User ID into a single, consistent supporter_id column for seamless merging.

Missing and Inconsistent Data: Cleaned up the donation_amount column by filling in missing values with 0.

Mixed Data Types: Standardized all date columns (e.g., donation_date, event_date) to a unified YYYY-MM-DD format, handling multiple input formats gracefully.

Merging Datasets: Performed a LEFT JOIN on the DataFrames using a common key (supporter_id) to create a comprehensive table that links donations and event participation to specific campaigns.

Load: The final, cleaned DataFrame is loaded into two different destinations to show versatility:

analytics_ready_data.csv: A clean CSV file that can be easily shared or used in a spreadsheet program.

charity_data.db: A SQLite database, demonstrating the ability to load data into a structured database for SQL-based analysis.

**Tools & Technologies**

Python: The primary language for the ETL script.

Pandas: Used for all data manipulation, cleaning, and transformation tasks.

SQLAlchemy: Used to establish a connection and load the data into the SQLite database.

Git & GitHub: Used for version control and project hosting.

**How to Run the Project**

Clone the repository to your local machine:
git clone https://github.com/Kaviya-Mahendran/ETL_pipeline_for_Charity.git

Navigate to the project directory.

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

**Install the required libraries:**
pip install -r requirements.txt (Note: You can create this file by running pip freeze > requirements.txt)

Run the ETL pipeline:
python3 etl_pipeline.py

The script will generate analytics_ready_data.csv and charity_data.db in the project folder.
