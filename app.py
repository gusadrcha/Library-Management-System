import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import sqlite3

_white = "#ffffff"
_black = "#00171f"
_navyblue = "#003459"
_blue = "#007ea7"
_skyblue = "#00a8e8"

# creates a window
LMS_GUI_WINDOW = tk.Tk()

LMS_GUI_WINDOW.config(bg=_black)

# connects the GUI with the LMS database
connection = sqlite3.connect("LMS.db")

# default size of window when first created
height = LMS_GUI_WINDOW.winfo_screenheight()
width = LMS_GUI_WINDOW.winfo_screenwidth()

print(height, width)

LMS_GUI_WINDOW.geometry(f'{int(height)}x{int(width)}')

# change the icon of the application
LMS_GUI_WINDOW.iconbitmap("book-icon-file-13.jpg")

# set the title of the GUI
LMS_GUI_WINDOW.title("Library Management System")

tabControl = ttk.Notebook(LMS_GUI_WINDOW)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Query 1")
tabControl.add(tab2, text="Query 2")
tabControl.add(tab3, text="Query 3")
tabControl.add(tab4, text="Query 4")
tabControl.add(tab5, text="Query 5")

tabControl.pack(expand=1, fill='both')

# -- Query 1 --
# book input frame that holds all book entries-----------------
bookInputFrame1 = tk.Frame(tab1, background="white")
bookInputFrame1.grid(row=0, column=0, padx=20, pady=20)

# T = Text(root, bg, fg, bd, height, width, font, ..)
Q1DescriptionLabel = tk.Label(bookInputFrame1,
                              text="Check Out a Book").grid(row=0, column=0, columnspan=4, pady=10)

bookNameEntry = tk.Entry(bookInputFrame1)
bookNameEntryLabel = tk.Label(bookInputFrame1, text="Book Title")
bookNameEntryLabel.grid(row=1, column=0, sticky='sw')
bookNameEntry.grid(row=2, column=0, columnspan=2)

bookIDEntry = tk.Entry(bookInputFrame1)
bookIDEntryLabel = tk.Label(bookInputFrame1, text="Book ID")
bookIDEntryLabel.grid(row=1, column=2, sticky="sw")
bookIDEntry.grid(row=2, column=2, columnspan=2)

bookPublisherEntry = tk.Entry(bookInputFrame1)
bookPublisherEntryLabel = tk.Label(bookInputFrame1, text="Book Publisher")
bookPublisherEntryLabel.grid(row=3, column=0, sticky="sw")
bookPublisherEntry.grid(row=4, column=0, columnspan=2)

bookBorrowerEntry = tk.Entry(bookInputFrame1)
bookBorrowerEntryLabel = tk.Label(bookInputFrame1, text="Card No.")
bookBorrowerEntryLabel.grid(row=3, column=2, sticky="sw")
bookBorrowerEntry.grid(row=4, column=2, columnspan=2)

Q1SubmitButton = tk.Button(bookInputFrame1, text = 'Submit',
                           command = 1+1).grid(row=5, column=0,columnspan=4, pady=10)
# ----------------------------------

# -- Query 2 --
# borrower input frame that holds all borrower entries --------------
borrowerInputFrame = tk.Frame(tab2, background="white")
borrowerInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q2DescriptionLabel = tk.Label(borrowerInputFrame,
                              text="Create Library Account").grid(row=0, column=0, columnspan=2, pady=10)

borrwerNameEntry = tk.Entry(borrowerInputFrame)
borrwerNameEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Name")
borrwerNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
borrwerNameEntry.grid(row=2, column=0, columnspan=2)

borrowerAddressEntry = tk.Entry(borrowerInputFrame)
borrowerAddressEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Address")
borrowerAddressEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
borrowerAddressEntry.grid(row=4, column=0, columnspan=2)

borrowerPhoneNumberEntry = tk.Entry(borrowerInputFrame)
borrowerPhoneNumberLabel = tk.Label(borrowerInputFrame, text="Borrower Phone No.")
borrowerPhoneNumberLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
borrowerPhoneNumberEntry.grid(row=6, column=0, columnspan=2)

Q2SubmitButton = tk.Button(borrowerInputFrame, text = 'Submit',
                           command = 1+1).grid(row=7, column=0,columnspan=2, pady=10)
#------------------------------

#-- Query 3 --
bookInputFrame2 = tk.Frame(tab3, background="white")
bookInputFrame2.grid(row=0, column=0, padx=20, pady=20)

Q3DescriptionLabel = tk.Label(bookInputFrame2,
                              text="Add Book to System").grid(row=0, column=0, columnspan=2, pady=10)

bookNameEntry = tk.Entry(bookInputFrame2)
bookNameEntryLabel = tk.Label(bookInputFrame2, text="Book Title")
bookNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky='sw')
bookNameEntry.grid(row=2, column=0, columnspan=2)

