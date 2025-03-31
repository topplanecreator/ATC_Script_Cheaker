import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import math
import csv
import webbrowser
import pytest  # Import pytest

# --- Constants and Data Loading ---

# File paths for CSV data
CSV_FILENAME = "airlines.csv"  # Contains airline codes and names
AIRPORTS_CSV = "airports.csv" # Contains airport information
ROUTES_CSV = "routes.csv"     # Contains flight route information

def load_airline_codes(csv_filename):
    """Loads airline codes and names from a CSV file."""
    airline_codes = {}
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    code, name = row
                    airline_codes[code.strip()] = name.strip()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_filename}")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return {}
    return airline_codes

AIRLINE_CODES = load_airline_codes(CSV_FILENAME)

def load_airports(csv_path):
    """Loads airport data from a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_path}")
        return pd.DataFrame()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return pd.DataFrame()

def create_route_list(csv_file):
    """Creates displayable route names and flight plan route strings from a CSV file."""
    display_routes = []
    flight_plan_routes = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) >= 3:
                    route_name = row[1]
                    fix_name = row[2]
                    display_routes.append(f"{route_name.replace('6',' SIX').replace('7',' SEVEN').replace('5',' FIVE').replace('4',' FOUR')} ({fix_name})")
                    flight_plan_routes.append(f"{route_name.replace('6',' SIX').replace('7',' SEVEN').replace('5',' FIVE').replace('4',' FOUR')} departure, {fix_name} transition")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_file}")
        return [], []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return [], []
    return display_routes, flight_plan_routes

route_display_list, flight_plan_routes = create_route_list(ROUTES_CSV)

# --- Airport Information and Calculation Functions ---

def get_airport_info(df, code):
    """Retrieves airport information from a DataFrame based on the airport code."""
    airport = df[df['ident'] == code.upper()]
    if airport.empty:
        return None
    return airport.iloc[0]

def calculate_direction(lat1, lon1, lat2, lon2):
    """Calculates the bearing (direction) between two points given their latitudes and longitudes."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    
    if bearing < 0:
        bearing += 360
    return round(bearing, 2)

def name_heading(code1, code2, airports_df):
    """Calculates the heading and retrieves airport names and codes."""
    airport1 = get_airport_info(airports_df, code1)
    airport2 = get_airport_info(airports_df, code2)
    
    if airport1 is None or airport2 is None:
        messagebox.showerror("Error", "One or both airport codes not found.")
        return None, None, None
    
    heading = calculate_direction(airport1.latitude_deg, airport1.longitude_deg, 
                                  airport2.latitude_deg, airport2.longitude_deg)
    
    rheading = round(heading)
    
    airport_info1 = f"{airport1.Aname} ({airport1.ident})"
    airport_info2 = f"{airport2.Aname} ({airport2.ident})"
    
    return rheading, airport_info1, airport_info2

def altitude_cal(altitude, rheading):
    """Calculates the final altitude based on the given altitude and heading."""
    cal_altitude = altitude / 10

    if 0 <= rheading < 180:
        heading_direction = "NE"
    else:
        heading_direction = "SW"

    if heading_direction == "NE":
        if cal_altitude % 2 == 0:
            final_altitude = round((cal_altitude + 1) * 10)
        else:
            final_altitude = round(cal_altitude * 10)
    else:
        if cal_altitude % 2 != 0:
            final_altitude = round((cal_altitude + 1) * 10)
        else:
            final_altitude = round(cal_altitude * 10)

    return final_altitude

# --- Utility Functions ---

def update_callsign_label(callsign_entry, callsign_label):
    """Updates the callsign label with the airline name based on the entered callsign."""
    callsign = callsign_entry.get().upper()
    if len(callsign) >= 3 and callsign[:3] in AIRLINE_CODES:
        airline_name = AIRLINE_CODES[callsign[:3]]
        callsign_label.config(text=f"{airline_name} {callsign[3:]}")
    else:
        callsign_label.config(text="")

# --- Flight Plan Generation ---

def generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var):
    """Generates and displays a flight plan based on user inputs."""
    frequency = frequency_entry.get() or '125.8'
    callsign = callsign_entry.get().upper()
    airline_code = callsign[:3]
    flight_number = callsign[3:]

    if airline_code in AIRLINE_CODES:
        callsign = f"{AIRLINE_CODES[airline_code]} {flight_number}"

    code1 = departure_entry.get().upper() or "KMEM"
    code2 = destination_entry.get().upper()

    route_name = route_var.get()
    if route_name in ["GENEH SEVEN (NUYID)", "GMBUD SEVEN (JADET)", "OLEMS SIX (LEYIK)", "BINKY SIX (BASBE)", "AUTMN SIX (LUVEC)", "NIKEI FIVE (INAYO)", "HOTRD FIVE (TOMKE)", "GRRIZ FIVE (MIEDZ)", "ELVIS FOUR (NFIVE)", "ELVIS FOUR (EFOUR)", "ELVIS FOUR (STREE)", "ELVIS FOUR (SFOUR)", "ELVIS FOUR (WFIVE)"]:
        route_night_label.config(text=f"Note: {route_name} is a 0200-0600 only SID.")
    else:
        route_night_label.config(text="")

    route_index = route_display_list.index(route_name)
    route = flight_plan_routes[route_index]

    airports_df = load_airports(AIRPORTS_CSV)
    rheading, airport_info1, airport_info2 = name_heading(code1, code2, airports_df)
    if rheading is None:
        return

    flight_direction = "NE" if 0 <= rheading < 180 else "SW"
    direction_label.config(text=f"Direction: {flight_direction}")
    heading_var.set(f"Heading: {rheading}°")

    altitude = int(altitude_entry.get())
    final_altitude = altitude_cal(altitude, rheading)
    sub1 = "" if final_altitude >= 200 else "00"
    sub2 = "FL " if final_altitude >= 200 else ""

    flight_plan_label.config(text=f'{callsign}, cleared to {airport_info2}, via {route}, \n'
                            f'then as filed, maintain 5000, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
                            f'departure frequency {frequency}, squawk {squawk_entry.get()}')
    
    print(f'{callsign}, cleared to {airport_info2}, via {route}, \n'
            f'then as filed, maintain 5000, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
            f'departure frequency {frequency}, squawk {squawk_entry.get()} \n\n'
            f'****************************************************\n\n')

# --- GUI Setup ---

root = tk.Tk()
root.title("Flight Plan Generator")
root.geometry("650x700")
root.resizable(True, True)

top_frame = ttk.Frame(root)
top_frame.pack(fill=tk.X)

notebook = ttk.Notebook(top_frame, height=450)
notebook.pack(fill=tk.X, expand=False)

frame1 = ttk.Frame(notebook, padding=10)
frame2 = ttk.Frame(notebook)

notebook.add(frame1, text="IFR")
notebook.add(frame2, text="VFR")

frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=2)

# --- IFR Frame (frame1) ---

