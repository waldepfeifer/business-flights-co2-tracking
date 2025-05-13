import pandas as pd
import sys
import duckdb
from haversine import haversine

con = duckdb.connect("flights.ddb")

def cf_routes_airports(con,date_from,date_to):
# Get data from the tables company_flights, routes and airports of the flights.dbb
    query = '''

    SELECT
        cf.department,
        cf.route_index,
        cf.flight_date,
        CAST(src_airport.longitude as FLOAT) AS source_longitude,
        CAST(src_airport.latitude as FLOAT) AS source_latitude,
        CAST(dest_airport.longitude as FLOAT) AS destination_longitude,
        CAST(dest_airport.latitude as FLOAT) AS destination_latitude,
    FROM
        company_flights cf
    LEFT JOIN
        routes r
        ON cf.route_index = r.index
    LEFT JOIN
        airports src_airport
        ON r.source_id = src_airport.id
    LEFT JOIN
        airports dest_airport
        ON r.dest_id = dest_airport.id
    WHERE
        cf.flight_date >= ? AND cf.flight_date <= ?

    '''
    cf_routes_airports_df = con.execute(query, [date_from, date_to]).df()
    return cf_routes_airports_df

def calculate_distance(row): # Haversine formula to calculate km
    source = (row["source_latitude"], row["source_longitude"])
    destination = (row["destination_latitude"], row["destination_longitude"])
    km = haversine(source, destination)

    return km

def calculate_co2(row):
    co2_per_km_per_passenger = 0.1
    co2_result = row["distance_km"] * co2_per_km_per_passenger

    return co2_result

def co2_aggregation(df):
    aggregated_df = df.groupby("department", as_index=False)["co2_footprint"].sum()
    aggregated_df["co2_footprint"] = aggregated_df["co2_footprint"].round().astype(int)

    return aggregated_df

def csv_generator(df,date_from,date_to):
    filename = f"co2_report_{date_from}_{date_to}.csv"
    df.to_csv(filename, index=False)

    return f"Export of {filename} finalized"

def main():
    if len(sys.argv) != 3:
        print("Usage: python co2_report.py DATE_FROM DATE_TO")
        sys.exit(1)
    
    date_from = sys.argv[1]
    date_to = sys.argv[2]

    print("Data joined from company_flights, routes and airports -------------------")
    cf_routes_airports_df = cf_routes_airports(con,date_from,date_to)
    print(cf_routes_airports_df)
    print()

    print("Calculate distance_km column -------------------")
    distance_df = cf_routes_airports_df.copy()
    distance_df["distance_km"] = distance_df.apply(calculate_distance, axis=1)
    print(distance_df)
    print()

    print("Calculate co2_footprint -------------------")
    footprint_df = distance_df.copy()
    footprint_df["co2_footprint"] = footprint_df.apply(calculate_co2, axis=1)
    print(footprint_df)
    print()

    print("Aggregate by dimension department and measure co2_footprint -------------------")
    aggregated_df = co2_aggregation(footprint_df)
    print(aggregated_df)
    print()
    print(csv_generator(aggregated_df,date_from,date_to))


if __name__ == "__main__":
    main()