# bookIDEntry = tk.Entry(bookInputFrame2)
# bookIDEntryLabel = tk.Label(bookInputFrame2, text="Book ID")
# bookIDEntryLabel.grid(row=1, column=2, columnspan=2, sticky="sw")
# bookIDEntry.grid(row=2, column=2, columnspan=2)

bookPublisherEntry = tk.Entry(bookInputFrame2)
bookPublisherEntryLabel = tk.Label(bookInputFrame2, text="Book Publisher")
bookPublisherEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
bookPublisherEntry.grid(row=4, column=0, columnspan=2)

bookAuthorEntry = tk.Entry(bookInputFrame2)
bookAuthorEntryLabel = tk.Label(bookInputFrame2, text="Book Author")
bookAuthorEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
bookAuthorEntry.grid(row=6, column=0, columnspan=2)

Q3SubmitButton = tk.Button(bookInputFrame2, text = 'Submit',
                           command = 1+1).grid(row=7, column=0,columnspan=2, pady=10)

# -- Query 4 --
bookCopiesPerBranchInputFrame = tk.Frame(tab4, background="white")
bookCopiesPerBranchInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q4DescriptionLabel = tk.Label(bookCopiesPerBranchInputFrame,
                              text="Search for a Book").grid(row=0, column=0, columnspan=2, pady=10)

bookTitleEntry = tk.Entry(bookCopiesPerBranchInputFrame)
bookTitleEntryLabel = tk.Label(bookCopiesPerBranchInputFrame, text="Book Title")
bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
bookTitleEntry.grid(row=2, column=0, columnspan=2)

Q4SubmitButton = tk.Button(bookCopiesPerBranchInputFrame, text = 'Submit',
                           command = 1+1).grid(row=7, column=0,columnspan=2, pady=10)

# -- Query 5 --
dueDatesInputFrame = tk.Frame(tab5, background="white")
dueDatesInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q5DescriptionLabel = tk.Label(dueDatesInputFrame,
                              text="Search for Late Returns").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(dueDatesInputFrame, text= "Choose a Start Date").grid(row=1, column=0, columnspan=2, sticky="sw")
