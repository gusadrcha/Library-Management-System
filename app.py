import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta
import sqlite3

_white = "#ffffff"
_black = "#00171f"
_navyblue = "#003459"
_blue = "#007ea7"
_skyblue = "#00a8e8"

# creates a window
LMS_GUI_WINDOW = tk.Tk()

LMS_GUI_WINDOW.config(bg=_black)

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
def Q1Submit():
    Q1Connection = sqlite3.connect("LMS.db")
    Q1Cursor = Q1Connection.cursor()

    Q1Cursor.execute("SELECT * FROM Book WHERE Book_id = ?",(bookIDEntry.get(),))
    tempBook = Q1Cursor.fetchall()
    if(tempBook):
        Q1Cursor.execute("SELECT * FROM Library_branch WHERE Branch_id = ?",(libraryBranchIDEntry.get(),))
        tempBranch = Q1Cursor.fetchall()
        if(tempBranch):
            Q1Cursor.execute("SELECT * FROM Borrower WHERE Card_no = ?",(bookBorrowerEntry.get(),))
            tempBorrower = Q1Cursor.fetchall()
            if(tempBorrower):
                Q1Cursor.execute("SELECT No_of_copies FROM Book_copies WHERE Book_id = ? AND Branch_id = ?",
                                 (tempBook[0][0],tempBranch[0][0],))
                tempCopyNum = Q1Cursor.fetchall()
                if(tempCopyNum):
                    if(int(tempCopyNum[0][0]) > 0):
                        Q1Cursor.execute("INSERT INTO Book_Loans VALUES (?,?,?,?,?,?)",
                                        (bookIDEntry.get(),libraryBranchIDEntry.get(),bookBorrowerEntry.get(),date.today(),date.today()+timedelta(days=30),None,))
                        Q1Cursor.execute("UPDATE Book_copies SET No_of_copies = No_of_copies-1 WHERE Book_id = ? AND Branch_id = ?",
                                        (tempBook[0][0],tempBranch[0][0],))
                        Q1Cursor.execute("SELECT No_of_copies FROM Book_copies WHERE Book_id = ? AND Branch_id = ?",
                                        (tempBook[0][0],tempBranch[0][0],))
                        Q1results = Q1Cursor.fetchall()
                        Q1resultsLabel = tk.Label(bookInputFrame1, text=str(Q1results[0][0])+" copies left", background="white").grid(row=1, column=2, columnspan=2)
                    else:
                        Q1error5 = tk.Label(bookInputFrame1, text="0 Copies at Specified Branch").grid(row=1, column=2, columnspan=2)
                else:
                    Q1error4 = tk.Label(bookInputFrame1, text="Specified Branch does not have Requested Book").grid(row=1, column=2, columnspan=2)
            else:
                Q1error3 = tk.Label(bookInputFrame1, text="Invalid Card No.").grid(row=1, column=2, columnspan=2)
        else:
            Q1error2 = tk.Label(bookInputFrame1, text="Invalid Branch ID").grid(row=1, column=2, columnspan=2)
    else:
        Q1error1 = tk.Label(bookInputFrame1, text="Invalid Book ID").grid(row=1, column=2, columnspan=2)


    Q1Connection.commit()
    Q1Connection.close()

bookInputFrame1 = tk.Frame(tab1, background="white")
bookInputFrame1.grid(row=0, column=0, padx=20, pady=20)

