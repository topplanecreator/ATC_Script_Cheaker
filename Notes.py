import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

NOTES_FILENAME = "user_notes.json"

def change_text_color(color):
    """Changes the selected text to the specified color."""
    notes_text_box.tag_configure(color, foreground=color)
    try:
        sel_start = "sel.first"
        sel_end = "sel.last"

        # Remove existing color tags
        for tag in notes_text_box.tag_names():
            if tag != "sel":
                notes_text_box.tag_remove(tag, sel_start, sel_end)

        notes_text_box.tag_add(color, sel_start, sel_end)
    except tk.TclError:
        pass

def save_notes(notes, tag_ranges, tag_colors):
    """Saves the notes, tag ranges, and tag colors to a JSON file."""
    serializable_tag_ranges = {}
    for tag, ranges in tag_ranges.items():
        serializable_ranges = []
        for r in ranges:
            if isinstance(r, str):
                serializable_ranges.append(r)
        serializable_tag_ranges[tag] = serializable_ranges
    try:
        with open(NOTES_FILENAME, 'w') as file:
            json.dump({"notes": notes, "tag_ranges": serializable_tag_ranges, "tag_colors": tag_colors}, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save notes: {e}")

def load_notes():
    """Loads notes from a JSON file."""
    try:
        with open(NOTES_FILENAME, 'r') as file:
            data = json.load(file)
            return data["notes"], data["tag_ranges"], data["tag_colors"]
    except FileNotFoundError:
        return "", {}, {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load notes: {e}")
        return "", {}, {}

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
    tag_ranges = {}
    tag_colors = {}
    for tag in notes_text_box.tag_names():
        if tag != "sel":
            tag_ranges[tag] = list(notes_text_box.tag_ranges(tag))
            tag_colors[tag] = notes_text_box.tag_cget(tag, "foreground")
    save_notes(notes_text_box.get(1.0, tk.END), tag_ranges, tag_colors)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

loaded_notes, loaded_tag_ranges, loaded_tag_colors = load_notes()
notes_text_box.insert(tk.END, loaded_notes)

for tag, ranges in loaded_tag_ranges.items():
    if ranges:
        for i in range(0, len(ranges), 2):
            notes_text_box.tag_add(tag, ranges[i], ranges[i+1])
            notes_text_box.tag_configure(tag, foreground=loaded_tag_colors.get(tag, 'black'))

if __name__ == "__main__":
    root.mainloop()