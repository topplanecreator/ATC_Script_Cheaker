"""
auther: michel gledhill
name: gui.py

"""

import tkinter as tk
from tkinter import ttk
import webbrowser
import csv
import pandas as pd
import math

# Load airports from CSV and create ICAO-to-Name dictionary
def load_airports():
    airport_dict = {}
    try:
        with open("airports.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                icao = row["icao_code"].strip().upper()
                name = row["Aname"].strip()
                if icao:  # Ensure ICAO code exists
                    airport_dict[icao] = name
    except FileNotFoundError:
        print("Error: airports.csv not found.")
    return airport_dict

airport_dict = load_airports()

# Load routes and fixes from CSV
def load_routes():
    try:
        with open("routes.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            route_dict = {}
            fix_dict = {}  # Store fixes separately
            for row in reader:
                route, fix = row[1], row[2]
                route_display = f"{route} ({fix})"
                route_dict[route_display] = route  # Store route name
                fix_dict[route_display] = fix  # Store fix name
            return route_dict, fix_dict
    except FileNotFoundError:
        return {"AUTMN6 (LUVEC)": "AUTMN6"}, {"AUTMN6 (LUVEC)": "LUVEC"}  # Default if CSV is missing

routes_dict, fixes_dict = load_routes()
route_display_list = list(routes_dict.keys())  # What the user sees

# Function to format altitude correctly
def format_altitude(alt):
    alt = alt.upper().replace("FL", "")  # Remove "FL" if user enters it
    if not alt.isdigit() or len(alt) not in [2, 3]:  # Validate input
        return "35 thousand"  # Default to 35,000 ft if invalid input

    alt = int(alt)  # Convert to integer

    if alt >= 200:  # Use FL if 200 or above
        return f"FL{alt}"
    else:  # Use "thousand" format if below FL200
        return f"{alt} thousand"

# Convert ICAO code to airport name
def get_airport_name(icao_code):
    return airport_dict.get(icao_code.upper(), icao_code)  # Return name if found, else return the ICAO code

def calculate_heading(departure: str, destination: str, csv_path: str = "airports.csv") -> float:
    # Load airport data
    airports = pd.read_csv(csv_path)
    
    # Find departure and destination coordinates
    dep_row = airports[airports['icao_code'] == departure].iloc[0]
    dest_row = airports[airports['icao_code'] == destination].iloc[0]
    
    lat1, lon1 = math.radians(dep_row['latitude_deg']), math.radians(dep_row['longitude_deg'])
    lat2, lon2 = math.radians(dest_row['latitude_deg']), math.radians(dest_row['longitude_deg'])

    # Compute initial heading
    delta_lon = lon2 - lon1
    x = math.cos(lat2) * math.sin(delta_lon)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    
    heading = math.degrees(math.atan2(x, y))
    heading = (heading + 360) % 360  # Normalize to 0-360 degrees
    
    return heading



# Update function
def update_Flight_Plan():
    selected_display = Route_Display.get()
    selected_route = routes_dict.get(selected_display, "Unknown")
    selected_fix = fixes_dict.get(selected_display, "Unknown")
    formatted_altitude = format_altitude(Altitude.get())

    departure_name = get_airport_name(Departure.get())
    destination_name = get_airport_name(Destination.get())

    if Aircraft_Type.get() == "Jet":
        I_Alt = "5000"
    elif Aircraft_Type.get() == "Prop":
        I_Alt = "3000"
    else:
        I_Alt = "5000"

    heading = calculate_heading(Departure.get(), Destination.get())  # Calculate heading
    heading_var.set(f"{heading:.2f}°")  # Update the GUI variable

    flight_plan_text = (f'{Callsign.get()} cleared to {destination_name}, via {selected_route} departure {selected_fix} transition, \n'
                        f'then as filed, maintain {I_Alt}, expect {formatted_altitude} 1-0 minutes after departure, \n'
                        f'departure frequency {Frequency.get()}, squawk {Squawk.get()}')
    Flight_Plan.set(flight_plan_text)


# Initialize root window
root = tk.Tk()
root.title("Flight Plan Generator")
root.geometry("650x700")
root.resizable(True, True)

# Create a frame to hold the notebook with a fixed height
top_frame = ttk.Frame(root)
top_frame.pack(fill=tk.X)

# Create notebook (tabs)
notebook = ttk.Notebook(top_frame, height=450)
notebook.pack(fill=tk.X, expand=False)

# Create frames for tabs
frame1 = ttk.Frame(notebook, padding=10)
frame2 = ttk.Frame(notebook)

notebook.add(frame1, text="IFR")
notebook.add(frame2, text="VFR")

frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=2)

# ************************** Frame1 (IFR) ************************** #

# Input Fields
Frequency = tk.StringVar(value="125.8")
ttk.Label(frame1, text="Frequency:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Frequency).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

Callsign = tk.StringVar(value="AAL123")
ttk.Label(frame1, text="Callsign:").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Callsign).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Aircraft Type Selection
Aircraft_Type = tk.StringVar(value="Jet")  # Default to Jet

ttk.Label(frame1, text="Aircraft Type:").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
aircraft_dropdown = ttk.Combobox(frame1, textvariable=Aircraft_Type, values=["Jet", "Prop"], state="readonly")
aircraft_dropdown.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
aircraft_dropdown.current(0)  # Select Jet by default

Departure = tk.StringVar(value="KMEM")
ttk.Label(frame1, text="Departure ICAO:").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Departure).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

