import tkinter as tk  # Import the tkinter module for creating the GUI
from tkinter import messagebox  # Import messagebox for displaying error messages
from tkinter import ttk  # Import ttk for themed widgets
import pandas as pd  # Import pandas for data manipulation (CSV reading)
import math  # Import math module for calculations
import csv  # Import csv module for reading CSV files
import webbrowser #Import webbrowser to open links.
import json #Import json to read and write json files.

# Define the filenames for the CSV files and JSON file
CSV_FILENAME = "airlines.csv"
AIRPORTS_CSV = "airports.csv"
ROUTES_CSV = "routes.csv"
NOTES_FILENAME = "user_notes.json"

def load_airline_codes(csv_filename):
    """
    Loads airline codes and names from a CSV file into a dictionary.

    Args:
        csv_filename (str): The path to the CSV file.

    Returns:
        dict: A dictionary where keys are airline codes and values are airline names.
              Returns an empty dictionary if an error occurs.
    """
    airline_codes = {}  # Initialize an empty dictionary to store airline codes and names
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as file:  # Open the CSV file in read mode
            reader = csv.reader(file)  # Create a CSV reader object
            for row in reader:  # Iterate through each row in the CSV file
                if len(row) == 2:  # Check if the row has two columns (code and name)
                    code, name = row  # Unpack the row into code and name variables
                    airline_codes[code.strip()] = name.strip()  # Add the code and name to the dictionary (remove extra spaces)
    except FileNotFoundError:  # Handle the case where the file is not found
        messagebox.showerror("Error", f"File not found: {csv_filename}") #Display error messagebox.
        return {} #Return empty dictionary.
    except Exception as e:  # Handle other exceptions
        messagebox.showerror("Error", f"An error occurred: {e}") #Display error messagebox with specific error.
        return {} #Return empty dictionary.
    return airline_codes #Return populated dictionary.

AIRLINE_CODES = load_airline_codes(CSV_FILENAME) #Load airline codes from the CSV file.

def load_airports(csv_path):
    """
    Loads airport data from a CSV file into a pandas DataFrame.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing airport data.
                      Returns an empty DataFrame if an error occurs.
    """
    try:
        return pd.read_csv(csv_path)  # Read the CSV file into a pandas DataFrame and return it
    except FileNotFoundError: #Handle file not found error.
        messagebox.showerror("Error", f"File not found: {csv_path}") #Display error messagebox.
        return pd.DataFrame() #Return empty data frame.
    except Exception as e: #Handle other exceptions.
        messagebox.showerror("Error", f"An error occurred: {e}") #Display detailed error.
        return pd.DataFrame() #Return empty dataframe.

def create_route_list(csv_file):
    """
    Creates lists of display routes and flight plan routes from a CSV file.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing two lists: display routes and flight plan routes.
               Returns two empty lists if an error occurs.
    """
    display_routes = [] #Initialize display route list.
    flight_plan_routes = [] #Initialize flight plan route list.
    try:
        with open(csv_file, 'r') as file: #Open the CSV file in read mode.
            reader = csv.reader(file) #Create a CSV reader object.
            next(reader) #Skip the header row.
            for row in reader: #Iterate through each row in the CSV file.
                if len(row) >= 3: #Check if the row has at least three columns.
                    route_name = row[1] #Extract the route name.
                    fix_name = row[2] #Extract the fix name.
                    display_routes.append(f"{route_name.replace('6',' SIX').replace('7',' SEVEN').replace('5',' FIVE').replace('4',' FOUR')} ({fix_name})") #Format the display route.
                    flight_plan_routes.append(f"{route_name.replace('6',' SIX').replace('7',' SEVEN').replace('5',' FIVE').replace('4',' FOUR')} departure, {fix_name} transition") #Format the flight plan route.
    except FileNotFoundError: #Handle file not found error.
        messagebox.showerror("Error", f"File not found: {csv_file}") #Display error messagebox.
        return [], [] #Return empty lists.
    except Exception as e: #Handle other exceptions.
        messagebox.showerror("Error", f"An error occurred: {e}") #Display detailed error.
        return [], [] #Return empty lists.
    return display_routes, flight_plan_routes #Return the display and flight plan route lists.

route_display_list, flight_plan_routes = create_route_list(ROUTES_CSV) #Create route lists from the CSV file.

