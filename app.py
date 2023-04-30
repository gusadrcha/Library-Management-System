import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta, datetime
import sqlite3

_white = "#ffffff"
# _white = "#00171f"
_uta_orange = "#003459"
_blue = "#007ea7"
_uta_blue = "#00a8e8"
_uta_orange = "#F58025"
_uta_blue = "#0064B1"

# creates a window
LMS_GUI_WINDOW = tk.Tk()

LMS_GUI_WINDOW.config(bg=_white)

# default size of window when first created
height = LMS_GUI_WINDOW.winfo_screenheight()
width = LMS_GUI_WINDOW.winfo_screenwidth()

print(height, width)

LMS_GUI_WINDOW.geometry(f'{int(height)}x{int(width)}')

# change the icon of the application
LMS_GUI_WINDOW.iconbitmap("book-icon-file-13.jpg")

# set the title of the GUI
LMS_GUI_WINDOW.title("Library Management System")

defaultFont = Font(family='Times', size=16)
frameTitle = Font(family="Times", size=20, underline=1)

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
                        resultLabel = tk.Label(queryOneOutputFrame, text=str(Q1results[0][0])+" copies left", font=defaultFont, bg=_uta_blue, fg=_white)
                        resultLabel.pack(side="top")
                    else:
                        errorLabel = tk.Label(queryOneOutputFrame, text="0 Copies at Specified Branch", font=defaultFont, bg=_uta_blue, fg=_white)
                        errorLabel.pack(fill="both")
                else:
                    errorLabel = tk.Label(queryOneOutputFrame, text="Specified Branch does not have Requested Book", font=defaultFont, bg=_uta_blue, fg=_white)
                    errorLabel.pack(fill="both")
            else:
                errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Card No.", font=defaultFont, bg=_uta_blue, fg=_white)
                errorLabel.pack(fill="both")
        else:
            errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Branch ID", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(fill="both")
    else:
        errorLabel = tk.Label(queryOneOutputFrame, text="Invalid Book ID", font=defaultFont, bg=_uta_blue, fg=_white)
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

    tree1.configure(height=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)
    
    tree1.tag_configure("odd", background='#E8E8E8')
    tree1.tag_configure("even", background='#DFDFDF')

    print(len(tree1.get_children()))

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM book_loans")

    rows = r1cursor.fetchall()

    x = 0
    for row in rows:
        print(row)
        if x % 2 == 0:
            tree1.insert("", tk.END, values=row, tags=("even"))
        else:
            tree1.insert("", tk.END, values=row, tags=("odd"))
        x += 1

    tree1.column("1", anchor=tk.CENTER)
    tree1.column("2", anchor=tk.CENTER)
    tree1.column("3", anchor=tk.CENTER)
    tree1.column("4", anchor=tk.CENTER)
    tree1.column("5", anchor=tk.CENTER)
    tree1.column("6", anchor=tk.CENTER)
    
    tree1.pack(side=tk.TOP, padx=10, pady=10)

    r1Connect.commit()
    r1Connect.close()

bookInputFrame1 = tk.Frame(tab1, background=_uta_orange)
bookInputFrame1.pack(side=tk.LEFT, fill="both", expand=False)

