import tkinter as tk
import sqlite3

# creates a window
LMS_GUI_WINDOW = tk.Tk()

# connects the GUI with the LMS database
connection = sqlite3.connect("LMS.db")

# default size of window when first created
height = LMS_GUI_WINDOW.winfo_screenheight()/2
width = LMS_GUI_WINDOW.winfo_screenwidth()/2

LMS_GUI_WINDOW.geometry(f'{int(width)}x{int(height)}')

# change the icon of the application
LMS_GUI_WINDOW.iconbitmap("./book-icon-file-13.jpg")

# set the title of the GUI
LMS_GUI_WINDOW.title("Library Management System")

# place window in the center of the screen
LMS_GUI_WINDOW.eval('tk::PlaceWindow . center')

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()

# closes the connection to the database
connection.close()