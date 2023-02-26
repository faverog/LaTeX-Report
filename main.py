import os
from tkinter import filedialog, simpledialog
from tkinter import *
import ctypes
import tempfile
import base64
import zlib
from helpers import *

# Tkinter setup
ctypes.windll.shcore.SetProcessDpiAwareness(2)

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
                                        'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

root = Tk()
root.withdraw()
root.iconbitmap(default=ICON_PATH)

# Get project path and create LaTeX folder
folder_selected = filedialog.askdirectory()

new_path = folder_selected + "/LaTeX"
if not os.path.exists(new_path):
    os.makedirs(new_path)

# Get report information
# Create a new tkinter window
window = Tk()
window.title("Report Information")

# Create entry fields for the report information
entry_labels = ["File Name", "Report Title", "Professor", "Author", "Student Number", "Due Date"]
entries = [Entry(window) for i in range(len(entry_labels))]

# Set the position of the entry fields in the window
for i in range(len(entry_labels)):
    Label(window, text=entry_labels[i]).grid(row=i, column=0, padx=5, pady=5)
    entries[i].grid(row=i, column=1, padx=5, pady=5)

# Create a submit button
submit_button = Button(window, text="Submit", command)
submit_button.grid(row=len(entries)+1, column=0, padx=5, pady=5)

# Start the tkinter event loop
window.mainloop()
