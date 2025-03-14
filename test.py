import tkinter as tk
from tkinter import ttk
import csv

# Function to read routes from CSV
def read_routes(csv_filename):
    routes = []
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            routes.append(f"{row[1]} {row[2]}")  # Format: ID - Route (Fix)
    return routes

# Load routes from CSV
csv_filename = "routes.csv"
routes = read_routes(csv_filename)

# Create the main window
root = tk.Tk()
root.title("Route Selector")

# Dropdown label
label = tk.Label(root, text="Select a Route:")
label.pack(pady=10)

# Create a StringVar to store the selected route
selected_route = tk.StringVar()

# Create a dropdown menu
dropdown = ttk.Combobox(root, textvariable=selected_route, values=routes, state="readonly")
dropdown.pack(pady=10)

def on_select(event):
    print("Selected Route:", selected_route.get())

# Bind the selection event
dropdown.bind("<<ComboboxSelected>>", on_select)

# Run the application
root.mainloop()