queryOneOutputFrame = tk.Frame(tab1, background=_uta_blue)
queryOneOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q1DescriptionLabel = tk.Label(bookInputFrame1, text="Check Out a Book", font=defaultFont, background=_uta_orange, fg=_white)
Q1DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q1OutputLabel = tk.Label(queryOneOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q1OutputLabel.pack(side="top", pady=10)

bookIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
bookIDEntryLabel = tk.Label(bookInputFrame1, text="Book ID", font=defaultFont, background=_uta_orange, fg=_white)
bookIDEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
bookIDEntry.grid(row=2, column=0, columnspan=2, padx=10)

libraryBranchIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
libraryBranchIDEntryLabel = tk.Label(bookInputFrame1, text="Branch ID", font=defaultFont, background=_uta_orange, fg=_white)
libraryBranchIDEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
libraryBranchIDEntry.grid(row=4, column=0, columnspan=2, padx=10)

bookBorrowerEntry = tk.Entry(bookInputFrame1, font=defaultFont)
bookBorrowerEntryLabel = tk.Label(bookInputFrame1, text="Card No.", font=defaultFont, background=_uta_orange, fg=_white)
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

    validNumberSet = set("0123456789")
    inputSet = set(str(borrowerPhoneNumberEntry.get()))

    Q2Connection = sqlite3.connect("LMS.db")
    Q2Cursor = Q2Connection.cursor()

    if not str(borrowerNameEntry.get()):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter a Name", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")
    
    elif((len(str(borrowerPhoneNumberEntry.get())) != 10) or (not inputSet.issubset(validNumberSet))):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Invalid Phone Number", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

    elif not str(borrowerAddressEntry.get()):
        errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter an Address", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

    else:
        tempOldPhoneString = str(borrowerPhoneNumberEntry.get())
        tempPhoneString = tempOldPhoneString[:3]+"-"+tempOldPhoneString[3:6]+"-"+tempOldPhoneString[6:]
        Q2Cursor.execute("INSERT INTO Borrower VALUES (?,?,?,?)",
                        (None,borrowerNameEntry.get(),borrowerAddressEntry.get(),tempPhoneString,))
        Q2Cursor.execute("SELECT Card_no FROM Borrower WHERE name = ? AND address = ? AND phone_number = ?",
                        (borrowerNameEntry.get(),borrowerAddressEntry.get(),tempPhoneString,))

        Q2results = Q2Cursor.fetchall()
        resultLabel = tk.Label(queryTwoOutputFrame, text="New Card: "+str(Q2results[0][0]), font=defaultFont, bg=_uta_blue, fg=_white)
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

    tree2.tag_configure("odd", background='#E8E8E8')
    tree2.tag_configure("even", background='#DFDFDF')

    tree2.heading("1", text= "Card_no")
    tree2.heading("2", text="Name")
    tree2.heading("3", text="Address")
    tree2.heading("4", text="Phone")

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM borrower")

    rows = r1cursor.fetchall()

    x = 0
    for row in rows:
        print(row)
        if x % 2 ==0:
            tree2.insert("", tk.END, values=row, tags=("even"))
        else:
            tree2.insert("", tk.END, values=row, tags=("odd"))
        x += 1

    tree2.column("1", anchor=tk.CENTER)
    tree2.column("2", anchor=tk.CENTER)
    tree2.column("3", anchor=tk.CENTER)
    tree2.column("4", anchor=tk.CENTER)

    tree2.pack(padx=10, pady=10)

    r1Connect.commit()
    r1Connect.close()

borrowerInputFrame = tk.Frame(tab2, background=_uta_orange)
borrowerInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryTwoOutputFrame = tk.Frame(tab2, background=_uta_blue)
queryTwoOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q2DescriptionLabel = tk.Label(borrowerInputFrame, text="Create Library Account", font=defaultFont, bg=_uta_orange, fg=_white)
Q2DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q2OutputLabel = tk.Label(queryTwoOutputFrame, text="Output", font=defaultFont, bg=_uta_blue, fg=_white)
Q2OutputLabel.pack(side="top", pady=10)

borrowerNameEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerNameEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Name", font=defaultFont, bg=_uta_orange, fg=_white)
borrowerNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
borrowerNameEntry.grid(row=2, column=0, columnspan=2, padx=10)

borrowerAddressEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerAddressEntryLabel = tk.Label(borrowerInputFrame, text="Borrower Address", font=defaultFont, bg=_uta_orange, fg=_white)
borrowerAddressEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
borrowerAddressEntry.grid(row=4, column=0, columnspan=2, padx=10)

