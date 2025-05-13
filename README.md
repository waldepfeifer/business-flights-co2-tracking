<img width="1317" alt="image" src="https://github.com/user-attachments/assets/6eb0353a-e510-499b-ac9e-6ff68e54a377" />

# Business Flights CO₂ Tracking

## 📖 Project Overview

This project helps **Company XYZ** track and report the **CO₂ emissions of their business flights**. The system uses two automated Python processes:

- **Data ingestion and deduplication** of monthly flight reports
- **Calculation and reporting** of CO₂ emissions by department for a given date range

The project uses **DuckDB** for lightweight database storage and the **Haversine formula** to compute flight distances.

## 🎯 Objectives

- Automate ingestion of monthly flight data
- Prevent duplicate flight records
- Calculate distances between airports using latitude and longitude
- Estimate CO₂ footprint (0.1 kg of CO₂ per km per passenger)
- Generate CSV reports of CO₂ emissions by department

## 🛠 Technologies Used

- Python 3.x
- DuckDB
- Pandas
- Haversine library
- Command-line scripts

## 📂 Project Structure

flights_upload.py  
co2_report.py  
flights.ddb (generated database file)  
README.md  
requirements.txt

## 🚀 How It Works

### 1️⃣ Upload Flight Data

The **flights_upload.py** script reads a monthly CSV file of flights and updates the database without creating duplicates.

The flight file must include:

- employee_id (integer)
- department (text)
- route_index (integer)
- flight_date (YYYY-MM-DD as text)

Run the script:

(Here you would normally use a bash command like)  
python3 flights_upload.py path_to_file.csv

### 2️⃣ Generate CO₂ Report

The **co2_report.py** script generates a CO₂ footprint report for a date range.

Run the script:

(Here you would normally use a bash command like)  
python3 co2_report.py YYYY-MM-DD YYYY-MM-DD

Example:  
python3 co2_report.py 2024-01-01 2024-03-31

A file named  
co2_report_2024-01-01_2024-03-31.csv  
will be created with columns:

- department
- co2_footprint (total kg of CO₂ for flights in the period)

### How the CO₂ Is Calculated

The distance between source and destination airports is calculated using the **Haversine formula** from the haversine library.  
CO₂ emissions are then calculated as:

distance_km * 0.1 kg CO₂ per passenger

## 📝 Example Workflow

1. Monthly CSV files are uploaded via flights_upload.py
2. A quarterly report is generated via co2_report.py
3. The company can use the reports for carbon offset planning

## ⚠ Notes

- Duplicate records (identical in all fields) are automatically filtered
- The routes and airports tables must exist and be correctly populated
- Script assumes all route_index and airport IDs are valid
- No user input validation is required (as per assignment spec)

## 📜 License

This project is licensed under the MIT License. See LICENSE file for details.
