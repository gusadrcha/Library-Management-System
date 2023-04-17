import tkinter as tk

LMS_GUI_WINDOW = tk.Tk()

# default size of window when first created
height = LMS_GUI_WINDOW.winfo_screenheight()/2
width = LMS_GUI_WINDOW.winfo_screenwidth()/2

LMS_GUI_WINDOW.geometry(f'{int(width)}x{int(height)}')

# set the title of the GUI
LMS_GUI_WINDOW.title("Library Management System")

# place window in the center of the screen
LMS_GUI_WINDOW.eval('tk::PlaceWindow . center')

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()