borrowerPhoneNumberEntry = tk.Entry(borrowerInputFrame, font=defaultFont)
borrowerPhoneNumberLabel = tk.Label(borrowerInputFrame, text="Borrower Phone No.", font=defaultFont, bg=_uta_orange, fg=_white)
borrowerPhoneNumberLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
borrowerPhoneNumberEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q2SubmitButton = tk.Button(borrowerInputFrame, text = 'Submit', font=defaultFont, command = Q2Submit)
Q2SubmitButton.grid(row=7, column=0, pady=10)

Q2ViewButton = tk.Button(borrowerInputFrame, text = 'View', font=defaultFont, command = displayQ2Results)
Q2ViewButton.grid(row=7, column=1, pady=10)
#------------------------------

#-- Query 3 --
def Q3Submit():
    global errorLabel
    global tree3
    global resultLabel

    if tree3.winfo_exists:
        tree3.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()

    if resultLabel.winfo_exists:
        resultLabel.pack_forget()

    Q3Connection = sqlite3.connect("LMS.db")
    Q3Cursor = Q3Connection.cursor()

    if(Q3bookTitleEntry.get() and bookPublisherEntry.get() and bookAuthorEntry.get()):
        Q3Cursor.execute("SELECT B.Book_id FROM Book B, Book_authors BA WHERE B.Title = ? AND B.Book_publisher = ? AND BA.Author_name = ? AND B.Book_id = BA.Book_id",(Q3bookTitleEntry.get(),bookPublisherEntry.get(),bookAuthorEntry.get(),))
        alreadyExists1 = Q3Cursor.fetchall()
        # Q3Cursor.execute("SELECT Book_id FROM Book_authors WHERE Author_name = ?",(bookAuthorEntry.get(),))
        # alreadyExists2 = Q3Cursor.fetchall()

        if(alreadyExists1 ):
            errorLabel = tk.Label(queryThreeOutputFrame, text="Already in System", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side="top")
        else:
            Q3Cursor.execute("INSERT INTO Book VALUES (?,?,?)",(None,Q3bookTitleEntry.get(),bookPublisherEntry.get(),))
            Q3Cursor.execute("SELECT Book_id FROM Book WHERE Title = ? AND Book_publisher = ?",(Q3bookTitleEntry.get(),bookPublisherEntry.get(),))
            tempBookIDs = Q3Cursor.fetchall()

            Q3Cursor.execute("INSERT INTO Book_authors VALUES (?,?)",(tempBookIDs[-1][0],bookAuthorEntry.get(),))
            Q3Cursor.execute("SELECT Branch_id FROM Library_branch")
            branchList = Q3Cursor.fetchall()
            for branch in branchList:
                Q3Cursor.execute("INSERT INTO Book_copies VALUES (?,?,?)",(tempBookIDs[-1][0],branch[0],5,))
            resultLabel = tk.Label(queryThreeOutputFrame, text="Successfully Added!\nNew Book ID: {}".format(tempBookIDs[-1][0]), font=defaultFont, bg=_uta_blue, fg=_white)
            resultLabel.pack(side="top")
    else:
        errorLabel = tk.Label(queryThreeOutputFrame, text="Fill in all entry boxes", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

    Q3Connection.commit()
    Q3Connection.close()

def displayQ3Results():
    global tree3
    global errorLabel

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    if tree3.winfo_exists:
        for item in tree3.get_children():
            tree3.delete(item)
        tree3.pack_forget()
    
    if errorLabel.winfo_exists:
        errorLabel.pack_forget() 

    tree3.heading("1", text= "Book_id")
    tree3.heading("2", text="Branch_id")
    tree3.heading("3", text="No_copies")

    tree3.tag_configure("odd", background='#E8E8E8')
    tree3.tag_configure("even", background='#DFDFDF')

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM Book_copies")

    rows = r1cursor.fetchall()

    x = 0
    for row in rows:
        if x % 2 == 0:
            tree3.insert("", tk.END, values=row, tags=("even"))
        else:
            tree3.insert("", tk.END, values=row, tags=("odd"))
        x += 1

    tree3.column("1", anchor=tk.CENTER)
    tree3.column("2", anchor=tk.CENTER)
    tree3.column("3", anchor=tk.CENTER)

    tree3.pack(padx=10, pady=10)

    r1Connect.commit()
    r1Connect.close()

bookInputFrame2 = tk.Frame(tab3, background=_uta_orange)
bookInputFrame2.pack(side=tk.LEFT, fill="both", expand=False)

queryThreeOutputFrame = tk.Frame(tab3, background=_uta_blue)
queryThreeOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q3DescriptionLabel = tk.Label(bookInputFrame2,
                              text="Add Book to System", font=defaultFont, bg=_uta_orange, fg=_white)
Q3DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q3OutputLabel = tk.Label(queryThreeOutputFrame,
                              text="Output", font=defaultFont, bg=_uta_blue, fg=_white)
Q3OutputLabel.pack(side="top", pady=10)

Q3bookTitleEntry = tk.Entry(bookInputFrame2, font=defaultFont)
Q3bookTitleEntryLabel = tk.Label(bookInputFrame2, text="Book Title", font=defaultFont, bg=_uta_orange, fg=_white)
Q3bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky='sw')
Q3bookTitleEntry.grid(row=2, column=0, columnspan=2, padx=10)

