import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta, datetime
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

defaultFont = Font(family='Times',
                   size=16)

# create the main tab window and view
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
    global errorLabel
    global tree1
    global resultLabel

    if tree1.winfo_exists:
        tree1.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()
    
    if resultLabel.winfo_exists:
        resultLabel.pack_forget()

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
                        resultLabel = tk.Label(queryOneOutputFrame, text=str(Q1results[0][0])+" copies left", background="white").pack(side="top")
                    else:
                        errorLabel = tk.Label(queryOneOutputFrame, text="0 Copies at Specified Branch")
                        errorLabel.pack(fill="both")
                else:
                    errorLabel = tk.Label(queryOneOutputFrame, text="Specified Branch does not have Requested Book")
                    errorLabel.pack(fill="both")
            else:
                errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Card No.")
                errorLabel.pack(fill="both")
        else:
            errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Branch ID")
            errorLabel.pack(fill="both")
    else:
        errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Book ID")
        errorLabel.pack(fill="both")


    Q1Connection.commit()
    Q1Connection.close()

def displayQ1Result():
    global tree1
    global errorLabel

    if tree1.winfo_exists:
        for item in tree1.get_children():
            tree1.delete(item)
        tree1.pack_forget()
    
    if errorLabel.winfo_exists:
        errorLabel.pack_forget() 

    tree1.heading("1", text="Book_id")
    tree1.heading("2", text="Branch_id")
    tree1.heading("3", text= "Card_no")
    tree1.heading("4", text="Date_out")
    tree1.heading("5", text="Due_date")
    tree1.heading("6", text="Returned_date")

    print(len(tree1.get_children()))

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM book_loans")

    rows = r1cursor.fetchall()

    for row in rows:
        print(row)
        tree1.insert("", tk.END, values=row)
    tree1.pack()

    r1Connect.commit()
    r1Connect.close()

bookInputFrame1 = tk.Frame(tab1, background=_navyblue)
bookInputFrame1.pack(side=tk.LEFT, fill="both", expand=False)

queryOneOutputFrame = tk.Frame(tab1, background=_skyblue)
queryOneOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

# T = Text(root, bg, fg, bd, height, width, font, ..)
Q1DescriptionLabel = tk.Label(bookInputFrame1, text="Check Out a Book", font=defaultFont, background=_navyblue, fg=_white).grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q1OutputLabel = tk.Label(queryOneOutputFrame, text="Output", font=defaultFont).pack(side=tk.TOP)

bookIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
bookIDEntryLabel = tk.Label(bookInputFrame1, text="Book ID", font=defaultFont, background=_navyblue, fg=_white)
bookIDEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
bookIDEntry.grid(row=2, column=0, columnspan=2, padx=10)

libraryBranchIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
libraryBranchIDEntryLabel = tk.Label(bookInputFrame1, text="Branch ID", font=defaultFont, background=_navyblue, fg=_white)
libraryBranchIDEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
libraryBranchIDEntry.grid(row=4, column=0, columnspan=2, padx=10)

bookBorrowerEntry = tk.Entry(bookInputFrame1, font=defaultFont)
bookBorrowerEntryLabel = tk.Label(bookInputFrame1, text="Card No.", font=defaultFont, background=_navyblue, fg=_white)
bookBorrowerEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
bookBorrowerEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q1SubmitButton = tk.Button(bookInputFrame1, text = 'Submit', font=defaultFont, command = Q1Submit).grid(row=7, column=0, pady=10)

Q1ViewButton = tk.Button(bookInputFrame1, text="View", font=defaultFont, command=displayQ1Result)
Q1ViewButton.grid(row=7, column=1, pady=10)

# ----------------------------------

