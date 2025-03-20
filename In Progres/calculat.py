"""
Author: Michael Gledhill
Name: calculat.py
"""

import pandas as pd
import math
import os
import sys

# Load CSV containing airport data
def load_airports():
    """Load airport data from CSV file."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_path, "airports.csv")
    
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        print("Error: airports.csv not found.")
        return None

def get_airport_info(df, code):
    """Retrieve airport information by ICAO code."""
    airport = df[df['ident'] == code.upper()]
    return None if airport.empty else airport.iloc[0]

def calculate_heading(lat1, lon1, lat2, lon2):
    """Calculate the heading direction between two coordinates."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing) % 360  # Normalize to 0-360
    return round(bearing, 2)

def validate_altitude(altitude, heading):
    """Check if altitude follows IFR semicircular rules based on direction of flight."""
    if 0 <= heading < 180:
        return "Incorrect altitude!" if altitude % 2000 == 0 else "Altitude is correct."
    else:
        return "Incorrect altitude!" if altitude % 2000 != 0 else "Altitude is correct."

def process_flight_plan(departure, destination, altitude):
    """Process the flight plan and validate heading and altitude."""
    df = load_airports()
    if df is None:
        return {"error": ["Unable to load airport data."]}

    errors = []

    airport1 = get_airport_info(df, departure)
    airport2 = get_airport_info(df, destination)

    if airport1 is None:
        errors.append(f"Departure airport '{departure}' not found.")
    if airport2 is None:
        errors.append(f"Destination airport '{destination}' not found.")

    if errors:
        return {"error": errors}

    heading = calculate_heading(airport1.latitude_deg, airport1.longitude_deg,
                                airport2.latitude_deg, airport2.longitude_deg)

    try:
        altitude = int(altitude)
        altitude_msg = validate_altitude(altitude, heading)
    except ValueError:
        errors.append("Invalid altitude format.")

    if errors:
        return {"error": errors}
    
    return {
        "departure": f"{airport1.Aname} ({airport1.ident})",
        "destination": f"{airport2.Aname} ({airport2.ident})",
        "heading": heading,
        "altitude_check": altitude_msg
    }
