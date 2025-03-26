import tkinter as tk
from tkinter import messagebox
import pandas as pd
import math
import os
import sys
import pandas as pd
import csv


CSV_FILENAME = "airlines.csv"
def load_airline_codes(csv_filename):
    airline_codes = {}
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:  # Ensure there are exactly two columns
                code, name = row
                airline_codes[code.strip()] = name.strip()
    return airline_codes

AIRLINE_CODES = load_airline_codes(CSV_FILENAME)

def load_airports(csv_path):
    return pd.read_csv(csv_path)

def get_airport_info(df, code):
    airport = df[df['ident'] == code.upper()]
    if airport.empty:
        return None
    return airport.iloc[0]

def calculate_direction(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    
    if bearing < 0:
        bearing += 360
    return round(bearing, 2)

def name_heading(code1, code2):

    # Get the correct path (works for bundled .exe or normal script)
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_path, "airports.csv")

    # Load CSV
    df = pd.read_csv(csv_path)
    
    airports_df = load_airports(csv_path)
    
    airport1 = get_airport_info(airports_df, code1)
    airport2 = get_airport_info(airports_df, code2)
    
    if airport1 is None or airport2 is None:
        print("One or both airport codes not found. Please try again.")
        return None, None, None
    
    heading = calculate_direction(airport1.latitude_deg, airport1.longitude_deg, 
                                  airport2.latitude_deg, airport2.longitude_deg)
    
    rheading = round(heading)
    
    airport_info1 = f"{airport1.Aname} ({airport1.ident})"
    airport_info2 = f"{airport2.Aname} ({airport2.ident})"
    
    return rheading, airport_info1, airport_info2

def altitude_cal(altitude, rheading, fr):
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

    if fr == "VFR":
        final_altitude += 5

    if final_altitude > 195 and fr == "VFR":
        if heading_direction == "NE":
            final_altitude = 195
        else:
            final_altitude = 185

    return final_altitude


def to_uppercase(event):
    current_text = event.widget.get()
    event.widget.delete(0, tk.END)
    event.widget.insert(0, current_text.upper())



def update_callsign_label(event):
    callsign = callsign_entry.get().upper()
    if len(callsign) >= 3 and callsign[:3] in AIRLINE_CODES:
        airline_name = AIRLINE_CODES[callsign[:3]]
        callsign_label.config(text=f"{airline_name} {callsign[3:]}")
    else:
        callsign_label.config(text="")


def get_valid_input(prompt, valid_values=None, input_type=str):
    while True:
        user_input = input(prompt).strip()
        try:
            if input_type == int:
                user_input = int(user_input)
                if user_input <= 0:
                    print("Please enter a positive number.")
                    continue
            elif valid_values and user_input.upper() not in valid_values:
                print(f"Invalid input. Valid options are: {', '.join(valid_values)}.")
                continue
            return user_input
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")
    