# -- Query 2 --
# borrower input frame that holds all borrower entries --------------
def Q2Submit():
    global errorLabel
    global tree2
    global resultLabel

    if tree2.winfo_exists:
        tree2.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()
    
    if resultLabel.winfo_exists:
        resultLabel.pack_forget()

    Q2Connection = sqlite3.connect("LMS.db")
    Q2Cursor = Q2Connection.cursor()

    if not str(borrowerNameEntry.get()):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter a Name", font=defaultFont)
        errorLabel.pack(side="top")
    
    elif(len(str(borrowerPhoneNumberEntry.get())) != 10):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Invalid Phone Number", font=defaultFont)
        errorLabel.pack(side="top")

    elif not str(borrowerAddressEntry.get()):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter an Address", font=defaultFont)
        errorLabel.pack(side="top")

    else:
        Q2Cursor.execute("INSERT INTO Borrower VALUES (?,?,?,?)",
                        (None,borrowerNameEntry.get(),borrowerAddressEntry.get(),borrowerPhoneNumberEntry.get(),))
        Q2Cursor.execute("SELECT Card_no FROM Borrower WHERE name = ? AND address = ? AND phone_number = ?",
                        (borrowerNameEntry.get(),borrowerAddressEntry.get(),borrowerPhoneNumberEntry.get(),))

        Q2results = Q2Cursor.fetchall()
        resultLabel = tk.Label(queryTwoOutputFrame, text="New Card: "+str(Q2results[0][0]))
        resultLabel.pack(side="top")

    Q2Connection.commit()
    Q2Connection.close()

def displayQ2Results():
    global tree2
    global errorLabel

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    if tree2.winfo_exists:
        for item in tree2.get_children():
            tree2.delete(item)
        tree2.pack_forget()
    
    if errorLabel.winfo_exists:
        errorLabel.pack_forget() 

    tree2.heading("1", text= "Card_no")
    tree2.heading("2", text="Name")
    tree2.heading("3", text="Address")

    print(len(tree2.get_children()))

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM borrower")

    rows = r1cursor.fetchall()

    for row in rows:
        print(row)
        tree2.insert("", tk.END, values=row)
    tree2.pack()

    r1Connect.commit()
    r1Connect.close()

borrowerInputFrame = tk.Frame(tab2, background=_navyblue)
borrowerInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryTwoOutputFrame = tk.Frame(tab2, background=_skyblue)
queryTwoOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q2DescriptionLabel = tk.Label(borrowerInputFrame, text="Create Library Account", font=defaultFont, bg=_navyblue, fg=_white)
Q2DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q2OutputLabel = tk.Label(queryTwoOutputFrame, text="Output", font=defaultFont)
Q2OutputLabel.pack(side="top")

borrowerNameEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerNameEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Name", font=defaultFont, bg=_navyblue, fg=_white)
borrowerNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
borrowerNameEntry.grid(row=2, column=0, columnspan=2, padx=10)

borrowerAddressEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerAddressEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Address", font=defaultFont, bg=_navyblue, fg=_white)
borrowerAddressEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
borrowerAddressEntry.grid(row=4, column=0, columnspan=2, padx=10)

borrowerPhoneNumberEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerPhoneNumberLabel = tk.Label(borrowerInputFrame, text="Borrower Phone No.", font=defaultFont, bg=_navyblue, fg=_white)
borrowerPhoneNumberLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
borrowerPhoneNumberEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q2SubmitButton = tk.Button(borrowerInputFrame, text = 'Submit', font=defaultFont, command = Q2Submit)
Q2SubmitButton.grid(row=7, column=0, pady=10)

Q2ViewButton = tk.Button(borrowerInputFrame, text = 'View', font=defaultFont, command = displayQ2Results)
Q2ViewButton.grid(row=7, column=1, pady=10)
#------------------------------