def get_airport_info(df, code):
    """
    Retrieves airport information from a DataFrame based on the airport code.

    Args:
        df (pd.DataFrame): The DataFrame containing airport data.
        code (str): The airport code.

    Returns:
        pd.Series: A pandas Series containing airport information, or None if not found.
    """
    airport = df[df['ident'] == code.upper()]  # Filter the DataFrame to find the airport with the given code
    if airport.empty:  # Check if the airport was found
        return None #Return None if airport not found.
    return airport.iloc[0] #Return the first row as a Series.

def calculate_direction(lat1, lon1, lat2, lon2):
    """
    Calculates the direction (bearing) between two points given their latitudes and longitudes.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: The bearing in degrees.
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2]) #Convert latitude and longitude to radians
    d_lon = lon2 - lon1 #Calculate the difference in longitude.
    x = math.sin(d_lon) * math.cos(lat2) #Calculate x.
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon) #Calculate y.
    bearing = math.atan2(x, y) #Calculate the bearing.
    bearing = math.degrees(bearing) #Convert the bearing to degrees.
    if bearing < 0: #Adjust the bearing to be between 0 and 360 degrees.
        bearing += 360
    return round(bearing, 2) #Return the rounded bearing.

def name_heading(code1, code2, airports_df):
    """
    Calculates the heading and airport information between two airports.

    Args:
        code1 (str): The ICAO code of the departure airport.
        code2 (str): The ICAO code of the destination airport.
        airports_df (pd.DataFrame): The DataFrame containing airport data.

    Returns:
        tuple: A tuple containing the rounded heading, airport information for the departure airport,
               and airport information for the destination airport.
               Returns None, None, None if an error occurs.
    """
    airport1 = get_airport_info(airports_df, code1) #Get departure airport info.
    airport2 = get_airport_info(airports_df, code2) #Get destination airport info.
    if airport1 is None or airport2 is None: #Check if either airport was not found.
        messagebox.showerror("Error", "One or both airport codes not found.") #Display error message.
        return None, None, None #Return None values.
    heading = calculate_direction(airport1.latitude_deg, airport1.longitude_deg,
                                  airport2.latitude_deg, airport2.longitude_deg) #Calculate the heading.
    rheading = round(heading) #Round the heading.
    airport_info1 = f"{airport1.name} ({airport1.ident})" #Format the departure airport information.
    airport_info2 = f"{airport2.name} ({airport2.ident})" #Format the destination airport information.
    return rheading, airport_info1, airport_info2 #Return the rounded heading and airport information.

def altitude_cal(altitude, rheading):
    """
    Calculates the final altitude based on the input altitude and heading.

    Args:
        altitude (int): The input altitude.
        rheading (int): The rounded heading.

    Returns:
        int: The calculated final altitude.
    """
    cal_altitude = altitude / 10 #Calculate the intermediate altitude.
    heading_direction = "NE" if 0 <= rheading < 180 else "SW" #Determine the heading direction.
    if heading_direction == "NE": #Adjust the altitude based on the heading direction.
        if cal_altitude % 2 == 0:
            final_altitude = round((cal_altitude + 1) * 10)
        else:
            final_altitude = round(cal_altitude * 10)
    else:
        if cal_altitude % 2 != 0:
            final_altitude = round((cal_altitude + 1) * 10)
        else:
            final_altitude = round(cal_altitude * 10)
    return final_altitude #Return the final altitude.

def update_callsign_label(callsign_entry, callsign_label):
    """
    Updates the callsign label with the airline name based on the callsign entry.

    Args:
        callsign_entry (ttk.Entry): The callsign entry widget.
        callsign_label (ttk.Label): The callsign label widget.
    """
    callsign = callsign_entry.get().upper() #Get the callsign from the entry and convert it to uppercase.
    airline_code = callsign[:3] #Extract the airline code from the callsign.
    if airline_code in AIRLINE_CODES: #Check if the airline code is in the dictionary.
        callsign_label.config(text=f"({AIRLINE_CODES[airline_code]})") #Update the label with the airline name.
    else:
        callsign_label.config(text="") #Clear the label if the airline code is not found.

def generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var, aircraft_type_var, notes_text_box, system_notes_text_box):
    """
    Generates and displays the flight plan based on the input parameters.

    Args:
        frequency_entry (ttk.Entry): The frequency entry widget.
        callsign_entry (ttk.Entry): The callsign entry widget.
        route_var (ttk.Combobox): The route combobox widget.
        departure_entry (ttk.Entry): The departure airport entry widget.
        destination_entry (ttk.Entry): The destination airport entry widget.
        altitude_entry (ttk.Entry): The altitude entry widget.
        squawk_entry (ttk.Entry): The squawk entry widget.
        flight_plan_label (tk.Label): The flight plan label widget.
        direction_label (tk.Label): The direction label widget.
        route_night_label (tk.Label): The route night label widget.
        heading_var (tk.StringVar): The heading variable.
        aircraft_type_var (tk.StringVar): The aircraft type variable.
        notes_text_box(tk.TextBox): User note textbox.
        system_notes_text_box (tk.TextBox): System notes textbox.
    """
    frequency = frequency_entry.get() or '125.8' #Get the frequency from the entry or use a default value.
    callsign = callsign_entry.get().upper() #Get the callsign from the entry and convert it to uppercase.
    airline_code = callsign[:3] #Extract the airline code from the callsign.
    flight_number = callsign[3:] #Extract the flight number from the callsign.
    if airline_code in AIRLINE_CODES: #Check if the airline code is in the dictionary.
        callsign = f"{AIRLINE_CODES[airline_code]} {flight_number}" #Format the callsign with the airline name.
    code1 = departure_entry.get().upper() or "KMEM" #Get the departure airport code from the entry or use a default value.
    code2 = destination_entry.get().upper() #Get the destination airport code from the entry.
    route_name = route_var.get() #Get the route name from the combobox.
    night_flag = "" #Initialize the night flag.
    if route_name in ["GENEH SEVEN (NUYID)", "GMBUD SEVEN (JADET)", "OLEMS SIX (LEYIK)", "BINKY SIX (BASBE)", "AUTMN SIX (LUVEC)", "NIKEI FIVE (INAYO)", "HOTRD FIVE (TOMKE)", "GRRIZ FIVE (MIEDZ)", "ELVIS FOUR (NFIVE)", "ELVIS FOUR (EFOUR)", "ELVIS FOUR (STREE)", "ELVIS FOUR (SFOUR)", "ELVIS FOUR (WFIVE)"]: #Check if the route is a night route.
        night_flag = " (Night SID)" #Set the night flag.
        route_night_label.config(text="Night SID") #Update the route night label.
    else:
        route_night_label.config(text="") #Clear the route night label.
    route_index = route_display_list.index(route_name) #Get the index of the route in the display list.
    route = flight_plan_routes[route_index] #Get the flight plan route from the list.
    airports_df = load_airports(AIRPORTS_CSV) #Load the airports DataFrame.
    rheading, airport_info1, airport_info2 = name_heading(code1, code2, airports_df) #Calculate the heading and airport information.
    if rheading is None: #Check if an error occurred.
        return #Exit the function.
    flight_direction = "NE" if 0 <= rheading < 180 else "SW" #Determine the flight direction.
    direction_label.config(text=f"Direction: {flight_direction}") #Update the direction label.
    heading_var.set(f"Heading: {rheading}°") #Update the heading variable.
    altitude = int(altitude_entry.get()) #Get the altitude from the entry.
    final_altitude = altitude_cal(altitude, rheading) #Calculate the final altitude.
    sub1 = "" if final_altitude >= 200 else "00" #Determine the altitude suffix.
    sub2 = "FL " if final_altitude >= 200 else "" #Determine the altitude prefix.
    aircraft_type = aircraft_type_var.get() #Get the aircraft type.
    initial_altitude = 3000 if aircraft_type == "Prop" else 5000 #Determine the initial altitude based on the aircraft type.
    flight_plan_label.config(text=f'{callsign}, cleared to {airport_info2}, via {route}{night_flag}, \n'
                                  f'then as filed, maintain {initial_altitude}, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
                                  f'departure frequency {frequency}, squawk {squawk_entry.get()}') #Format and display the flight plan.
    print(f'{callsign}, cleared to {airport_info2}, via {route}, \n'
          f'then as filed, maintain {initial_altitude}, expect {sub2}{final_altitude}{sub1} 1-0 minutes after departure, \n'
          f'departure frequency {frequency}, squawk {squawk_entry.get()} \n\n'
          f'****************************************************\n\n') #Print the flight plan to the console.
    notes = [] #Initialize the notes list.
    if altitude != final_altitude: #Check if the input altitude does not match the calculated final altitude.
        notes.append(f"Altitude Note: Input altitude {altitude} does not match calculated final altitude {final_altitude}.") #Add an altitude note.
    if aircraft_type == "Prop" and code1.upper() != "KMEM" and "ELVIS FOUR" not in route_name: #Check if a prop plane is departing from a non-KMEM airport.
        notes.append("Prop Note: Prop planes can only depart from KMEM (Elvis).") #Add a prop plane note.
    if night_flag: #Check if the route is a night route.
        notes.append(f"Night Note: {route_name} is a 0200-0600 only SID.") #Add a night route note.
    notes.append(f"Direction: {flight_direction}") #Add the flight direction to the notes.
    system_notes_text_box.delete(1.0, tk.END) #Clear the system notes textbox.
    if notes: #Check if there are notes.
        system_notes_text_box.config(fg="red") #Set the text color to red.
        system_notes_text_box.insert(tk.END, "\n".join(notes)) #Insert the notes into the textbox.
    else:
        system_notes_text_box.config(fg="black") #Set the text color to black.

current_text_color = "black" #Initialize the current text color.
tag_colors_dict = {} #Initialize the tag colors dictionary.

def change_text_color(color):
    """
    Changes the text color of the selected text in the notes textbox.

    Args:
        color (str): The color to change the text to.
    """
    global current_text_color #Access the global current text color variable.
    current_text_color = color #Set the current text color.
    notes_text_box.tag_configure(color, foreground=color) #Configure the tag for the color.
    tag_colors_dict[color] = color #Add the color to the tag colors dictionary.
    try:
        notes_text_box.tag_add(color, "sel.first", "sel.last") #Add the tag to the selected text.
    except tk.TclError: #Handle the case where no text is selected.
        pass

def save_notes(notes, tag_ranges, tag_colors):
    """
    Saves the notes, tag ranges, and tag colors to a JSON file.

    Args:
        notes (str): The notes text.
        tag_ranges (dict): A dictionary of tag ranges.
        tag_colors (dict): A dictionary of tag colors.
    """
    serializable_tag_ranges = {} #Initialize the serializable tag ranges dictionary.
    for tag, ranges in tag_ranges.items(): #Iterate through the tag ranges.
        serializable_ranges = [] #Initialize the serializable ranges list.
        for r in ranges: #Iterate through the ranges.
            if isinstance(r, str): #Check if the range is a string.
                serializable_ranges.append(r) #Add the range to the serializable ranges list.
        serializable_tag_ranges[tag] = serializable_ranges #Add the tag and serializable ranges to the dictionary.
    try:
        with open(NOTES_FILENAME, 'w') as file: #Open the JSON file in write mode.
            json.dump({"notes": notes, "tag_ranges": serializable_tag_ranges, "tag_colors": tag_colors}, file) #Dump the notes, tag ranges, and tag colors to the file.
    except Exception as e: #Handle exceptions.
        messagebox.showerror("Error", f"Failed to save notes: {e}") #Display error messagebox.

def load_notes():
    """
    Loads the notes, tag ranges, and tag colors from a JSON file.

    Returns:
        tuple: A tuple containing the notes text, tag ranges dictionary, and tag colors dictionary.
               Returns empty values if an error occurs.
    """
    try:
        with open(NOTES_FILENAME, 'r') as file: #Open the JSON file in read mode.
            data = json.load(file) #Load the data from the file.
            return data["notes"], data["tag_ranges"], data["tag_colors"] #Return the notes, tag ranges, and tag colors.
    except FileNotFoundError: #Handle file not found error.
        return "", {}, {} #Return empty values.
    except Exception as e: #Handle other exceptions.
        messagebox.showerror("Error", f"Failed to load notes: {e}") #Display error messagebox.
        return "", {}, {} #Return empty values.

root = tk.Tk() #Create the main window.
root.title("Flight Plan Generator") #Set the window title.
root.geometry("850x1000") #Set the window size.
root.resizable(True, True) #Make the window resizable.

top_frame = ttk.Frame(root) #Create the top frame.
top_frame.pack(fill=tk.X) #Pack the top frame.

notebook = ttk.Notebook(top_frame, height=450) #Create the notebook widget.
notebook.pack(fill=tk.X, expand=False) #Pack the notebook widget.

frame1 = ttk.Frame(notebook, padding=10) #Create the first frame for IFR.
frame2 = ttk.Frame(notebook) #Create the second frame for VFR.

notebook.add(frame1, text="IFR") #Add the first frame to the notebook.
notebook.add(frame2, text="VFR") #Add the second frame to the notebook.

frame1.columnconfigure(0, weight=1) #Configure the column weights for the first frame.
frame1.columnconfigure(1, weight=2)

Frequency = tk.StringVar(value="125.8") #Create a string variable for the frequency.
ttk.Label(frame1, text="Frequency:").grid(row=0, column=0, sticky="ew", padx=5, pady=5) #Create and pack the frequency label.
frequency_entry = ttk.Entry(frame1, textvariable=Frequency) #Create and pack the frequency entry.
frequency_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

Callsign = tk.StringVar(value="AAL123") #Create a string variable for the callsign.
ttk.Label(frame1, text="Callsign:").grid(row=1, column=0, sticky="ew", padx=5, pady=5) #Create and pack the callsign label.
callsign_entry = ttk.Entry(frame1, textvariable=Callsign) #Create and pack the callsign entry.
callsign_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
callsign_label = ttk.Label(frame1, text="") #Create and pack the callsign label.
callsign_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
callsign_entry.bind("<KeyRelease>", lambda event: update_callsign_label(callsign_entry, callsign_label)) #Bind the key release event to update the callsign label.

Aircraft_Type = tk.StringVar(value="Jet") #Create a string variable for the aircraft type.
ttk.Label(frame1, text="Aircraft Type:").grid(row=2, column=0, sticky="ew", padx=5, pady=5) #Create and pack the aircraft type label.
aircraft_dropdown = ttk.Combobox(frame1, textvariable=Aircraft_Type, values=["Jet", "Prop"], state="readonly") #Create and pack the aircraft type combobox.
aircraft_dropdown.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
aircraft_dropdown.current(0) #Set the default aircraft type.

Departure = tk.StringVar(value="KMEM") #Create a string variable for the departure airport.
ttk.Label(frame1, text="Departure ICAO:").grid(row=3, column=0, sticky="ew", padx=5, pady=5) #Create and pack the departure airport label.
departure_entry = ttk.Entry(frame1, textvariable=Departure) #Create and pack the departure airport entry.
departure_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

Destination = tk.StringVar(value="KLAX") #Create a string variable for the destination airport.
ttk.Label(frame1, text="Destination ICAO:").grid(row=4, column=0, sticky="ew", padx=5, pady=5) #Create and pack the destination airport label.
destination_entry = ttk.Entry(frame1, textvariable=Destination) #Create and pack the destination airport entry.
destination_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

Route_Display = tk.StringVar(value=route_display_list[0]) #Create a string variable for the route.
ttk.Label(frame1, text="Route:").grid(row=5, column=0, sticky="ew", padx=5, pady=5) #Create and pack the route label.
route_var = ttk.Combobox(frame1, textvariable=Route_Display, values=route_display_list, state="readonly") #Create and pack the route combobox.
route_var.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
route_var.current(0) #Set the default route.

Altitude = tk.StringVar(value="350") #Create a string variable for the altitude.
ttk.Label(frame1, text="Altitude:").grid(row=6, column=0, sticky="ew", padx=5, pady=5) #Create and pack the altitude label.
altitude_entry = ttk.Entry(frame1, textvariable=Altitude) #Create and pack the altitude entry.
altitude_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

Squawk = tk.StringVar(value="2200") #Create a string variable for the squawk code.
ttk.Label(frame1, text="Squawk:").grid(row=7, column=0, sticky="ew", padx=5, pady=5) #Create and pack the squawk label.
squawk_entry = ttk.Entry(frame1, textvariable=Squawk) #Create and pack the squawk entry.
squawk_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

flight_plan_label = tk.Label(frame1, text="Flight Plan:", justify=tk.LEFT) #Create and pack the flight plan label.
flight_plan_label.grid(row=9, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

route_night_label = tk.Label(frame1, text="") #Create and pack the route night label.
route_night_label.grid(row=11, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

heading_var = tk.StringVar(value="0.00°") #Create a string variable for the heading.
ttk.Label(frame1, textvariable=heading_var).grid(row=12, column=0, columnspan=2, sticky="ew", padx=0, pady=0) #Create and pack the heading label.

direction_label = tk.Label(frame1, text="") #Create and pack the direction label.
direction_label.grid(row=13, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

ttk.Button(frame1, text="Update Flight Plan", command=lambda: generate_flight_plan(frequency_entry, callsign_entry, route_var, departure_entry, destination_entry, altitude_entry, squawk_entry, flight_plan_label, direction_label, route_night_label, heading_var, Aircraft_Type, notes_text_box, system_notes_text_box)).grid(row=8, column=0, columnspan=2, pady=10) #Create and pack the update flight plan button.

def GoToLink():
    """
    Opens a link in the default web browser.
    """
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ") #Open the link.

ttk.Label(frame2, text="VFR Flight Plan Coming Soon!").grid(row=0, column=0, columnspan=2, pady=20) #Create and pack the VFR flight plan label.
ttk.Label(frame2, text="\
    - VFR clearances are are carbon copy of one another! (callsign), \n\
        Cleared into the Memphis Class Bravo Airspace, Maintain VFR at or below 2500. \n\
        Departure frequency XXX.XX, squawk XXXX\n\n\
    - We have to fill out the flight plan editor for VFR aircraft! The most important part \n\
        is the aircraft type, direction of flight, and the VFR altitude! It goes in as VFR/XXX\n\n\
    - These clearances differ at different airspaces! Charlies don't require the clearance portion.\n\n\
    - VFR clearances are very simple to give and therefore can be prioritized in the queue \n\
        instead of IFR clearances which require a full route check.").grid(row=3, column=0, columnspan=2, pady=20) #Create and pack the VFR flight plan information label.
my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white") #Create and pack the click me button.
my_button.grid(row=1, column=0, columnspan=2, pady=10)

system_notes_frame = ttk.Frame(root, padding=5) #Create the system notes frame.
system_notes_frame.pack(fill=tk.X) #Pack the system notes frame.
tk.Label(system_notes_frame, text="System Notes:").pack() #Create and pack the system notes label.
system_notes_text_box = tk.Text(system_notes_frame, height=4, wrap="word") #Create and pack the system notes textbox.
system_notes_text_box.pack(fill=tk.X)

notes_frame = ttk.Frame(root, padding=5) #Create the notes frame.
notes_frame.pack(fill=tk.BOTH, expand=True) #Pack the notes frame.
tk.Label(notes_frame, text="Your Notes:").grid(row=0, column=0, sticky="w", padx=5, pady=0) #Create and pack the notes label.
notes_text_box = tk.Text(notes_frame, height=6, wrap="word") #Create and pack the notes textbox.
scrollbar = tk.Scrollbar(notes_text_box, command=notes_text_box.yview) #Create and pack the scrollbar.
notes_text_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=0) #Grid the notes textbox.
notes_text_box.config(yscrollcommand=scrollbar.set) #Configure the scrollbar.
color_bar = ttk.Frame(notes_frame) #Create the color bar frame.
color_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5) #Grid the color bar frame.
colors = ["black", "red", "blue", "green", "purple", "orange", "white"] #Define the colors.
for i, color in enumerate(colors): #Iterate through the colors.
    style = ttk.Style() #Create a style object.
    style.configure(f"{color}.TButton", background=color) #Configure the style.
    color_button = ttk.Button(color_bar, text=color.capitalize(), width=6, style=f"{color}.TButton", command=lambda c=color: change_text_color(c)) #Create and pack the color button.
    color_button.grid(row=0, column=i, padx=2) #Grid the color button.
notes_frame.grid_rowconfigure(1, weight=1) #Configure the row weight.
notes_frame.grid_columnconfigure(0, weight=1) #Configure the column weight.

def on_closing():
    """
    Saves the notes and closes the window.
    """
    tag_ranges = {} #Initialize the tag ranges dictionary.
    tag_colors = {} #Initialize the tag colors dictionary.
    for tag in notes_text_box.tag_names(): #Iterate through the tags.
        if tag != "sel": #Check if the tag is not the selection tag.
            tag_ranges[tag] = list(notes_text_box.tag_ranges(tag)) #Get the tag ranges.
            if tag in tag_colors_dict: #Check if the tag is in the tag colors dictionary.
                tag_colors[tag] = tag_colors_dict[tag] #Get the tag color.
    save_notes(notes_text_box.get(1.0, tk.END), tag_ranges, tag_colors) #Save the notes.
    root.destroy() #Destroy the window.
root.protocol("WM_DELETE_WINDOW", on_closing)

# Load notes when the application starts
loaded_notes, loaded_tag_ranges, loaded_tag_colors = load_notes()
notes_text_box.insert(tk.END, loaded_notes)

# Apply loaded tags and colors
for tag, ranges in loaded_tag_ranges.items():
    if ranges:
        for i in range(0, len(ranges), 2):
            notes_text_box.tag_add(tag, ranges[i], ranges[i+1])
            if tag in loaded_tag_colors: # Check if color exists
                notes_text_box.tag_configure(tag, foreground=loaded_tag_colors[tag])
                tag_colors_dict[tag] = loaded_tag_colors[tag] # Add the tag back to the dictionary

# --- Run the application ---
if __name__ == "__main__":
    root.mainloop()