def generate_flight_plan(event=None):
    global route_changed_flag  # Ensure we're modifying the global flag
    
    frequency = frequency_entry.get() or '125.8'
    callsign = callsign_entry.get().upper()
    
    airline_code = callsign[:3]
    flight_number = callsign[3:]

    if airline_code in AIRLINE_CODES:
        callsign = f"{AIRLINE_CODES[airline_code]} {flight_number}"
    
    code1 = departure_entry.get().upper() or "KMEM"
    code2 = destination_entry.get().upper()
    
    # Automatically set route to "ELVIS FOUR" if VFR
    route = route_var.get().upper()
    
    if fr_var.get().upper() == "VFR" and route_var.get() not in [
    "ELVIS FOUR (NRONE)",
    "ELVIS FOUR (NTWOO)",
    "ELVIS FOUR (NTREE)",
    "ELVIS FOUR (NFOUR)",
    "ELVIS FOUR (NFIVE)",
    "ELVIS FOUR (EONE)",
    "ELVIS FOUR (ETWOO)",
    "ELVIS FOUR (ETREE)",
    "ELVIS FOUR (EFOUR)",
    "ELVIS FOUR (SONE)",
    "ELVIS FOUR (STWOO)",
    "ELVIS FOUR (STREE)",
    "ELVIS FOUR (SFOUR",
    "ELVIS FOUR (WONE)",
    "ELVIS FOUR (WTWOO)",
    "ELVIS FOUR (WTREE)",
    "ELVIS FOUR (WFOUR)",
    "ELVIS FOUR (WFIVE)",]:
        route = "ELVIS FOUR"
        route_changed_flag = True
        route_change_label.config(text="Note: The route must be changed.")
    else:
        route_changed_flag = False
        route_change_label.config(text="")  # Clear the message if route is the default
  
    if route_var.get() in ["GENEH SEVEN (NUYID)", "GMBUD SEVEN (JADET)", "OLEMS SIX (LEYIK)", "BINKY SIX (BASBE)", "AUTMN SIX (LUVEC))", "NIKEI FIVE (INAYO)", "HOTRD FIVE (TOMKE)", "GRRIZ FIVE (MIEDZ)", "ELVIS FOUR (NFIVE)", "ELVIS FOUR (EFOUR)", "ELVIS FOUR (STREE)", "ELVIS FOUR (SFOUR)", "ELVIS FOUR (WFOUR)", "ELVIS FOUR (WFIVE)", ] and fr_var.get().upper() == "IFR":
        route_night_flag = True
        route_night_label.config(text=f"Note: {route_var.get()} is a 0200-0600 only SID.")
    else:
        route_night_flag = False
        route_night_label.config(text="")
    
    altitude = int(altitude_entry.get())
    fr = fr_var.get().upper()
    squawk = squawk_entry.get().upper()

    rheading, airport_info1, airport_info2 = name_heading(code1, code2)
    if rheading is None:
        messagebox.showerror("Error", "One or both airport codes not found.")
        return

    sub1 = ""
    sub2 = ""
    Cleared=""
    
    final_altitude = altitude_cal(altitude, rheading, fr)
    if final_altitude < 200:
        sub1 = "00"
    else:
        sub2 = "FL "
    if fr == "VFR":
        Cleared = "cleared out of the class bravo,"
    else:
        Cleared = ""
        
    
    # Determine flight direction
    flight_direction = "NE" if 0 <= rheading < 180 else "SW"
    direction_label.config(text=f"Direction: {flight_direction}")

    final_altitude = altitude_cal(altitude, rheading, fr)
    sub1 = "" if final_altitude >= 200 else "00"
    sub2 = "FL " if final_altitude >= 200 else ""
    Cleared = "cleared out of the class bravo," if fr == "VFR" else ""
    
    output_label.config(text=f'{callsign}, {Cleared} cleared to {airport_info2}, via {route}, \n'
                            f'then as filed, maintain 5000, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
                            f'departure frequency {frequency}, squawk {squawk}')


# Prevent running generate_flight_plan when pressing Enter in the NOTAMs text box
def on_enter(event):
    # Check if the focus is on the NOTAMs text box
    if event.widget != notam_text_box:
        generate_flight_plan(event)

# Tkinter Window Setup (same as before)
root = tk.Tk()
root.title("Flight Plan Generator")
default_font = ("Arial", 12)
root.option_add("*Font", default_font)
# Allow the window to be resizable in both directions
root.resizable(True, True)  # (width, height) resizable

# Configure the columns and rows to expand
root.grid_columnconfigure(0, weight=1, uniform="equal")  # Column 0 should expand
root.grid_columnconfigure(1, weight=2, uniform="equal")  # Column 1 should expand more
root.grid_columnconfigure(2, weight=0)  # Column 2 does not need to expand

# Configure rows to make NOTAMs row expand vertically
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)
root.grid_rowconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=0)
root.grid_rowconfigure(7, weight=0)
root.grid_rowconfigure(8, weight=0)
root.grid_rowconfigure(9, weight=0)
root.grid_rowconfigure(10, weight=0)
root.grid_rowconfigure(11, weight=1)  # Make row 11 (NOTAMs) expand vertically

