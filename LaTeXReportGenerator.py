'''
LaTeX Report Generator
Gian Favero
February 2023
'''
from tkinter import *
from tkinter import filedialog
import ctypes
import tempfile
import base64
import zlib
import os

class LaTeXReportGenerator:
    def __init__(self):
        # Tkinter setup
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        self.ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
                                        'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

        _, self.ICON_PATH = tempfile.mkstemp()
        with open(self.ICON_PATH, 'wb') as icon_file:
            icon_file.write(self.ICON)

        # Report Variables
        self.report_information = {
            "File Name": "",
            "Report Title": "",
            "Course": "",
            "Professor": "",
            "Author": "",
            "Student ID": "",
            "Due Date": ""
        }

    def get_directory(self):
        root = Tk()
        root.withdraw()
        root.iconbitmap(default=self.ICON_PATH)

        # Get project path and create LaTeX folder
        folder_selected = filedialog.askdirectory()

        self.path = folder_selected + "/LaTeX"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        if not os.path.exists(folder_selected + "Images"):
            os.makedirs(folder_selected + "Images")

    def submit_entries(self):
        # Get the values from the entry fields
        for index, key in enumerate(self.report_information.keys()):
            self.report_information[key] = self.entries[index].get()
        self.root.quit()
    
    def on_closing(self):
        self.root.quit()

    def get_report_information(self):
        # Create a new tkinter self.root
        self.root = Tk()
        self.root.title("Report Information")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create entry fields for the report information
        entry_labels = ["File Name", "Report Title", "Course", "Professor", "Author", "Student Number", "Due Date"]
        self.entries = [Entry(self.root) for i in range(len(entry_labels))]

        # Set the position of the entry fields in the self.root
        for i in range(len(entry_labels)):
            Label(self.root, text=entry_labels[i]).grid(row=i, column=0, padx=5, pady=5)
            self.entries[i].grid(row=i, column=1, padx=5, pady=5)

        # Create a submit button
        submit_button = Button(self.root, text="Submit", command=self.submit_entries)
        submit_button.grid(row=len(self.entries)+1, column=1, padx=5, pady=5)

        # Start the entry self.root event loop
        self.root.mainloop()

    def generate_report(self, style):
        if style == "Favero":
            with open('LaTeX Templates/Favero/FaveroTemplate.tex', 'r') as template_file:
                template = template_file.read()
                for key in self.report_information.keys():
                    template = template.replace(f'${key}$', self.report_information[key])
                new_report = template

                filepath = os.path.join(self.path, self.report_information["File Name"] + ".tex")
                with open(filepath, 'w') as new_file:
                    new_file.write(new_report)

