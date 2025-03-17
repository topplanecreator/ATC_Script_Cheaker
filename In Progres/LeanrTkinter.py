import tkinter as tk
from tkinter import ttk
import webbrowser

def update_label():
    label_text.set(f"Now for the fun: {selected_option1.get()} {input1.get()}")
    label_text.set(f"Now for the fun: {selected_option1.get()} {input1.get()}")

root = tk.Tk()
root.title("My test Tkinter")
root.resizable(True, True)

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for tabs
frame1 = tk.Frame(notebook)
frame2 = tk.Frame(notebook)

frame1.pack(fill=tk.BOTH, expand=True)
frame2.pack(fill=tk.BOTH, expand=True)

notebook.add(frame1, text="Tab1")
notebook.add(frame2, text="Tab2")

#**************************         Frame1          **************************#

# Apply column weights in frame1
frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)

# Label inside frame1
tk.Label(frame1, text="Is this a Dropdown").grid(row=0, column=0, sticky="ew", padx=5, pady=5)

# Dropdown inside frame1
selected_option1 = tk.StringVar(value="Hi")  # Default value
dropdown1 = tk.OptionMenu(frame1, selected_option1, "Hi", "By", "test1", "test2")
dropdown1.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

# Input Box
tk.Label(frame1, text="Is this an input box").grid(row=1, column=0, sticky="ew", padx=5, pady=5)

input1 = tk.Entry(frame1)
input1.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Label for displaying updates
label_text = tk.StringVar(value="Now for the fun: ")
label_display = tk.Label(frame1, textvariable=label_text)
label_display = tk.Label(frame1, textvariable=label_text)
label_display.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Button to update label
update_button = tk.Button(frame1, text="Cool Butten", command=update_label)
update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

#**************************         Frame2          **************************#

def GoToLink():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # My link

# Apply column weights in frame2
frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)

# Label inside frame2
label2 = tk.Label(frame2, text="Is this a box?")
label2.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)  # Centered label

# Dropdown inside frame2
selected_option2 = tk.StringVar(value="Hi")  # Separate variable for selection
dropdown2 = tk.OptionMenu(frame2, selected_option2, "Hi", "By", "test1", "test2")
dropdown2.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)  # Moves dropdown down

# my Button
my_button = tk.Button(frame2, text="Click me!", command=GoToLink, bg="red", fg="white")
my_button.grid(row=2, column=0, columnspan=2, pady=10)  # Centered button


# Run the application
root.mainloop()