cal1 = DateEntry(dueDatesInputFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
cal1.grid(row=2, column=0, columnspan=2, sticky="sw")

tk.Label(dueDatesInputFrame, text= "Choose an End Date").grid(row=3, column=0, columnspan=2, sticky="sw")
cal2 = DateEntry(dueDatesInputFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
cal2.grid(row=4, column=0, columnspan=2, sticky="sw")

Q5SubmitButton = tk.Button(dueDatesInputFrame, text = 'Submit',
                           command = 1+1).grid(row=5, column=0,columnspan=2, pady=10)

# main_frame = tk.Frame(LMS_GUI_WINDOW)
# main_frame.pack(fill=tk.BOTH, expand=1)

# my_canvas = tk.Canvas(main_frame)
# my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# my_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
# my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # configure the canvas
# my_canvas.configure(yscrollcommand=my_scrollbar.set)
# my_canvas.bind(
#     '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
# )

# # input frame that holds all input entries
# inputFrame = tk.Frame(my_canvas, background=_navyblue)
# outputFrame = tk.Frame(my_canvas, background=_blue)

# # publisher input frame that holds all publisher entries -------------
# publisherInputFrame = tk.Frame(inputFrame, background="white", padx=20, pady=20)
# publisherInputFrame.grid(row=0, column=0, padx=20, pady=20)

# publisherFrameLabel = tk.Label(publisherInputFrame, text="PUBLISHER", font=('courier sans mono', 16, 'bold'))
# publisherFrameLabel.grid(row=0, column=0, columnspan=4, sticky="nw")

# publisherNameEntry = tk.Entry(publisherInputFrame)
# publisherNameEntryLabel = tk.Label(publisherInputFrame, text="Publisher Name")
# publisherNameEntryLabel.grid(row=1, column=0, sticky='sw')
# publisherNameEntry.grid(row=2, column=0, columnspan=2)

# publisherPhoneNumberEntry = tk.Entry(publisherInputFrame)
# publisherPhoneNumberEntryLabel = tk.Label(publisherInputFrame, text="Publisher Phone Number")
# publisherPhoneNumberEntryLabel.grid(row=1, column=2, sticky="sw")
# publisherPhoneNumberEntry.grid(row=2, column=2, columnspan=2)

# publisherAddressEntry = tk.Entry(publisherInputFrame)
# publisherAddressEntryLabel = tk.Label(publisherInputFrame, text="Publisher Address")
# publisherAddressEntryLabel.grid(row=3, column=0, sticky="sw")
# publisherAddressEntry.grid(row=4, column=0)
# #----------------------------------

# # library branch input frame that holds all borrower entries --------
# libraryBranchInputFrame = tk.Frame(inputFrame, background="white", padx=20, pady=20)
# libraryBranchInputFrame.grid(row=1, column=0, padx=20, pady=20)

# libraryBranchIDEntry = tk.Entry(libraryBranchInputFrame)
# libraryBranchIDEntryLabel = tk.Label(libraryBranchInputFrame, text="Branch ID")
# libraryBranchIDEntryLabel.grid(row=0, column=0, sticky="sw")
# libraryBranchIDEntry.grid(row=1, column=0, columnspan=2)

# libraryBranchNameEntry = tk.Entry(libraryBranchInputFrame)
# libraryBranchNameEntryLabel = tk.Label(libraryBranchInputFrame, text="Branch Name")
# libraryBranchNameEntryLabel.grid(row=0, column=2, sticky="sw")
# libraryBranchNameEntry.grid(row=1, column=2, columnspan=2)

# libraryBranchAddressEntry = tk.Entry(libraryBranchInputFrame)
# libraryBranchAddressEntryLabel = tk.Label(libraryBranchInputFrame, text="Branch Address")
# libraryBranchAddressEntryLabel.grid(row=2, column=0, sticky="sw")
# libraryBranchAddressEntry.grid(row=3, column=0, columnspan=2)
# #-----------------------------------

# # book loans input frame that holds all book entries
# bookLoansInputFrame = tk.Frame(inputFrame, background=_white)
# bookLoansInputFrame.grid(row=4, column=0)

# bookLoans_BookIDEntry = tk.Entry(bookLoansInputFrame)
# bookLoans_BookIDEntryLabel = tk.Label(bookLoansInputFrame, text="Book ID")
# bookLoans_BookIDEntryLabel.grid(row=1, column=0)
# bookLoans_BookIDEntry.grid(row=2, column=0, columnspan=2)

# bookLoans_BranchIDEntry = tk.Entry(bookLoansInputFrame)
# bookLoans_BranchIDEntryLabel = tk.Label(bookLoansInputFrame, text="Branch ID")
# bookLoans_BranchIDEntryLabel.grid(row=1, column=2)
# bookLoans_BranchIDEntry.grid(row=2, column=2, columnspan=2)

# bookLoans_CardNumEntry = tk.Entry(bookLoansInputFrame)
# bookLoans_CardNumEntryLabel = tk.Label(bookLoansInputFrame, text="Card No.")
# bookLoans_CardNumEntryLabel.grid(row=3, column=0)
# bookLoans_CardNumEntry.grid(row=4, column=0, columnspan=2)

# bookLoans_DateOutEntry = tk.Entry(bookLoansInputFrame)
# bookLoans_DateOutEntryLabel = tk.Label(bookLoansInputFrame, text="Date Out (YYYY/MM/DD)")
# bookLoans_DateOutEntryLabel.grid(row=3, column=2)
# bookLoans_DateOutEntry.grid(row=4, column=2, columnspan=2)

# bookLoans_DateReturnedEntry = tk.Entry(bookLoansInputFrame)


# publisherInputFrame = tk.Frame(outputFrame, background="white", padx=20, pady=20)
# publisherInputFrame.grid(row=0, column=0, padx=20, pady=20)

# publisherFrameLabel = tk.Label(publisherInputFrame, text="PUBLISHER", font=('courier sans mono', 16, 'bold'))
# publisherFrameLabel.grid(row=0, column=0, columnspan=4, sticky="nw")

# publisherNameEntry = tk.Entry(publisherInputFrame)
# publisherNameEntryLabel = tk.Label(publisherInputFrame, text="Publisher Name")
# publisherNameEntryLabel.grid(row=1, column=0, sticky='sw')
# publisherNameEntry.grid(row=2, column=0, columnspan=2)

# publisherPhoneNumberEntry = tk.Entry(publisherInputFrame)
# publisherPhoneNumberEntryLabel = tk.Label(publisherInputFrame, text="Publisher Phone Number")
# publisherPhoneNumberEntryLabel.grid(row=1, column=2, sticky="sw")
# publisherPhoneNumberEntry.grid(row=2, column=2, columnspan=2)

# publisherAddressEntry = tk.Entry(publisherInputFrame)
# publisherAddressEntryLabel = tk.Label(publisherInputFrame, text="Publisher Address")
# publisherAddressEntryLabel.grid(row=3, column=0, sticky="sw")
# publisherAddressEntry.grid(row=4, column=0)

# # place the whole entirety of the input frame onto the root window
# inputFrame.grid(row=0, column=0, sticky="nesw", columnspan=2)

# my_canvas.create_window((0, 0), window=inputFrame, anchor="ne")
# my_canvas.create_window((0, 0), window=outputFrame, anchor="nw")

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()

# closes the connection to the database
connection.close()