# Input Fields
Frequency = tk.StringVar(value="125.8")
ttk.Label(frame1, text="Frequency:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
frequency_entry = ttk.Entry(frame1, textvariable=Frequency)
frequency_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

Callsign = tk.StringVar(value="AAL123")
ttk.Label(frame1, text="Callsign:").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
callsign_entry = ttk.Entry(frame1, textvariable=Callsign)
callsign_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
callsign_label = ttk.Label(frame1, text="")
callsign_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
callsign_entry.bind("<KeyRelease>", lambda event: update_callsign_label(callsign_entry, callsign_label))

Aircraft_Type = tk.StringVar(value="Jet")
ttk.Label(frame1, text="Aircraft Type:").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
aircraft_dropdown = ttk.Combobox(frame1, textvariable=Aircraft_Type, values=["Jet", "Prop"], state="readonly")
aircraft_dropdown.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
aircraft_dropdown.current(0)

Departure = tk.StringVar(value="KMEM")
ttk.Label(frame1, text="Departure ICAO:").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
departure_entry = ttk.Entry(frame1, textvariable=Departure)
departure_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

Destination = tk.StringVar(value="KLAX")
ttk.Label(frame1, text="Destination ICAO:").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
destination_entry = ttk.Entry(frame1, textvariable=Destination)
destination_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

Route_Display = tk.StringVar(value=route_display_list[0])
ttk.Label(frame1, text="Route:").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
route_var = ttk.Combobox(frame1, textvariable=Route_Display, values=route_display_list, state="readonly")
route_var.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
route_var.current(0)

Altitude = tk.StringVar(value="350")
ttk.Label(frame1, text="Altitude:").grid(row=6, column=0, sticky="ew", padx=5, pady=5)
altitude_entry = ttk.Entry(frame1, textvariable=Altitude)
altitude_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

Squawk = tk.StringVar(value="2200")
ttk.Label(frame1, text="Squawk:").grid(row=7, column=0, sticky="ew", padx=5, pady=5)
squawk_entry = ttk.Entry(frame1, textvariable=Squawk)
squawk_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

flight_plan_label = tk.Label(frame1, text="Flight Plan:", justify=tk.LEFT)
flight_plan_label.grid(row=9, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

direction_label = tk.Label(frame1, text="Direction:")
direction_label.grid(row=10, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

route_night_label = tk.Label(frame1, text="")
route_night_label.grid(row=11, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

heading_var = tk.StringVar(value="0.00°")
ttk.Label(frame1, textvariable=heading_var).grid(row=12, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

ttk.Button(frame1, text="Update Flight Plan", command=lambda: generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var)).grid(row=8, column=0, columnspan=2, pady=10)

# --- VFR Frame (frame2) ---

def GoToLink():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

ttk.Label(frame2, text="VFR Flight Plan Coming Soon!").grid(row=0, column=0, columnspan=2, pady=20)

my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white")
my_button.grid(row=1, column=0, columnspan=2, pady=10)

# --- Notes Section (Expands) ---

notes_frame = ttk.Frame(root, padding=5)
notes_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(notes_frame, text="Notes:").pack(anchor="w", padx=5, pady=0)

notes_text_box = tk.Text(notes_frame, height=6, wrap="word")
scrollbar = tk.Scrollbar(notes_frame, command=notes_text_box.yview)

notes_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=0)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

notes_text_box.config(yscrollcommand=scrollbar.set)

# --- Pytest Functions ---

def test_load_airline_codes():
    """Tests the load_airline_codes function."""
    codes = load_airline_codes("airlines.csv")
    assert isinstance(codes, dict)
    if codes:
        assert len(codes) > 0

def test_load_airports():
    """Tests the load_airports function."""
    df = load_airports("airports.csv")
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'ident' in df.columns
        assert 'latitude_deg' in df.columns
        assert 'longitude_deg' in df.columns

def test_create_route_list():
    """Tests the create_route_list function."""
    display, plan = create_route_list("routes.csv")
    assert isinstance(display, list)
    assert isinstance(plan, list)
    if display:
        assert len(display) > 0

def test_get_airport_info():
    """Tests the get_airport_info function."""
    airports_df = load_airports("airports.csv")
    if not airports_df.empty:
        airport = get_airport_info(airports_df, "KMEM")
        if airport is not None:
            assert 'ident' in airport.index

def test_calculate_direction():
    """Tests the calculate_direction function."""
    direction = calculate_direction(35.0, -90.0, 40.0, -80.0)
    assert isinstance(direction, float)
    assert 0 <= direction <= 360

def test_name_heading():
    """Tests the name_heading function."""
    airports_df = load_airports("airports.csv")
    if not airports_df.empty:
        heading, info1, info2 = name_heading("KMEM", "KLAX", airports_df)
        if heading is not None:
            assert isinstance(heading, int)
            assert isinstance(info1, str)
            assert isinstance(info2, str)

def test_altitude_cal():
    """Tests the altitude_cal function."""
    altitude = altitude_cal(350, 90)
    assert isinstance(altitude, int)
    assert altitude > 0

# --- Run the application ---
if __name__ == "__main__":
    root.mainloop()