Destination = tk.StringVar(value="KLAX")
ttk.Label(frame1, text="Destination ICAO:").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Destination).grid(row=4, column=1, sticky="ew", padx=5, pady=5)

# Route Dropdown (Displays "ROUTE (FIX)", but stores just the route)
Route_Display = tk.StringVar(value=route_display_list[0])
ttk.Label(frame1, text="Route:").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
route_dropdown = ttk.Combobox(frame1, textvariable=Route_Display, values=route_display_list, state="readonly")
route_dropdown.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
route_dropdown.current(0)  # Select first route by default

Altitude = tk.StringVar(value="350")  # Default to Flight Level 350
ttk.Label(frame1, text="Altitude:").grid(row=6, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Altitude).grid(row=6, column=1, sticky="ew", padx=5, pady=5)

Squawk = tk.StringVar(value="2200")
ttk.Label(frame1, text="Squawk:").grid(row=7, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Squawk).grid(row=7, column=1, sticky="ew", padx=5, pady=5)

# Add Update Button
ttk.Button(frame1, text="Update Flight Plan", command=update_Flight_Plan).grid(row=8, column=0, columnspan=2, pady=10)

# Flight Plan Display Below Button
Flight_Plan = tk.StringVar(value="Flight Plan:")
ttk.Label(frame1, textvariable=Flight_Plan, relief="solid", padding=0).grid(row=9, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

heading_var = tk.StringVar(value="0.00°")  # Default value
ttk.Label(frame1, textvariable=heading_var).grid(row=10, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
# ************************** Frame2 (VFR) ************************** #

def GoToLink():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

ttk.Label(frame2, text="VFR Flight Plan Coming Soon!").grid(row=0, column=0, columnspan=2, pady=20)

my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white")
my_button.grid(row=1, column=0, columnspan=2, pady=10)


# ************************** Notes Section (Expands) ************************** #

notes_frame = ttk.Frame(root, padding=5)
notes_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(notes_frame, text="Notes:").pack(anchor="w", padx=5, pady=0)

notes_text_box = tk.Text(notes_frame, height=6, wrap="word")
scrollbar = tk.Scrollbar(notes_frame, command=notes_text_box.yview)

notes_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=0)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

notes_text_box.config(yscrollcommand=scrollbar.set)


# Run the application
root.mainloop()
