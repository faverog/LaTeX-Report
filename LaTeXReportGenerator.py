'''
LaTeX Report Generator
Gian Favero
February 2023
'''
import sys
from tkinter import *
from tkinter import filedialog
import ctypes
import tempfile
import base64
import zlib
import os
import shutil

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
            "Template": "",
            "Info Keys": {},
        }

        self.entries = []
        self.selected_template = ""

    def get_directory(self):
        self.root = Tk()
        self.root.withdraw()
        self.root.iconbitmap(default=self.ICON_PATH)

        # Get project path and create LaTeX folder
        folder_selected = filedialog.askdirectory()

        self.path = folder_selected + "/LaTeX"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        if not os.path.exists(folder_selected + "/LaTeX Images"):
            os.makedirs(folder_selected + "/LaTeX Images")
        
    def get_template(self):
        self.root = Tk()
        self.root.title("Report Template")
        self.root.geometry("300x100")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        label = Label(self.root, text="Select a report template:")
        label.grid(row=0, column=0, padx=5, pady=5)

        options = ["Favero", "Capstone Report", "Favero 2"]
        self.selected_template = StringVar(self.root)

        self.selected_template.set(options[0])

        dropdown = OptionMenu(self.root, self.selected_template, *options)
        dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        submit_button = Button(self.root, text="Submit", command=self.submit_template_entry)
        submit_button.grid(row=1, column=1, padx=5, pady=5)

        self.root.mainloop()

    def submit_template_entry(self):
        self.report_information["Template"] = self.selected_template.get()
        print("Template Chosen: ", self.report_information["Template"])
        self.root.quit()
        self.root.destroy()

    def submit_info_entries(self):
        # Get the values from the entry fields
        for index, key in enumerate(self.report_information["Info Keys"].keys()):
            self.report_information["Info Keys"][key] = self.entries[index].get()
        
        print("Report Information:", self.report_information)
        self.root.quit()
    
    def on_closing(self):
        self.root.quit()
        print("Program terminated")
        sys.exit()

    def get_report_information(self):
        # Create a new tkinter self.root
        self.root = Tk()
        self.root.title("Report Information")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create entry fields for the report information
        if self.report_information["Template"] == "Favero":
            entry_labels = ["File Name", "Report Title", "Course", "Professor", "Author", "Student ID", "Due Date"]
        elif self.report_information["Template"] == "Capstone Report":
            entry_labels = ["File Name", "Date"]
        elif self.report_information["Template"] == "Favero 2":
            entry_labels = ["File Name", "Report Title", "Course", "Author", "Student ID", "Due Date"]
        self.report_information["Info Keys"] = {key: "" for key in entry_labels}
        self.entries = [Entry(self.root) for i in range(len(entry_labels))]

        # Set the position of the entry fields in the self.root
        for i in range(len(entry_labels)):
            Label(self.root, text=entry_labels[i]).grid(row=i, column=0, padx=5, pady=5)
            self.entries[i].grid(row=i, column=1, padx=5, pady=5)

        # Create a submit button
        submit_button = Button(self.root, text="Submit", command=self.submit_info_entries)
        submit_button.grid(row=len(self.entries)+1, column=1, padx=5, pady=5)

        # Start the entry self.root event loop
        self.root.mainloop()

    def generate_report(self):
        path = ""
        if self.report_information["Template"] == "Favero":
            path = 'LaTeX Templates/Favero/FaveroTemplate.tex'
            shutil.copyfile('LaTeX Templates/Favero/mcode.sty', os.path.join(self.path, 'mcode.sty'))
            shutil.copyfile('LaTeX Templates/Favero/matlab.sty', os.path.join(self.path, 'matlab.sty'))
        elif self.report_information["Template"] == "Capstone Report":
            path = 'LaTeX Templates/Capstone Progress Updates/ProgressReport.tex'
            shutil.copyfile('LaTeX Templates/Capstone Progress Updates/assignment.cls', os.path.join(self.path, 'assignment.cls'))
            shutil.copyfile('LaTeX Templates/Capstone Progress Updates/UWin Logo.jpg', os.path.join(self.path, 'UWin Logo.jpg'))
            shutil.copyfile('LaTeX Templates/Capstone Progress Updates/GanttChart.png', os.path.join(self.path, 'GanttChart.png'))
        elif self.report_information["Template"] == "Favero 2":
            path = 'LaTeX Templates/Favero 2/Favero 2.tex'
            shutil.copyfile('LaTeX Templates/Favero 2/assignment.cls', os.path.join(self.path, 'assignment.cls'))
            shutil.copyfile('LaTeX Templates/Favero 2/UWin Logo.jpg', os.path.join(self.path, 'UWin Logo.jpg'))
            shutil.copyfile('LaTeX Templates/Favero 2/mcgill_logo.jpg', os.path.join(self.path, 'mcgill_logo.jpg'))

        if path != "":
            print("Generating Report...")
            with open(path, 'r') as template_file:
                template = template_file.read()
                for key in self.report_information["Info Keys"].keys():
                    template = template.replace(f'${key}$', self.report_information["Info Keys"][key])
                new_report = template

                filepath = os.path.join(self.path, self.report_information["Info Keys"]["File Name"] + ".tex")
                with open(filepath, 'w') as new_file:
                    new_file.write(new_report)

            print("Report Generated Successfully!")
        else:
            print("Error with template selection")