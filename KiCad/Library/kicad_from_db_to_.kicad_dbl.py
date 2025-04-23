""" 
This python script is capable of generating a .kicad_dbl file from a database file (.db).

Parameters
----------
database file (.db):    The database file to be converted.
kicad_dbl file:         The .kicad_dbl file to be generated.

Notes
-----
Author:     Manuel Caballero
Date:       23/April/2025
Version:    23/April/2025    The ORIGIN

This code belongs to AqueronteBlog and is licensed under the MIT License.
You can use it for any purpose, but you must include the original license and 
copyright notice in any copies or substantial portions of the code.

Follow me on:
            - GitHub:  https://github.com/AqueronteBlog
            - YouTube: https://www.youtube.com/user/AqueronteBlog
            - X:       https://twitter.com/aqueronteblog
"""
import sqlite3
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

def load_database_and_generate_json():
    # Open a file dialog to select the database file
    db_file = filedialog.askopenfilename(
        title="Select SQLite Database",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
    )
    if not db_file:
        return

    try:
        # Extract the database file name without the extension
        db_name = os.path.splitext(os.path.basename(db_file))[0]

        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Query to get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            messagebox.showinfo("No Tables", "No tables found in the database.")
            return

        # Generate the JSON structure
        json_data = {
            "meta": {
                "version": 0
            },
            "name": "KiCad database",
            "description": "A database of components",
            "source": {
                "type": "odbc",
                "dsn": "",
                "username": "",
                "password": "",
                "timeout_seconds": 2,
                "connection_string": f"DSN={db_name};"
            },
            "libraries": []
        }

        # Add tables to the libraries section
        for table in tables:
            table_name = table[0]
            library_entry = {
                "name": table_name,
                "table": table_name,
                "key": "Manufacturer Part Number",
                "symbols": "Symbol",
                "footprints": "Footprint",
                "fields": [
                    {"column": "Manufacturer Part Number", "name": "Manufacturer Part Number", "inherit_properties": True},
                    {"column": "Value", "name": "Value", "inherit_properties": True},
                    {"column": "Manufacturer", "name": "Manufacturer", "inherit_properties": True},
                    {"column": "Description", "name": "Description", "inherit_properties": True},
                    {"column": "Datasheet", "name": "Datasheet", "inherit_properties": True},
                    {"column": "Verified", "name": "Verified", "inherit_properties": True},
                    {"column": "Supplier 1", "name": "Supplier 1", "inherit_properties": True},
                    {"column": "Supplier 1 Part Number", "name": "Supplier 1 Part Number", "inherit_properties": True},
                    {"column": "Supplier 2", "name": "Supplier 2", "inherit_properties": True},
                    {"column": "Supplier 2 Part Number", "name": "Supplier 2 Part Number", "inherit_properties": True}
                ]
            }
            json_data["libraries"].append(library_entry)

        # Save the JSON file
        output_file = filedialog.asksaveasfilename(
            title="Save kicad_dbl File",
            defaultextension=".kicad_dbl",
            filetypes=[("kicad_dbl Files", "*.kicad_dbl"), ("All Files", "*.*")]
        )
        if not output_file:
            return

        with open(output_file, "w") as file:
            json.dump(json_data, file, indent=4)

        messagebox.showinfo("Success", f"kicad_dbl file saved: {output_file}")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def open_hyperlink():
    webbrowser.open("https://www.youtube.com/AqueronteBlog")

# Create the main application window
root = tk.Tk()
root.title("KiCad - DB to kicad_dbl Converter")

# Create a button to load the database and generate the JSON file
convert_button = tk.Button(root, text="Load Database and Generate kicad_dbl", command=load_database_and_generate_json)
convert_button.pack(pady=20)

# Add a hyperlink to the specified website
link = tk.Label(root, text="Visit AqueronteBlog", fg="blue", cursor="hand2")
link.pack(pady=10)
link.bind("<Button-1>", lambda e: open_hyperlink())

# Run the application
root.mainloop()