#-- Query 3 --
def Q3Submit():
    Q3Connection = sqlite3.connect("LMS.db")
    Q3Cursor = Q3Connection.cursor()

    Q3Cursor.execute("SELECT Book_id FROM Book WHERE Title = ? AND Book_publisher = ?",(Q3bookTitleEntry.get(),bookPublisherEntry.get(),))
    alreadyExists = Q3Cursor.fetchall()
    if(alreadyExists):
        Q3error1 = tk.Label(bookInputFrame2, text="Already in System").grid(row=1, column=2, columnspan=2)
    else:
        Q3Cursor.execute("INSERT INTO Book VALUES (?,?,?)",(None,Q3bookTitleEntry.get(),bookPublisherEntry.get(),))
        Q3Cursor.execute("SELECT Book_id FROM Book WHERE Title = ? AND Book_publisher = ?",(Q3bookTitleEntry.get(),bookPublisherEntry.get(),))
        tempBookID = Q3Cursor.fetchall()
        Q3Cursor.execute("INSERT INTO Book_authors VALUES (?,?)",(tempBookID[0][0],bookAuthorEntry.get(),))
        Q3Cursor.execute("SELECT Branch_id FROM Library_branch")
        branchList = Q3Cursor.fetchall()
        for branch in branchList:
            Q3Cursor.execute("INSERT INTO Book_copies VALUES (?,?,?)",(tempBookID[0][0],branch[0],5,))
        Q3OutputLabel = tk.Label(bookInputFrame2, text="Successfully Added!").grid(row=1, column=2, columnspan=2)

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
    start_date_str = cal1.get_date().strftime('%m/%d/%Y')
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    end_date_str = cal2.get_date().strftime('%m/%d/%Y')
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    Q5Cursor.execute("SELECT Book_id FROM Book_Loans WHERE Date_out BETWEEN ? AND ?", (start_date, end_date,))
    Q5Range = Q5Cursor.fetchall()

    if Q5Range:
        Q5Cursor.execute("SELECT Book_id, (julianday(Returned_date) - julianday(Due_date)) AS days_late "
                         "FROM Book_loans "
                         "WHERE Returned_date > Due_date AND Due_date BETWEEN ? AND ?",
                         (start_date, end_date,))
        Q5Results = Q5Cursor.fetchall()
        if Q5Results:
            Q5PrintResults = "BookID : Late\n"
            for result in Q5Results:
                Q5PrintResults += str(result[0]) + " : " + str(result[1]) + "\n"
            Q5resultsLabel = tk.Label(dueDatesInputFrame, text=Q5PrintResults).grid(row=1, column=2, columnspan=2)
        else:
            Q5error1 = tk.Label(dueDatesInputFrame, text="No late returns found").grid(row=1, column=2, columnspan=2)
    else:
        Q5error2 = tk.Label(dueDatesInputFrame, text="Invalid Date Range").grid(row=1, column=2, columnspan=2)
    Q5Connection.commit()
    Q5Connection.close()


dueDatesInputFrame = tk.Frame(tab5, background="white")
dueDatesInputFrame.grid(row=0, column=0, padx=20, pady=20)

Q5DescriptionLabel = tk.Label(dueDatesInputFrame,
                              text="Search for Late Returns").grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q5OutputLabel = tk.Label(dueDatesInputFrame,
                          text="Output").grid(row=0, column=2, columnspan=2, padx=5, pady=10)

tk.Label(dueDatesInputFrame, text="Choose a Start Date").grid(row=1, column=0, columnspan=2, sticky="sw")
cal1 = DateEntry(dueDatesInputFrame, width=16, background="magenta3", foreground="white", bd=2)
cal1.grid(row=2, column=0, columnspan=2, sticky="sw")
Q5Start_Date = cal1

tk.Label(dueDatesInputFrame, text="Choose an End Date").grid(row=3, column=0, columnspan=2, sticky="sw")
cal2 = DateEntry(dueDatesInputFrame, width=16, background="magenta3", foreground="white", bd=2)
cal2.grid(row=4, column=0, columnspan=2, sticky="sw")
Q5End_Date = cal2

Q5SubmitButton = tk.Button(dueDatesInputFrame, text='Submit',
                           command=Q5Submit).grid(row=5, column=0, columnspan=2, pady=10)

# global variables

errorLabel = tk.Label()
resultLabel = tk.Label()
resultFrame: tk.Frame()

tree1 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2","3", "4", "5", "6"), show='headings')
tree2 = ttk.Treeview(queryTwoOutputFrame, columns=("1", "2","3"), show='headings')
tree3 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2","3", "4", "5", "6"), show='headings')
tree4 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2","3", "4", "5", "6"), show='headings')
tree5 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2","3", "4", "5", "6"), show='headings')

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()