bookPublisherEntry = tk.Entry(bookInputFrame2, font=defaultFont)
bookPublisherEntryLabel = tk.Label(bookInputFrame2, text="Book Publisher", font=defaultFont, bg=_uta_orange, fg=_white)
bookPublisherEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
bookPublisherEntry.grid(row=4, column=0, columnspan=2, padx=10)

bookAuthorEntry = tk.Entry(bookInputFrame2, font=defaultFont)
bookAuthorEntryLabel = tk.Label(bookInputFrame2, text="Book Author", font=defaultFont, bg=_uta_orange, fg=_white)
bookAuthorEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
bookAuthorEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q3SubmitButton = tk.Button(bookInputFrame2, text = 'Submit', font=defaultFont,
                           command = Q3Submit).grid(row=7, column=0, pady=10)

Q3ViewButton = tk.Button(bookInputFrame2, text = 'View', font=defaultFont, command = displayQ3Results)
Q3ViewButton.grid(row=7, column=1, pady=10)

# -- Query 4 --
def Q4Submit():
    global tree4
    global errorLabel

    if tree4.winfo_exists:
        for item in tree4.get_children():
            tree4.delete(item)
        tree4.pack_forget()
    
    if errorLabel.winfo_exists:
        errorLabel.pack_forget()

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    Q4Connection = sqlite3.connect("LMS.db")
    Q4Cursor = Q4Connection.cursor()

    Q4Cursor.execute("SELECT Book_id FROM Book WHERE Title = ?",(Q4bookTitleEntry.get(),))
    tempBookID = Q4Cursor.fetchall()
    if(tempBookID):
        Q4Cursor.execute("SELECT Branch_id, No_of_copies FROM Book_copies WHERE Book_id = ? GROUP BY Branch_id",(str(tempBookID[0][0])),)
        Q4results = Q4Cursor.fetchall()
        if(Q4results):
            for result in Q4results:
                print(result)
                tree4.insert("", tk.END, values=result)
            tree4.pack(padx=10, pady=10)
            
            tree4.heading("1", text="Branch_#")
            tree4.heading("2", text="Amount")

            print(len(tree4.get_children()))
        else:
            errorLabel = tk.Label(queryFourOutputFrame, text="Book No Longer Held", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side="top")
    else:
        errorLabel = tk.Label(queryFourOutputFrame, text="Invalid Book Title", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

    Q4Connection.commit()
    Q4Connection.close()

bookCopiesPerBranchInputFrame = tk.Frame(tab4, background=_uta_orange)
bookCopiesPerBranchInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryFourOutputFrame = tk.Frame(tab4, background=_uta_blue)
queryFourOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q4DescriptionLabel = tk.Label(bookCopiesPerBranchInputFrame,
                              text="Search for a Book", font=defaultFont, bg=_uta_orange, fg=_white)
Q4DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q4OutputLabel = tk.Label(queryFourOutputFrame,
                              text="Output", font=defaultFont, bg=_uta_blue, fg=_white)
Q4OutputLabel.pack(side="top", pady=10)

Q4bookTitleEntry = tk.Entry(bookCopiesPerBranchInputFrame, font=defaultFont)
Q4bookTitleEntryLabel = tk.Label(bookCopiesPerBranchInputFrame, text="Book Title", font=defaultFont, bg=_uta_orange, fg=_white)
Q4bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
Q4bookTitleEntry.grid(row=2, column=0, columnspan=2, padx=10)

Q4SubmitButton = tk.Button(bookCopiesPerBranchInputFrame, text = 'Submit', font=defaultFont, command = Q4Submit)
Q4SubmitButton.grid(row=3, column=0, columnspan=2, pady=10)

# -- Query 5 --
def Q5Submit():
    global errorLabel
    global tree5
    global resultLabel

    if tree5.winfo_exists:
        for item in tree5.get_children():
            tree5.delete(item)
        tree5.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()

    if resultLabel.winfo_exists:
        resultLabel.pack_forget()

    Q5Connection = sqlite3.connect("LMS.db")
    Q5Cursor = Q5Connection.cursor()

    start_date_str = cal1.get_date()
    start_date = datetime.strftime(start_date_str, '%Y-%m-%d')
    end_date_str = cal2.get_date()
    end_date = datetime.strftime(end_date_str, '%Y-%m-%d')

    Q5Cursor.execute("CREATE VIEW IF NOT EXISTS BookLoanInfo AS SELECT BR.name as BName, BL.Card_no as Card_No, BK.Book_id as Book_id, "
                     "BK.Title as Title, BL.Branch_id, BL.Date_out as Date_Out, BL.Due_date as Due_Date, BL.Returned_date, "
                     "CASE WHEN BL.Returned_date <= BL.Due_date THEN 0 "
                     "ELSE JulianDay(BL.Returned_date) - JulianDay(BL.Due_date) END AS 'DaysLate',"
                     "CASE WHEN BL.Returned_date <= BL.Due_date THEN 0 "
                     "ELSE (JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)) * 10 END AS LateFeeBalance "
                     "FROM Book_Loans BL JOIN Borrower BR ON BL.Card_no = BR.Card_no JOIN Book BK ON BL.Book_id = BK.Book_id;")
    Q5Cursor.execute("SELECT * FROM BookLoanInfo")

    Q5Cursor.execute("SELECT Book_id FROM Book_Loans WHERE Due_date BETWEEN ? AND ?", (start_date, end_date,))
    Q5Range = Q5Cursor.fetchall()

    if Q5Range:
        Q5Cursor.execute("SELECT Book_id, (julianday(Returned_date) - julianday(Due_date)) AS days_late "
                         "FROM Book_loans "
                         "WHERE Returned_date > Due_date AND Due_date BETWEEN ? AND ?",
                         (start_date, end_date,))
        Q5Results = Q5Cursor.fetchall()
        if Q5Results:
            # Q5PrintResults = "BookID : Late\n"
            for result in Q5Results:
                print(result)
                tree5.insert("", tk.END, values=result)
                # Q5PrintResults += str(result[0]) + " : " + str(result[1]) + "\n"
            tree5.pack(padx=10, pady=10)

            tree5.heading("1", text= "Borrower Name")
            tree5.heading("2", text="Borrower ID")
            tree5.heading("3", text="Book ID")
            tree5.heading("4", text="Book Title")
            tree5.heading("5", text="Branch ID")
            tree5.heading("6", text="Date Out")
            tree5.heading("7", text="Due Date")
            tree5.heading("8", text="Returned Date")
            tree5.heading("9", text="Days Late")
            tree5.heading("10", text="Late Fee Balance")

            print(len(tree5.get_children()))
            # resultLabel = tk.Label(queryFiveOutputFrame, text=Q5PrintResults)
            # resultLabel.pack(side="top")
        else:
            errorLabel = tk.Label(queryFiveOutputFrame, text="No late returns found", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side="top")
    else:
        errorLabel = tk.Label(queryFiveOutputFrame, text="Invalid Date Range", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

    Q5Connection.commit()
    Q5Connection.close()

def displayQ5Results():
    global tree5
    global errorLabel

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    if tree5.winfo_exists:
        for item in tree5.get_children():
            tree5.delete(item)
        tree5.pack_forget()
    
    if errorLabel.winfo_exists:
        errorLabel.pack_forget() 

    tree5.heading("1", text= "Book_id")
    tree5.heading("2", text="Days Late")

    print(len(tree5.get_children()))

    r1Connect = sqlite3.connect("LMS.db")
    r1cursor = r1Connect.cursor()

    r1cursor.execute("SELECT * FROM Book_copies")

    rows = r1cursor.fetchall()

    for row in rows:
        print(row)
        tree5.insert("", tk.END, values=row)
    tree5.pack(padx=10, pady=10)

    r1Connect.commit()
    r1Connect.close()

dueDatesInputFrame = tk.Frame(tab5, background=_uta_orange)
dueDatesInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryFiveOutputFrame = tk.Frame(tab5, background=_uta_blue)
queryFiveOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q5DescriptionLabel = tk.Label(dueDatesInputFrame,
                              text="Select Due Date Range", font=defaultFont, bg=_uta_orange, fg=_white)
Q5DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q5OutputLabel = tk.Label(queryFiveOutputFrame,
                          text="Late Returns", font=defaultFont, bg=_uta_blue, fg=_white)
Q5OutputLabel.pack(side="top", pady=10)

tk.Label(dueDatesInputFrame, text="Choose a Start Date", font=defaultFont, bg=_uta_orange, fg=_white).grid(row=1, column=0, columnspan=2, sticky="sw")
cal1 = DateEntry(dueDatesInputFrame, font=defaultFont, width=16, background=_white, foreground="black", bd=2)
cal1.grid(row=2, column=0, columnspan=2, sticky="sw", padx=10)
Q5Start_Date = cal1

tk.Label(dueDatesInputFrame, text="Choose an End Date", font=defaultFont, bg=_uta_orange, fg=_white).grid(row=3, column=0, columnspan=2, sticky="sw")
cal2 = DateEntry(dueDatesInputFrame, font=defaultFont, width=16, background=_white, foreground="black", bd=2)
cal2.grid(row=4, column=0, columnspan=2, sticky="sw", padx=10)
Q5End_Date = cal2



Q5SubmitButton = tk.Button(dueDatesInputFrame, text='Submit', font=defaultFont,
                           command=Q5Submit).grid(row=5, column=0, columnspan=2, pady=10)

# Q5ViewButton = tk.Button(dueDatesInputFrame, text = 'View', font=defaultFont, command = displayQ5Results)
# Q5ViewButton.grid(row=5, column=1, pady=10)

# global variables

errorLabel = tk.Label()
resultLabel = tk.Label()
resultFrame: tk.Frame()

tree1 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2", "3", "4", "5", "6"), show='headings', height=20)
tree2 = ttk.Treeview(queryTwoOutputFrame, columns=("1", "2", "3", "4"), show='headings', height=20)
tree3 = ttk.Treeview(queryThreeOutputFrame, columns=("1", "2", "3"), show='headings', height=20)
tree4 = ttk.Treeview(queryFourOutputFrame, columns=("1", "2"), show='headings', height=10)
tree5 = ttk.Treeview(queryFiveOutputFrame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), show='headings', height=20)

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()