import pandas as pd
import sys
import duckdb

con = duckdb.connect("flights.ddb")

def create_company_flights_table(con):
    
    query = """
    
    CREATE TABLE IF NOT EXISTS company_flights (
        employee_id INTEGER,
        department TEXT,
        route_index INTEGER,
        flight_date TEXT)
        
    """
    con.sql(query)

    record_count = con.sql("SELECT COUNT(*) FROM company_flights").fetchone()[0]
    
    return f"Table company_flights created or available with {record_count} records"

def load_csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    
    return df

def remove_duplicates(df):
    clean_df = df.drop_duplicates()

    return clean_df

def records_not_in_db(df,con): # Left exclusive join
    select_query = """ SELECT * FROM company_flights """
    company_flights_df = con.sql(select_query).df()
    
    merged = pd.merge(df, company_flights_df, how='left', indicator=True)
    records_not_in_db = merged[merged['_merge'] == 'left_only'].drop(columns='_merge')
    
    return records_not_in_db

def insert_new_records(df,con):
    con.register('df', df)
    insert_query = """ INSERT INTO company_flights FROM df """
    con.sql(insert_query)

    record_count = con.sql("SELECT COUNT(*) FROM df").fetchone()[0]

    return f"{record_count} records inserted into company_flights table"

def main():
    if len(sys.argv) != 2:
        print("Usage: python flights_upload.py path_to_file")
        sys.exit(1)
    
    file_path = sys.argv[1]
    print()
    print(create_company_flights_table(con))
    print()
    print("Records in company_flights table -------------------------")
    print(con.sql("SELECT * FROM company_flights"))
    df = load_csv_to_dataframe(file_path)
    print()
    print("Data from File Path: "+ file_path + " loaded into df ----------------------")
    print(df)
    print()
    clean_df = remove_duplicates(df)
    print("Clean df after removing duplicates in file ----------------------")
    print(clean_df)
    print()
    records_not_in_db_df = records_not_in_db(clean_df,con)
    print("Records not available in company_flights table ----------------------")
    print(records_not_in_db_df)
    print()
    print(insert_new_records(records_not_in_db_df,con))
    print()
    print("Data in company_flights table after insert ----------------------")
    print(con.sql("SELECT * FROM company_flights"))

if __name__ == "__main__":
    main()

