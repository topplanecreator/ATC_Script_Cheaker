import tkinter as tk
from tkinter import messagebox, ttk
import csv

def load_routes_from_csv(file_path):
    routes = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                route_name = row[1]
                fix = row[2]
                time_flag = row[4]
                route_entry = f"{route_name} ({fix})"
                routes.append((route_entry, time_flag))
    except FileNotFoundError:
        messagebox.showerror("Error", "Route CSV file not found!")
    return routes

def check_time_flag(*args):
    selected_route = route_var.get()
    for route, time_flag in routes:
        if route == selected_route and time_flag == "T":
            warning_label.config(text=f"Warning: The {departure_entry.get()} departure is a 0200-0600 departure.", fg="red")
            break
    else:
        warning_label.config(text="")

def submit_flight_details():
    callsign = callsign_entry.get()
    airport_info2 = destination_entry.get()
    route = route_var.get()
    aircraft_type = aircraft_type_var.get()
    final_altitude = "3000" if aircraft_type == "Prop" else "5000"
    frequency = frequency_entry.get()
    squawk = squawk_entry.get()

    # Extract departure and fix from route string
    if "(" in route and ")" in route:
        departure, fix = route.split(" (")
        fix = fix.strip(")")
    else:
        departure, fix = route, "UNKNOWN"

    # Check if the aircraft type is Prop and enforce ELVIS4
    if aircraft_type == "Prop" and "ELVIS4" not in route:
        route += " (ELVIS4 required for Props)"

    clearance_text = (f"{callsign} Memphis Ground, cleared to {airport_info2}, via {departure} departure, {fix} transition, \n"
                      f"then as filed, maintain {final_altitude}, expect {final_altitude} 1-0 minutes after departure, \n"
                      f"departure frequency {frequency}, squawk {squawk}")
    
    output_label.config(text=clearance_text, fg="black")

def update_prop_warning(*args):
    aircraft_type = aircraft_type_var.get()
    if aircraft_type == "Prop":
        prop_warning_label.config(text="Note: Prop aircraft must use the ELVIS4 departure.", fg="red")
    else:
        prop_warning_label.config(text="")

root = tk.Tk()
root.title("Flight Input")
root.resizable(True, True)

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

frame1 = tk.Frame(notebook)
notebook.add(frame1, text="Flight Input")

labels = ["Frequency:", "Callsign:", "Departure:", "Destination:", "Route:", "Aircraft Type:", "Altitude:", "Squawk:"]
for i, label in enumerate(labels):
    tk.Label(frame1, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)

frequency_entry = tk.Entry(frame1)
callsign_entry = tk.Entry(frame1)
departure_entry = tk.Entry(frame1)
destination_entry = tk.Entry(frame1)
altitude_entry = tk.Entry(frame1)
squawk_entry = tk.Entry(frame1)

entries = [frequency_entry, callsign_entry, departure_entry, destination_entry, altitude_entry, squawk_entry]
for i, entry in enumerate(entries):
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    frame1.columnconfigure(1, weight=1)

routes = load_routes_from_csv("routes.csv")
route_var = tk.StringVar(value=routes[0][0] if routes else "No Routes Available")
route_dropdown = tk.OptionMenu(frame1, route_var, *[r[0] for r in routes])
route_dropdown.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
route_var.trace_add("write", check_time_flag)

aircraft_type_var = tk.StringVar(value="Jet")
aircraft_type_dropdown = tk.OptionMenu(frame1, aircraft_type_var, "Jet", "Prop")
aircraft_type_dropdown.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
aircraft_type_var.trace_add("write", update_prop_warning)

altitude_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
squawk_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

submit_button = tk.Button(frame1, text="Submit", command=submit_flight_details)
submit_button.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")

warning_label = tk.Label(frame1, text="", fg="red")
warning_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=5, pady=5)

prop_warning_label = tk.Label(frame1, text="", fg="red")
prop_warning_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=5, pady=5)

output_label = tk.Label(frame1, text="", justify=tk.LEFT)
output_label.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

frame2 = tk.Frame(notebook)
notebook.add(frame2, text="Additional Input")

labels2 = ["Field 1:", "Field 2:", "Field 3:", "Field 4:"]
for i, label in enumerate(labels2):
    tk.Label(frame2, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)

field1_entry = tk.Entry(frame2)
field2_entry = tk.Entry(frame2)
field3_entry = tk.Entry(frame2)
field4_entry = tk.Entry(frame2)

entries2 = [field1_entry, field2_entry, field3_entry, field4_entry]
for i, entry in enumerate(entries2):
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    frame2.columnconfigure(1, weight=1)

submit_button2 = tk.Button(frame2, text="Submit", command=lambda: messagebox.showinfo("Additional Data", "Additional data submitted!"))
submit_button2.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

note_frame = tk.Frame(root)
note_frame.pack(fill=tk.BOTH, expand=True, pady=10)

tk.Label(note_frame, text="Notes:").pack(anchor="w", padx=5)
note_text = tk.Text(note_frame, height=6)
note_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()
