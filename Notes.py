import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

NOTES_FILENAME = "user_notes.json"

def change_text_color(color):
    """Colors the selected text."""
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
root.title("Colorful Notes Box")
root.geometry("600x450")

notes_frame = ttk.Frame(root, padding=5)
notes_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(notes_frame, text="Your Notes:").grid(row=0, column=0, sticky="w", padx=5, pady=0)
notes_text_box = tk.Text(notes_frame, height=10, wrap="word")
notes_text_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=0)

color_frame = ttk.Frame(notes_frame)
color_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# Color buttons
colors = ["black", "white", "red", "blue", "green", "yellow", "purple", "orange", "gray"]
for i, color in enumerate(colors):
    button = ttk.Button(color_frame, text=color.capitalize(), command=lambda c=color: change_text_color(c))
    button.grid(row=0, column=i, padx=2)

notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)

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