# Labels and Input Fields (same as before)
tk.Label(root, text="Frequency:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
frequency_entry = tk.Entry(root)
frequency_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
frequency_entry.insert(0, '125.8')
frequency_entry.bind("<KeyRelease>", to_uppercase)

tk.Label(root, text="Callsign:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
callsign_entry = tk.Entry(root)
callsign_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
callsign_entry.bind("<KeyRelease>", update_callsign_label)
callsign_label = tk.Label(root, text="", fg="gray")
callsign_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

tk.Label(root, text="Departure:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
departure_entry = tk.Entry(root)
departure_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
departure_entry.insert(0, 'KMEM')
departure_entry.bind("<KeyRelease>", to_uppercase)

tk.Label(root, text="Destination:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
destination_entry = tk.Entry(root)
destination_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
destination_entry.bind("<KeyRelease>", to_uppercase)

tk.Label(root, text="Route:").grid(row=4, column=0, sticky="w", padx=10, pady=5) ### this needs to be changed to a csv if posible
routes = [
    "AUTMN SIX (LUVEC)",
    "AZONE SEVEN (PITEW)", 
    "BBKNG SEVEN (KERMI)", 
    "BINKY SIX (BASBE)", 
    "CHLDR FIVE (ANSWA)", 
    "CRSON SEVEN (HUMMS)", 
    "DUCKZ FIVE (HELAR)", 
    "ELVIS FOUR (NRONE)",
    "ELVIS FOUR (NTWOO)",
    "ELVIS FOUR (NTREE)",
    "ELVIS FOUR (NFOUR)",
    "ELVIS FOUR (NFIVE)",
    "ELVIS FOUR (EONE)",
    "ELVIS FOUR (ETWOO)",
    "ELVIS FOUR (ETREE)",
    "ELVIS FOUR (EFOUR)",
    "ELVIS FOUR (SONE)",
    "ELVIS FOUR (STWOO)",
    "ELVIS FOUR (STREE)",
    "ELVIS FOUR (SFOUR)",
    "ELVIS FOUR (WONE)",
    "ELVIS FOUR (WTWOO)",
    "ELVIS FOUR (WTREE)",
    "ELVIS FOUR (WFOUR)",
    "ELVIS FOUR (WFIVE)",  
    "GENEH SEVEN (NUYID)", 
    "GMBUD SEVEN (JADET)", 
    "GOETZ SEVEN (DIYAB)", 
    "GRRIZ FIVE (MIEDZ)", 
    "HOTRD FIVE (TOMKE)", 
    "JTEEE FIVE (ODATE)", 
    "NIKEI FIVE (INAYO)", 
    "OLEMS SIX (LEYIK)",
    "PIEPE SIX (IBUFY)", 
    "SELPH SEVEN (OHULO)", 
    "ZUMIT FIVE (FOXOM)"
]
route_var = tk.StringVar()
route_var.set(routes[0])  # Set default route
route_menu = tk.OptionMenu(root, route_var, *routes)
route_menu.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

tk.Label(root, text="Altitude:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
altitude_entry = tk.Entry(root)
altitude_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
altitude_entry.bind("<KeyRelease>", to_uppercase)

tk.Label(root, text="VFR/IFR:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
fr_var = tk.StringVar(value="IFR")
fr_menu = tk.OptionMenu(root, fr_var, "IFR", "VFR")
fr_menu.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

tk.Label(root, text="Squawk:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
squawk_entry = tk.Entry(root)
squawk_entry.grid(row=7, column=1, sticky="ew", padx=10, pady=5)
squawk_entry.bind("<KeyRelease>", to_uppercase)

# Generate Button
generate_button = tk.Button(root, text="Generate Flight Plan", command=generate_flight_plan)
generate_button.grid(row=8, columnspan=2, padx=10, pady=5)

# Output
output_label = tk.Label(root, text="", justify=tk.LEFT)
output_label.grid(row=9, columnspan=2, padx=10, pady=5)

# Add a label to display the route change status just above the requirements section
route_change_label = tk.Label(root, text="", fg="red")
route_change_label.grid(row=10, columnspan=2, padx=10, pady=5)

route_night_label = tk.Label(root, text="", fg="red")
route_night_label.grid(row=10, columnspan=2, padx=10, pady=5)
                        
# Create a text box for entering NOTAMs
tk.Label(root, text="Note Box:").grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=5)

# Text widget for NOTAMs input
notam_text_box = tk.Text(root, height=6, width=50)
notam_text_box.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Adding a scrollbar for the NOTAMs text box
scrollbar = tk.Scrollbar(root, command=notam_text_box.yview)
scrollbar.grid(row=11, column=2, sticky='ns')
notam_text_box.config(yscrollcommand=scrollbar.set)

direction_label = tk.Label(root, text="Direction: N/A", fg="gray")
direction_label.grid(row=4, column=2, sticky="w", padx=10, pady=5)

# Binding Enter key to trigger flight plan generation only if focus is outside the NOTAM box
root.bind("<Return>", on_enter)

# Run the application
root.mainloop()
