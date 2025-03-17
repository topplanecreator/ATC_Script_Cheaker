import tkinter as tk
from tkinter import ttk
import webbrowser

# Update function
def update_Flight_Plan():
    flight_plan_text = (f"Flight Plan: {Callsign.get()} | {Departure.get()} → {Destination.get()} "
                         f"via {Route.get()} at {Altitude.get()} ft | Squawk: {Squawk.get()}")
    Flight_Plan.set(flight_plan_text)

# Initialize root window
root = tk.Tk()
root.title("My Test Tkinter")
root.geometry("500x700")  # Set a reasonable default size
root.resizable(True, True)

# Create notebook (tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

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

Departure = tk.StringVar(value="KJFK")
ttk.Label(frame1, text="Departure:").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Departure).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

Destination = tk.StringVar(value="KLAX")
ttk.Label(frame1, text="Destination:").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Destination).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

Route = tk.StringVar(value="DCT HTO J174 DCT")
ttk.Label(frame1, text="Route:").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Route).grid(row=4, column=1, sticky="ew", padx=5, pady=5)

Altitude = tk.StringVar(value="35000")
ttk.Label(frame1, text="Altitude (ft):").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Altitude).grid(row=5, column=1, sticky="ew", padx=5, pady=5)

Squawk = tk.StringVar(value="2200")
ttk.Label(frame1, text="Squawk:").grid(row=6, column=0, sticky="ew", padx=5, pady=5)
ttk.Entry(frame1, textvariable=Squawk).grid(row=6, column=1, sticky="ew", padx=5, pady=5)

# Flight Plan Display
Flight_Plan = tk.StringVar(value="Flight Plan:")
ttk.Label(frame1, textvariable=Flight_Plan).grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Add Update Button
ttk.Button(frame1, text="Update Flight Plan", command=update_Flight_Plan).grid(row=8, column=0, columnspan=2, pady=10)

# ************************** Frame2 (VFR) ************************** #
def GoToLink():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # My link

ttk.Label(frame2, text="VFR Flight Plan Coming Soon!").pack(pady=20)

# Fixed button layout
my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white")
my_button.pack(pady=10)  # Consistent layout method

# Run the application
root.mainloop()