# T = Text(root, bg, fg, bd, height, width, font, ..)
Q1DescriptionLabel = tk.Label(bookInputFrame1,
                              text="Check Out a Book").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q1OutputLabel = tk.Label(bookInputFrame1,
                              text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

# bookNameEntry = tk.Entry(bookInputFrame1)
# bookNameEntryLabel = tk.Label(bookInputFrame1, text="Book Title")
# bookNameEntryLabel.grid(row=1, column=0, sticky='sw')
# bookNameEntry.grid(row=2, column=0, columnspan=2)

bookIDEntry = tk.Entry(bookInputFrame1)
bookIDEntryLabel = tk.Label(bookInputFrame1, text="Book ID")
bookIDEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
bookIDEntry.grid(row=2, column=0, columnspan=2)

libraryBranchIDEntry = tk.Entry(bookInputFrame1)
libraryBranchIDEntryLabel = tk.Label(bookInputFrame1, text="Branch ID")
libraryBranchIDEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
libraryBranchIDEntry.grid(row=4, column=0, columnspan=2)

bookBorrowerEntry = tk.Entry(bookInputFrame1)
bookBorrowerEntryLabel = tk.Label(bookInputFrame1, text="Card No.")
bookBorrowerEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
bookBorrowerEntry.grid(row=6, column=0, columnspan=2)

Q1SubmitButton = tk.Button(bookInputFrame1, text = 'Submit',
                           command = Q1Submit).grid(row=7, column=0,columnspan=2, pady=10)
# ----------------------------------

# -- Query 2 --
# borrower input frame that holds all borrower entries --------------
def Q2Submit():
    Q2Connection = sqlite3.connect("LMS.db")
    Q2Cursor = Q2Connection.cursor()

    print()

    if(len(str(borrowerPhoneNumberEntry.get())) != 10):
        Q2error1 = tk.Label(borrowerInputFrame, text="Invalid Phone Number").grid(row=1, column=2, columnspan=2)
    else:
        Q2Cursor.execute("INSERT INTO Borrower VALUES (?,?,?,?)",
                        (None,borrowerNameEntry.get(),borrowerAddressEntry.get(),borrowerPhoneNumberEntry.get(),))
        Q2Cursor.execute("SELECT Card_no FROM Borrower WHERE name = ? AND address = ? AND phone_number = ?",
                        (borrowerNameEntry.get(),borrowerAddressEntry.get(),borrowerPhoneNumberEntry.get(),))
        
        Q2results = Q2Cursor.fetchall()
        Q2resultsLabel = tk.Label(borrowerInputFrame, text="New Card: "+str(Q2results[0][0])).grid(row=1, column=2, columnspan=2)

    Q2Connection.commit()
    Q2Connection.close()

borrowerInputFrame = tk.Frame(tab2, background="white")
borrowerInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q2DescriptionLabel = tk.Label(borrowerInputFrame,
                              text="Create Library Account").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q2OutputLabel = tk.Label(borrowerInputFrame,
                              text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

borrowerNameEntry = tk.Entry(borrowerInputFrame)
borrowerNameEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Name")
borrowerNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
borrowerNameEntry.grid(row=2, column=0, columnspan=2)

borrowerAddressEntry = tk.Entry(borrowerInputFrame)
borrowerAddressEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Address")
borrowerAddressEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
borrowerAddressEntry.grid(row=4, column=0, columnspan=2)

borrowerPhoneNumberEntry = tk.Entry(borrowerInputFrame)
borrowerPhoneNumberLabel = tk.Label(borrowerInputFrame, text="Borrower Phone No.")
borrowerPhoneNumberLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
borrowerPhoneNumberEntry.grid(row=6, column=0, columnspan=2)

Q2SubmitButton = tk.Button(borrowerInputFrame, text = 'Submit',
                           command = Q2Submit).grid(row=7, column=0,columnspan=2, pady=10)
#------------------------------

#-- Query 3 --
def Q3Submit():
    Q3Connection = sqlite3.connect("LMS.db")
    Q3Cursor = Q3Connection.cursor()

    Q3Cursor.execute("")

    Q3Connection.commit()
    Q3Connection.close()

bookInputFrame2 = tk.Frame(tab3, background="white")
bookInputFrame2.grid(row=0, column=0, padx=20, pady=20)

Q3DescriptionLabel = tk.Label(bookInputFrame2,
                              text="Add Book to System").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q3OutputLabel = tk.Label(bookInputFrame2,
                              text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

Q3bookTitleEntry = tk.Entry(bookInputFrame2)
Q3bookTitleEntryLabel = tk.Label(bookInputFrame2, text="Book Title")
Q3bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky='sw')
Q3bookTitleEntry.grid(row=2, column=0, columnspan=2)

# Q3bookIDEntry = tk.Entry(bookInputFrame2)
# Q3bookIDEntryLabel = tk.Label(bookInputFrame2, text="Book ID")
# Q3bookIDEntryLabel.grid(row=1, column=2, columnspan=2, sticky="sw")
# Q3bookIDEntry.grid(row=2, column=2, columnspan=2)

bookPublisherEntry = tk.Entry(bookInputFrame2)
bookPublisherEntryLabel = tk.Label(bookInputFrame2, text="Book Publisher")
bookPublisherEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
bookPublisherEntry.grid(row=4, column=0, columnspan=2)

bookAuthorEntry = tk.Entry(bookInputFrame2)
bookAuthorEntryLabel = tk.Label(bookInputFrame2, text="Book Author")
bookAuthorEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
bookAuthorEntry.grid(row=6, column=0, columnspan=2)

Q3SubmitButton = tk.Button(bookInputFrame2, text = 'Submit',
                           command = Q3Submit).grid(row=7, column=0,columnspan=2, pady=10)

# -- Query 4 --
def Q4Submit():
    Q4Connection = sqlite3.connect("LMS.db")
    Q4Cursor = Q4Connection.cursor()

    Q4Cursor.execute("SELECT Book_id FROM Book WHERE Title = ?",(Q4bookTitleEntry.get(),))
    tempBookID = Q4Cursor.fetchall()
    if(tempBookID):
        Q4Cursor.execute("SELECT Branch_id, No_of_copies FROM Book_copies WHERE Book_id = ? GROUP BY Branch_id",(str(tempBookID[0][0])),)
        Q4results = Q4Cursor.fetchall()
        if(Q4results):
            Q4PrintResults = "Branch# : Amount\n"
            for result in Q4results:
                Q4PrintResults += str(result[0])+" : "+str(result[1])+"\n"
            Q4resultsLabel = tk.Label(bookCopiesPerBranchInputFrame, text=Q4PrintResults).grid(row=1, column=2, columnspan=2)
        else:
            Q4error2 = tk.Label(bookCopiesPerBranchInputFrame, text="Book No Longer Held").grid(row=1, column=2, columnspan=2)
    else:
        Q4error1 = tk.Label(bookCopiesPerBranchInputFrame, text="Invalid Book Title").grid(row=1, column=2, columnspan=2)

    Q4Connection.commit()
    Q4Connection.close()

bookCopiesPerBranchInputFrame = tk.Frame(tab4, background="white")
bookCopiesPerBranchInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q4DescriptionLabel = tk.Label(bookCopiesPerBranchInputFrame,
                              text="Search for a Book").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q4OutputLabel = tk.Label(bookCopiesPerBranchInputFrame,
                              text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

Q4bookTitleEntry = tk.Entry(bookCopiesPerBranchInputFrame)
Q4bookTitleEntryLabel = tk.Label(bookCopiesPerBranchInputFrame, text="Book Title")
Q4bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
Q4bookTitleEntry.grid(row=2, column=0, columnspan=2)

Q4SubmitButton = tk.Button(bookCopiesPerBranchInputFrame, text = 'Submit',
                           command = Q4Submit).grid(row=7, column=0,columnspan=2, pady=10)

# -- Query 5 --
def Q5Submit():
    Q5Connection = sqlite3.connect("LMS.db")
    Q5Cursor = Q5Connection.cursor()

    Q5Cursor.execute("")

    Q5Connection.commit()
    Q5Connection.close()

dueDatesInputFrame = tk.Frame(tab5, background="white")
dueDatesInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q5DescriptionLabel = tk.Label(dueDatesInputFrame,
                              text="Search for Late Returns").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q5OutputLabel = tk.Label(dueDatesInputFrame,
                              text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

tk.Label(dueDatesInputFrame, text= "Choose a Start Date").grid(row=1, column=0, columnspan=2, sticky="sw")
cal1 = DateEntry(dueDatesInputFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
cal1.grid(row=2, column=0, columnspan=2, sticky="sw")

tk.Label(dueDatesInputFrame, text= "Choose an End Date").grid(row=3, column=0, columnspan=2, sticky="sw")
cal2 = DateEntry(dueDatesInputFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
cal2.grid(row=4, column=0, columnspan=2, sticky="sw")

Q5SubmitButton = tk.Button(dueDatesInputFrame, text = 'Submit',
                           command = Q5Submit).grid(row=5, column=0,columnspan=2, pady=10)

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