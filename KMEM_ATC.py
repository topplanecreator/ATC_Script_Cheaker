import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import math
import csv
import webbrowser
import json

CSV_FILENAME = "airlines.csv"
AIRPORTS_CSV = "airports.csv"
ROUTES_CSV = "routes.csv"
NOTES_FILENAME = "user_notes.json"

def load_airline_codes(csv_filename):
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
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    return airline_codes

AIRLINE_CODES = load_airline_codes(CSV_FILENAME)

def load_airports(csv_path):
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_path}")
        return pd.DataFrame()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return pd.DataFrame()

def create_route_list(csv_file):
    display_routes = []
    flight_plan_routes = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 3:
                    route_name = row[1]
                    fix_name = row[2]
                    display_routes.append(f"{route_name.replace('6', ' SIX').replace('7', ' SEVEN').replace('5', ' FIVE').replace('4', ' FOUR')} ({fix_name})")
                    flight_plan_routes.append(f"{route_name.replace('6', ' SIX').replace('7', ' SEVEN').replace('5', ' FIVE').replace('4', ' FOUR')} departure, {fix_name} transition")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    return display_routes, flight_plan_routes

route_display_list, flight_plan_routes = create_route_list(ROUTES_CSV)

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

def name_heading(code1, code2, airports_df):
    airport1 = get_airport_info(airports_df, code1)
    airport2 = get_airport_info(airports_df, code2)
    if airport1 is None or airport2 is None:
        messagebox.showerror("Error", "One or both airport codes not found.")
        return None, None, None
    heading = calculate_direction(airport1.latitude_deg, airport1.longitude_deg,
                                  airport2.latitude_deg, airport2.longitude_deg)
    rheading = round(heading)
    airport_info1 = f"{airport1.name} ({airport1.ident})"
    airport_info2 = f"{airport2.name} ({airport2.ident})"
    return rheading, airport_info1, airport_info2

def altitude_cal(altitude, rheading):
    cal_altitude = altitude / 10
    heading_direction = "NE" if 0 <= rheading < 180 else "SW"
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

def update_callsign_label(callsign_entry, callsign_label):
    callsign = callsign_entry.get().upper()
    airline_code = callsign[:3]
    if airline_code in AIRLINE_CODES:
        callsign_label.config(text=f"({AIRLINE_CODES[airline_code]})")
    else:
        callsign_label.config(text="")

def generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var, aircraft_type_var, notes_text_box, system_notes_text_box):
    frequency = frequency_entry.get() or '125.8'
    callsign = callsign_entry.get().upper()
    airline_code = callsign[:3]
    flight_number = callsign[3:]
    if airline_code in AIRLINE_CODES:
        callsign = f"{AIRLINE_CODES[airline_code]} {flight_number}"
    code1 = departure_entry.get().upper() or "KMEM"
    code2 = destination_entry.get().upper()
    route_name = route_var.get()
    night_flag = ""
    if route_name in ["GENEH SEVEN (NUYID)", "GMBUD SEVEN (JADET)", "OLEMS SIX (LEYIK)", "BINKY SIX (BASBE)", "AUTMN SIX (LUVEC)", "NIKEI FIVE (INAYO)", "HOTRD FIVE (TOMKE)", "GRRIZ FIVE (MIEDZ)", "ELVIS FOUR (NFIVE)", "ELVIS FOUR (EFOUR)", "ELVIS FOUR (STREE)", "ELVIS FOUR (SFOUR)", "ELVIS FOUR (WFIVE)"]:
        night_flag = " (Night SID)"
        route_night_label.config(text="Night SID")
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
    aircraft_type = aircraft_type_var.get()
    initial_altitude = 3000 if aircraft_type == "Prop" else 5000
    flight_plan_label.config(text=f'{callsign}, cleared to {airport_info2}, via {route}{night_flag}, \n'
                                  f'then as filed, maintain {initial_altitude}, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
                                  f'departure frequency {frequency}, squawk {squawk_entry.get()}')
    notes = []
    if altitude != final_altitude:
        notes.append(f"Altitude Note: Input altitude {altitude} does not match calculated final altitude {final_altitude}.")
    if aircraft_type == "Prop" and code1.upper() != "KMEM" and "ELVIS FOUR" not in route_name:
        notes.append("Prop Note: Prop planes can only depart from KMEM (Elvis).")
    if night_flag:
        notes.append(f"Night Note: {route_name} is a 0200-0600 only SID.")
    notes.append(f"Direction: {flight_direction}")
    system_notes_text_box.delete(1.0, tk.END)
    if notes:
        system_notes_text_box.config(fg="red")
        system_notes_text_box.insert(tk.END, "\n".join(notes))
    else:
        system_notes_text_box.config(fg="white")

def change_text_color(color):
    notes_text_box.tag_configure(color, foreground=color)
    try:
        sel_start = "sel.first"
        sel_end = "sel.last"
        for tag in notes_text_box.tag_names():
            if tag != "sel":
                notes_text_box.tag_remove(tag, sel_start, sel_end)
        notes_text_box.tag_add(color, sel_start, sel_end)
    except tk.TclError:
        pass

def save_notes(notes, colors):
    """Saves notes and character colors."""
    try:
        with open(NOTES_FILENAME, 'w') as file:
            json.dump({"notes": notes, "colors": colors}, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save notes: {e}")

def load_notes():
    """Loads notes and character colors."""
    try:
        with open(NOTES_FILENAME, 'r') as file:
            data = json.load(file)
            return data["notes"], data["colors"]
    except FileNotFoundError:
        return "", []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load notes: {e}")
        return "", []

root = tk.Tk()
root.title("Flight Plan Generator")
root.geometry("900x1000")
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

route_night_label = tk.Label(frame1, text="")
route_night_label.grid(row=11, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

heading_var = tk.StringVar(value="0.00°")
ttk.Label(frame1, textvariable=heading_var).grid(row=12, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

direction_label = tk.Label(frame1, text="")
direction_label.grid(row=13, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

ttk.Button(frame1, text="Update Flight Plan", command=lambda: generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var, Aircraft_Type, notes_text_box, system_notes_text_box)).grid(row=8, column=0, columnspan=2, pady=10)

def GoToLink():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

ttk.Label(frame2, text="\
    - VFR clearances are are carbon copy of one another! (callsign), \n\
        Cleared into the Memphis Class Bravo Airspace, Maintain VFR at or below 2500. \n\
        Departure frequency XXX.XX, squawk XXXX\n\n\
    - We have to fill out the flight plan editor for VFR aircraft! The most important part \n\
        is the aircraft type, direction of flight, and the VFR altitude! It goes in as VFR/XXX\n\n\
    - These clearances differ at different airspaces! Charlies don't require the clearance portion.\n\n\
    - VFR clearances are very simple to give and therefore can be prioritized in the queue \n\
        instead of IFR clearances which require a full route check.").grid(row=3, column=0, columnspan=2, pady=20)
my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white")
my_button.grid(row=1, column=0, columnspan=2, pady=10)

system_notes_frame = ttk.Frame(root, padding=5)
system_notes_frame.pack(fill=tk.X)
tk.Label(system_notes_frame, text="System Notes:").pack()
system_notes_text_box = tk.Text(system_notes_frame, height=4, wrap="word")
system_notes_text_box.pack(fill=tk.X)

notes_frame = ttk.Frame(root, padding=5)
notes_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(notes_frame, text="Your Notes:").grid(row=0, column=0, sticky="w", padx=5, pady=0)
notes_text_box = tk.Text(notes_frame, height=10, wrap="word")
notes_text_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=0)

color_frame = ttk.Frame(notes_frame)
color_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

colors = ["black", "white", "red", "blue", "green", "yellow", "purple", "orange", "gray"]
for i, color in enumerate(colors):
    button = ttk.Button(color_frame, text=color.capitalize(), command=lambda c=color: change_text_color(c))
    button.grid(row=0, column=i, padx=2)

notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)

tag_colors_dict = {}

def on_closing():
    """Saves the notes and colors when the window closes."""
    notes = notes_text_box.get(1.0, tk.END)
    colors = []
    for i in range(len(notes)):
        tags = notes_text_box.tag_names(f"1.0+{i}c")
        color = "black"  # Default color
        for tag in tags:
            if tag != "sel":
                color = notes_text_box.tag_cget(tag, "foreground")
                break
        colors.append(color)
    save_notes(notes, colors)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

loaded_notes, loaded_colors = load_notes()
notes_text_box.insert(tk.END, loaded_notes)

if loaded_colors:
    for i, color in enumerate(loaded_colors):
        notes_text_box.tag_add(color, f"1.0+{i}c")
        notes_text_box.tag_configure(color, foreground=color)


if __name__ == "__main__":
    root.mainloop()