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
tab6_a = ttk.Frame(tabControl)
tab6_b = ttk.Frame(tabControl)

tabControl.add(tab1, text="Query 1")
tabControl.add(tab2, text="Query 2")
tabControl.add(tab3, text="Query 3")
tabControl.add(tab4, text="Query 4")
tabControl.add(tab5, text="Query 5")
tabControl.add(tab6_a, text="Query 6.a")
tabControl.add(tab6_b, text="Query 6.b")

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

    Q1Connection = sqlite3.connect("./LMS.db")
    Q1Cursor = Q1Connection.cursor()

    Q1Cursor.execute("SELECT * FROM Book WHERE Book_id = ?",(Q1bookIDEntry.get(),))
    tempBook = Q1Cursor.fetchall()
    if(tempBook):
        Q1Cursor.execute("SELECT * FROM Library_branch WHERE Branch_id = ?",(Q1libraryBranchIDEntry.get(),))
        tempBranch = Q1Cursor.fetchall()
        if(tempBranch):
            Q1Cursor.execute("SELECT * FROM Borrower WHERE Card_no = ?",(Q1bookBorrowerEntry.get(),))
            tempBorrower = Q1Cursor.fetchall()
            if(tempBorrower):
                Q1Cursor.execute("SELECT No_of_copies FROM Book_copies WHERE Book_id = ? AND Branch_id = ?",
                                 (tempBook[0][0],tempBranch[0][0],))
                tempCopyNum = Q1Cursor.fetchall()
                if(tempCopyNum):
                    if(int(tempCopyNum[0][0]) > 0):
                        Q1Cursor.execute("INSERT INTO Book_Loans VALUES (?,?,?,?,?,?,?)",
                                        (Q1bookIDEntry.get(),Q1libraryBranchIDEntry.get(),Q1bookBorrowerEntry.get(),date.today(),date.today()+timedelta(days=30),None,0,))
                        
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
    tree1.heading("7", text="Late Fee")

    tree1.configure(height=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)
    
    tree1.tag_configure("odd", background='#E8E8E8')
    tree1.tag_configure("even", background='#DFDFDF')

    r1Connect = sqlite3.connect("./LMS.db")
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
    tree1.column("7", anchor=tk.CENTER)

    tree1.pack(side=tk.TOP, padx=10, pady=10)

    r1Connect.commit()
    r1Connect.close()

bookInputFrame1 = tk.Frame(tab1, background=_uta_orange)
bookInputFrame1.pack(side=tk.LEFT, fill="both", expand=False)

queryOneOutputFrame = tk.Frame(tab1, background=_uta_blue)
queryOneOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q1DescriptionLabel = tk.Label(bookInputFrame1, text="Check Out a Book", font=frameTitle, background=_uta_orange, fg=_white)
Q1DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q1OutputLabel = tk.Label(queryOneOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q1OutputLabel.pack(side="top", pady=10)

Q1bookIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
Q1bookIDEntryLabel = tk.Label(bookInputFrame1, text="Book ID", font=defaultFont, background=_uta_orange, fg=_white)
Q1bookIDEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
Q1bookIDEntry.grid(row=2, column=0, columnspan=2, padx=10)

Q1libraryBranchIDEntry = tk.Entry(bookInputFrame1, font=defaultFont)
Q1libraryBranchIDEntryLabel = tk.Label(bookInputFrame1, text="Branch ID", font=defaultFont, background=_uta_orange, fg=_white)
Q1libraryBranchIDEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
Q1libraryBranchIDEntry.grid(row=4, column=0, columnspan=2, padx=10)

Q1bookBorrowerEntry = tk.Entry(bookInputFrame1, font=defaultFont)
Q1bookBorrowerEntryLabel = tk.Label(bookInputFrame1, text="Card No.", font=defaultFont, background=_uta_orange, fg=_white)
Q1bookBorrowerEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
Q1bookBorrowerEntry.grid(row=6, column=0, columnspan=2, padx=10)

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
    inputSet = set(str(Q2borrowerPhoneNumberEntry.get()))

    Q2Connection = sqlite3.connect("./LMS.db")
    Q2Cursor = Q2Connection.cursor()

    if(Q2borrowerNameEntry.get()):   
        if(Q2borrowerAddressEntry.get()):
            if((len(str(Q2borrowerPhoneNumberEntry.get())) == 10) and (inputSet.issubset(validNumberSet))):            
                tempOldPhoneString = str(Q2borrowerPhoneNumberEntry.get())
                tempPhoneString = tempOldPhoneString[:3]+"-"+tempOldPhoneString[3:6]+"-"+tempOldPhoneString[6:]
                Q2Cursor.execute("INSERT INTO Borrower VALUES (?,?,?,?)",
                                 (None,Q2borrowerNameEntry.get(),Q2borrowerAddressEntry.get(),tempPhoneString,))
                Q2Cursor.execute("SELECT Card_no FROM Borrower WHERE name = ? AND address = ? AND phone_number = ?",
                                 (Q2borrowerNameEntry.get(),Q2borrowerAddressEntry.get(),tempPhoneString,))

                Q2results = Q2Cursor.fetchall()
                resultLabel = tk.Label(queryTwoOutputFrame, text="New Card: "+str(Q2results[0][0]), font=defaultFont, bg=_uta_blue, fg=_white)
                resultLabel.pack(side="top")
            else:
                errorLabel = tk.Label(queryTwoOutputFrame, text="Invalid Phone Number", font=defaultFont, bg=_uta_blue, fg=_white)
                errorLabel.pack(side="top")
        else:
            errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter an Address", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side="top")
    else:
        errorLabel = tk.Label(queryTwoOutputFrame, text="Must enter a Name", font=defaultFont, bg=_uta_blue, fg=_white)
        errorLabel.pack(side="top")

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

    r1Connect = sqlite3.connect("./LMS.db")
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

Q2borrowerInputFrame = tk.Frame(tab2, background=_uta_orange)
Q2borrowerInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryTwoOutputFrame = tk.Frame(tab2, background=_uta_blue)
queryTwoOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q2DescriptionLabel = tk.Label(Q2borrowerInputFrame, text="Create Library Account", font=frameTitle, bg=_uta_orange, fg=_white)
Q2DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q2OutputLabel = tk.Label(queryTwoOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q2OutputLabel.pack(side="top", pady=10)

Q2borrowerNameEntry = tk.Entry(Q2borrowerInputFrame, font=defaultFont)
Q2borrowerNameEntryLabel = tk.Label(Q2borrowerInputFrame, text="Borrower Name", font=defaultFont, bg=_uta_orange, fg=_white)
Q2borrowerNameEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
Q2borrowerNameEntry.grid(row=2, column=0, columnspan=2, padx=10)

Q2borrowerAddressEntry = tk.Entry(Q2borrowerInputFrame, font=defaultFont)
Q2borrowerAddressEntryLabel = tk.Label(Q2borrowerInputFrame, text="Borrower Address", font=defaultFont, bg=_uta_orange, fg=_white)
Q2borrowerAddressEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
Q2borrowerAddressEntry.grid(row=4, column=0, columnspan=2, padx=10)

Q2borrowerPhoneNumberEntry = tk.Entry(Q2borrowerInputFrame, font=defaultFont)
Q2borrowerPhoneNumberLabel = tk.Label(Q2borrowerInputFrame, text="Borrower Phone No.", font=defaultFont, bg=_uta_orange, fg=_white)
Q2borrowerPhoneNumberLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
Q2borrowerPhoneNumberEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q2SubmitButton = tk.Button(Q2borrowerInputFrame, text = 'Submit', font=defaultFont, command = Q2Submit)
Q2SubmitButton.grid(row=7, column=0, pady=10)

Q2ViewButton = tk.Button(Q2borrowerInputFrame, text = 'View', font=defaultFont, command = displayQ2Results)
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

    Q3Connection = sqlite3.connect("./LMS.db")
    Q3Cursor = Q3Connection.cursor()

    if(Q3bookTitleEntry.get() and Q3bookPublisherEntry.get() and Q3bookAuthorEntry.get()):
        Q3Cursor.execute("SELECT B.Book_id FROM Book B, Book_authors BA WHERE B.Title = ? AND B.Book_publisher = ? AND BA.Author_name = ? AND B.Book_id = BA.Book_id",(Q3bookTitleEntry.get(),Q3bookPublisherEntry.get(),Q3bookAuthorEntry.get(),))
        alreadyExists1 = Q3Cursor.fetchall()

        if(alreadyExists1 ):
            errorLabel = tk.Label(queryThreeOutputFrame, text="Already in System", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side="top")
        else:
            Q3Cursor.execute("INSERT INTO Book VALUES (?,?,?)",(None,Q3bookTitleEntry.get(),Q3bookPublisherEntry.get(),))
            Q3Cursor.execute("SELECT Book_id FROM Book WHERE Title = ? AND Book_publisher = ?",(Q3bookTitleEntry.get(),Q3bookPublisherEntry.get(),))
            tempBookIDs = Q3Cursor.fetchall()

            Q3Cursor.execute("INSERT INTO Book_authors VALUES (?,?)",(tempBookIDs[-1][0],Q3bookAuthorEntry.get(),))
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

    r1Connect = sqlite3.connect("./LMS.db")
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

Q3bookInputFrame = tk.Frame(tab3, background=_uta_orange)
Q3bookInputFrame.pack(side=tk.LEFT, fill="both", expand=False)

queryThreeOutputFrame = tk.Frame(tab3, background=_uta_blue)
queryThreeOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q3DescriptionLabel = tk.Label(Q3bookInputFrame, text="Add Book to System", font=frameTitle, bg=_uta_orange, fg=_white)
Q3DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q3OutputLabel = tk.Label(queryThreeOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q3OutputLabel.pack(side="top", pady=10)

Q3bookTitleEntry = tk.Entry(Q3bookInputFrame, font=defaultFont)
Q3bookTitleEntryLabel = tk.Label(Q3bookInputFrame, text="Book Title", font=defaultFont, bg=_uta_orange, fg=_white)
Q3bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky='sw')
Q3bookTitleEntry.grid(row=2, column=0, columnspan=2, padx=10)

Q3bookPublisherEntry = tk.Entry(Q3bookInputFrame, font=defaultFont)
Q3bookPublisherEntryLabel = tk.Label(Q3bookInputFrame, text="Book Publisher", font=defaultFont, bg=_uta_orange, fg=_white)
Q3bookPublisherEntryLabel.grid(row=3, column=0, columnspan=2, sticky="sw")
Q3bookPublisherEntry.grid(row=4, column=0, columnspan=2, padx=10)

Q3bookAuthorEntry = tk.Entry(Q3bookInputFrame, font=defaultFont)
Q3bookAuthorEntryLabel = tk.Label(Q3bookInputFrame, text="Book Author", font=defaultFont, bg=_uta_orange, fg=_white)
Q3bookAuthorEntryLabel.grid(row=5, column=0, columnspan=2, sticky="sw")
Q3bookAuthorEntry.grid(row=6, column=0, columnspan=2, padx=10)

Q3SubmitButton = tk.Button(Q3bookInputFrame, text = 'Submit', font=defaultFont,
                           command = Q3Submit).grid(row=7, column=0, pady=10)

Q3ViewButton = tk.Button(Q3bookInputFrame, text = 'View', font=defaultFont, command = displayQ3Results)
Q3ViewButton.grid(row=7, column=1, pady=10)
# ----------------------------------


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

    Q4Connection = sqlite3.connect("./LMS.db")
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

Q4DescriptionLabel = tk.Label(bookCopiesPerBranchInputFrame, text="Search for a Book", font=frameTitle, bg=_uta_orange, fg=_white)
Q4DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q4OutputLabel = tk.Label(queryFourOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q4OutputLabel.pack(side="top", pady=10)

Q4bookTitleEntry = tk.Entry(bookCopiesPerBranchInputFrame, font=defaultFont)
Q4bookTitleEntryLabel = tk.Label(bookCopiesPerBranchInputFrame, text="Book Title", font=defaultFont, bg=_uta_orange, fg=_white)
Q4bookTitleEntryLabel.grid(row=1, column=0, columnspan=2, sticky="sw")
Q4bookTitleEntry.grid(row=2, column=0, columnspan=2, padx=10)

Q4SubmitButton = tk.Button(bookCopiesPerBranchInputFrame, text = 'Submit', font=defaultFont, command = Q4Submit)
Q4SubmitButton.grid(row=3, column=0, columnspan=2, pady=10)
# ----------------------------------

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

    Q5Connection = sqlite3.connect("./LMS.db")
    Q5Cursor = Q5Connection.cursor()

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    start_date_str = cal1.get_date()
    start_date = datetime.strftime(start_date_str, '%Y-%m-%d')
    end_date_str = cal2.get_date()
    end_date = datetime.strftime(end_date_str, '%Y-%m-%d')

    Q5Cursor.execute('''DROP VIEW IF EXISTS vBookLoanInfo''')
    
    Q5Cursor.execute('''
    CREATE VIEW vBookLoanInfo AS
    SELECT BL.Card_no AS Card_No,
           BR.name as 'Borrower Name',
           BL.Date_out as Date_Out,
           BL.Due_date as Due_Date,
           BL.Returned_date,
           (JulianDay(BL.Returned_date) - JulianDay(BL.Date_out)) as TotalDays,
           BK.Title as 'Book Title',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)
           END AS 'Number of days later return',
           BL.Branch_id as 'Branch ID',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE (JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)) * (SELECT LateFee
                                                                            FROM Library_Branch LB
                                                                            WHERE LB.branch_id = BL.Branch_id)
           END AS LateFeeBalance
    FROM Book_Loans BL
    JOIN Borrower BR ON BL.Card_no = BR.Card_no
    JOIN Book BK ON BL.Book_id = BK.Book_id
    JOIN Library_branch LB ON BL.branch_id = LB.Branch_id;
    ''')

    Q5Cursor.execute("SELECT * FROM vBookLoanInfo WHERE Due_Date BETWEEN ? AND ? AND julianday(returned_date) > julianday(Due_Date) ORDER BY LateFeeBalance DESC;", (start_date, end_date,))
    Q5Range = Q5Cursor.fetchall()

    if (start_date_str < end_date_str):
        if Q5Range:
            for record in Q5Range:
                lateFeeAmount = "${:.2f}".format(record[9])

                newTuple = (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], lateFeeAmount)                

                tree5.insert("", tk.END, values=newTuple)

            tree5.pack(padx=10, pady=10)

            tree5.heading("1", text= "Card No.")
            tree5.column("1", width=100, anchor=tk.CENTER)

            tree5.heading("2", text="Borrower Name")
            tree5.column("2", width=100, anchor=tk.CENTER)

            tree5.heading("3", text="Date Out")
            tree5.column("3", width=100, anchor=tk.CENTER)

            tree5.heading("4", text="Due Date")
            tree5.column("4", width=100, anchor=tk.CENTER)

            tree5.heading("5", text="Returned Date")
            tree5.column("5", width=100, anchor=tk.CENTER)

            tree5.heading("6", text="TotalDays")
            tree5.column("6", width=100, anchor=tk.CENTER)

            tree5.heading("7", text="Book Title")
            tree5.column("7", width=200, anchor=tk.CENTER)

            tree5.heading("8", text="Number of days later return")
            tree5.column("8", width=100, anchor=tk.CENTER)

            tree5.heading("9", text="Branch ID")
            tree5.column("9", width=100, anchor=tk.CENTER)

            tree5.heading("10", text="Late Fee Balance")
            tree5.column("10", width=100, anchor=tk.CENTER)

            print(len(tree5.get_children()))
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

    r1Connect = sqlite3.connect("./LMS.db")
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

Q5DescriptionLabel = tk.Label(dueDatesInputFrame, text="Select Due Date Range", font=frameTitle, bg=_uta_orange, fg=_white)
Q5DescriptionLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

# date selector
tk.Label(dueDatesInputFrame, text="Choose a Start Date", font=defaultFont, bg=_uta_orange, fg=_white).grid(row=1, column=0, columnspan=2, sticky="sw")
cal1 = DateEntry(dueDatesInputFrame, font=defaultFont, width=16, background=_white, foreground="black", bd=2)
cal1.grid(row=2, column=0, columnspan=2, sticky="sw", padx=10)
Q5Start_Date = cal1

tk.Label(dueDatesInputFrame, text="Choose an End Date", font=defaultFont, bg=_uta_orange, fg=_white).grid(row=3, column=0, columnspan=2, sticky="sw")
cal2 = DateEntry(dueDatesInputFrame, font=defaultFont, width=16, background=_white, foreground="black", bd=2)
cal2.grid(row=4, column=0, columnspan=2, sticky="sw", padx=10)
Q5End_Date = cal2

queryFiveOutputFrame = tk.Frame(tab5, background=_uta_blue)
queryFiveOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q5OutputLabel = tk.Label(queryFiveOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q5OutputLabel.pack(side="top", pady=10)


Q5SubmitButton = tk.Button(dueDatesInputFrame, text='Submit', font=defaultFont,
                           command=Q5Submit).grid(row=14, column=0, columnspan=2, pady=10)
# ----------------------------------


# -- Query 6.a --
def Q6aSubmit():
    global errorLabel
    global tree6a
    global resultLabel


    if tree6a.winfo_exists:
        for item in tree6a.get_children():
            tree6a.delete(item)
        tree6a.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()

    if resultLabel.winfo_exists:
        resultLabel.pack_forget()
            
    tree6a.heading("1", text="Borrower")
    tree6a.heading("2", text="Card No.")
    tree6a.heading("3", text="Late Fee Balance")

    tree6a.column("1", anchor=tk.CENTER)
    tree6a.column("2", anchor=tk.CENTER)
    tree6a.column("3", anchor=tk.CENTER)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    Q6aConnection = sqlite3.connect("./LMS.db")
    Q6aCursor = Q6aConnection.cursor()

    Q6aCursor.execute('''DROP VIEW IF EXISTS vBookLoanInfo''')
    
    Q6aCursor.execute('''
    CREATE VIEW vBookLoanInfo AS
    SELECT BL.Card_no AS Card_No,
           BR.name as 'Borrower Name',
           BL.Date_out as Date_Out,
           BL.Due_date as Due_Date,
           BL.Returned_date,
           (JulianDay(BL.Returned_date) - JulianDay(BL.Date_out)) as TotalDays,
           BK.Title as 'Book Title',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)
           END AS 'Number of days later return',
           BL.Branch_id as 'Branch ID',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE (JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)) * (SELECT LateFee
                                                                            FROM Library_Branch LB
                                                                            WHERE LB.branch_id = BL.Branch_id)
           END AS LateFeeBalance
    FROM Book_Loans BL
    JOIN Borrower BR ON BL.Card_no = BR.Card_no
    JOIN Book BK ON BL.Book_id = BK.Book_id
    JOIN Library_branch LB ON BL.branch_id = LB.Branch_id;
    ''')

    tempBorrowerName = "%"+str(Q6aborrowerNameEntry.get())+"%"

    if Q6acardNumberEntry.get() and Q6aborrowerNameEntry.get():
        Q6aCursor.execute('''SELECT "borrower name", card_no, SUM(LateFeeBalance) from vBookLoanInfo
                            WHERE card_no = ? AND "borrower name" LIKE ?
                            GROUP BY card_no''', (Q6acardNumberEntry.get(), tempBorrowerName,))
        
        Q6aResults = Q6aCursor.fetchall()

        if(Q6aResults):
            for result in Q6aResults:
                if result[2] == None or result[2] >= 0:

                    lateFeeAmount = "$0.00"

                    if result[2] != None and result[2] >= 0:
                        lateFeeAmount = "${:.2f}".format(float(result[2]))

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6a.insert("", tk.END, values=newTuple)
                else:
                    tree6a.insert("", tk.END, values=result)

            tree6a.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixAOutputFrame, text="Does not exist", font=defaultFont)
            errorLabel.pack(side=tk.TOP,)

    elif Q6aborrowerNameEntry.get():
        Q6aCursor.execute('''SELECT "borrower name", card_no, SUM(LateFeeBalance) from vBookLoanInfo
                            WHERE "borrower name" LIKE ?
                            GROUP BY card_no''', (tempBorrowerName,))
        Q6aResults = Q6aCursor.fetchall()

        if(Q6aResults):
            for result in Q6aResults:
                if result[2] == None or result[2] >= 0:

                    lateFeeAmount = "$0.00"

                    if result[2] != None and result[2] >= 0:
                        lateFeeAmount = "${:.2f}".format(float(result[2]))

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6a.insert("", tk.END, values=newTuple)
                else:
                    tree6a.insert("", tk.END, values=result)
            tree6a.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixAOutputFrame, text="User not found, maybe try Card No.?", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP)

    elif Q6acardNumberEntry.get():
        Q6aCursor.execute('''SELECT "borrower name", card_no, SUM(LateFeeBalance) from vBookLoanInfo
                            WHERE card_no = ?
                            GROUP BY card_no''', (Q6acardNumberEntry.get(),))
        Q6aResults = Q6aCursor.fetchall()
        
        if(Q6aResults):
            for result in Q6aResults:
                if result[2] == None or result[2] >= 0:

                    lateFeeAmount = "$0.00"

                    if result[2] != None and result[2] >= 0:
                        lateFeeAmount = "${:.2f}".format(float(result[2]))

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6a.insert("", tk.END, values=newTuple)
                else:
                    tree6a.insert("", tk.END, values=result)
            tree6a.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixAOutputFrame, text="User does not exist", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP)
        
    else:
        Q6aCursor.execute('''SELECT "borrower name", card_no, SUM(LateFeeBalance) from vBookLoanInfo GROUP BY card_no
                            ORDER BY LateFeeBalance DESC''')
        Q6aResults = Q6aCursor.fetchall()
        
        if(Q6aResults):
            for result in Q6aResults:
                if result[2] == None or result[2] >= 0:

                    lateFeeAmount = "$0.00"

                    if result[2] != None and result[2] >= 0:
                        lateFeeAmount = "${:.2f}".format(float(result[2]))

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6a.insert("", tk.END, values=newTuple)
                else:
                    tree6a.insert("", tk.END, values=result)
            tree6a.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixAOutputFrame, text="No data found", bg=_uta_blue, fg=_white, font=defaultFont)
            errorLabel.pack(side=tk.TOP)

    Q6aConnection.commit()
    Q6aConnection.close()

querySixAInputFrame = tk.Frame(tab6_a, background=_uta_orange)
querySixAInputFrame.pack(side=tk.LEFT, fill="both")

Q6aFiltersLabel = tk.Label(querySixAInputFrame, text="Search for Borrower", font=frameTitle, bg=_uta_orange, fg=_white)
Q6aFiltersLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

Q6acardNumberEntry = tk.Entry(querySixAInputFrame, font=defaultFont)
Q6acardNumberEntryLabel = tk.Label(querySixAInputFrame, text="Card No.", font=defaultFont, bg=_uta_orange, fg=_white)
Q6acardNumberEntryLabel.grid(row=1, column=0, sticky="sw", padx=10)
Q6acardNumberEntry.grid(row=2, column=0, sticky="sw", padx=10)

Q6aborrowerNameEntry = tk.Entry(querySixAInputFrame, font=defaultFont)
Q6aborrowerNameEntryLabel = tk.Label(querySixAInputFrame, text="Borrower Name", font=defaultFont, bg=_uta_orange, fg=_white)
Q6aborrowerNameEntryLabel.grid(row=3, column=0, sticky="sw", padx=10)
Q6aborrowerNameEntry.grid(row=4, column=0, sticky="sw", padx=10)

querySixAOutputFrame = tk.Frame(tab6_a, background=_uta_blue)
querySixAOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q6aOutputLabel = tk.Label(querySixAOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q6aOutputLabel.pack(side=tk.TOP)

Q6aSubmitButton = tk.Button(querySixAInputFrame, text='Submit', font=defaultFont, command=Q6aSubmit).grid(row=5, column=0, columnspan=2, pady=10)
# ----------------------------------


# -- Query 6.b --
def Q6bSubmit():
    global errorLabel
    global tree6b
    global resultLabel

    if tree6b.winfo_exists:
        for item in tree6b.get_children():
            tree6b.delete(item)
        tree6b.pack_forget()

    if errorLabel.winfo_exists:
        errorLabel.pack_forget()

    if resultLabel.winfo_exists:
        resultLabel.pack_forget()

    Q6bConnection = sqlite3.connect("./LMS.db")
    Q6bCursor = Q6bConnection.cursor()

    tree6b.heading("1", text="Book ID")
    tree6b.heading("2", text="Book Title")
    tree6b.heading("3", text="Late Fee")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=defaultFont)

    tree6b.column("1", anchor=tk.CENTER)
    tree6b.column("2", anchor=tk.CENTER)
    tree6b.column("3", anchor=tk.CENTER)

    Q6bCursor.execute('''DROP VIEW IF EXISTS vBookLoanInfo''')
    
    Q6bCursor.execute('''
    CREATE VIEW vBookLoanInfo AS
    SELECT BL.Card_no AS Card_No,
           BR.name as 'Borrower Name',
           BL.Date_out as Date_Out,
           BL.Due_date as Due_Date,
           BL.Returned_date,
           (JulianDay(BL.Returned_date) - JulianDay(BL.Date_out)) as TotalDays,
           BK.Title as 'Book Title',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)
           END AS 'Number of days later return',
           BL.Branch_id as 'Branch ID',
           CASE
             WHEN BL.Returned_date <= BL.Due_date THEN 0
             ELSE (JulianDay(BL.Returned_date) - JulianDay(BL.Due_date)) * (SELECT LateFee
                                                                            FROM Library_Branch LB
                                                                            WHERE LB.branch_id = BL.Branch_id)
           END AS LateFeeBalance
    FROM Book_Loans BL
    JOIN Borrower BR ON BL.Card_no = BR.Card_no
    JOIN Book BK ON BL.Book_id = BK.Book_id
    JOIN Library_branch LB ON BL.branch_id = LB.Branch_id;
    ''')

    if(Q6bBookIDEntry.get() and Q6bBookTitleEntry.get()):    
        tempBookTitle = "%"+str(Q6bBookTitleEntry.get())+"%"
        Q6bCursor.execute('''SELECT B.Book_id, VB."Book Title", LB.LateFee from vBookLoanInfo VB, Library_branch LB, Book B
                            WHERE B.Book_id = ? AND VB."Book Title" LIKE ? AND VB."Branch ID" = LB.branch_id AND B.Title = VB."Book Title"
                            GROUP BY card_no''', (Q6bBookIDEntry.get(), tempBookTitle,))
        Q6bResults = Q6bCursor.fetchall()
        print(Q6bResults)

        if(Q6bResults):
            for result in Q6bResults:
                if result[2] == 0 or result[2] == None:
                    lateFeeAmount = "Non-Applicable"

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6b.insert("", tk.END, values=newTuple)
                else:
                    tree6b.insert("", tk.END, values=result)            
            tree6b.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixBOutputFrame, text="Book does not exist", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP,)

    elif(Q6bBookTitleEntry.get()):
        tempBookTitle = "%"+str(Q6bBookTitleEntry.get())+"%"
        Q6bCursor.execute('''SELECT B.Book_id, VB."Book Title", LB.LateFee from vBookLoanInfo VB, Library_branch LB, Book B
                            WHERE VB."Book Title" LIKE ? AND VB."Branch ID" = LB.branch_id AND B.Title = VB."Book Title" GROUP BY book_id''', (tempBookTitle,))
        Q6bResults = Q6bCursor.fetchall()

        if(Q6bResults):
            for result in Q6bResults:
                if result[2] == 0 or result[2] == None:
                    lateFeeAmount = "Non-Applicable"

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6b.insert("", tk.END, values=newTuple)
                else:
                    tree6b.insert("", tk.END, values=result)      
            tree6b.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixBOutputFrame, text="Book Title does not exist", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP)
                    
    elif(Q6bBookIDEntry.get()):
        Q6bCursor.execute('''SELECT B.Book_id, VB."Book Title", LB.LateFee from vBookLoanInfo VB, Library_branch LB, Book B
                            WHERE B.book_id = ? AND VB."Branch ID" = LB.branch_id AND B.Title = VB."Book Title" GROUP BY B.book_id''', (Q6bBookIDEntry.get(),))
        Q6bResults = Q6bCursor.fetchall()
        print(Q6bResults)
        
        if(Q6bResults):
            for result in Q6bResults:
                if result[2] == 0 or result[2] == None:
                    lateFeeAmount = "Non-Applicable"

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6b.insert("", tk.END, values=newTuple)
                else:
                    tree6b.insert("", tk.END, values=result)      
            tree6b.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixBOutputFrame, text="Book ID does not exist", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP)
            
    else:
        Q6bCursor.execute('''SELECT B.Book_id, VB."Book Title", LB.LateFee FROM vBookLoanInfo VB, Library_branch LB, Book B
                            WHERE VB."Branch ID" = LB.branch_id AND B.Title = VB."Book Title" GROUP BY book_id 
                            ORDER BY LB.LateFee DESC''')
        Q6bResults = Q6bCursor.fetchall()

        if(Q6bResults):
            for result in Q6bResults:
                if result[2] == 0 or result[2] == None:
                    lateFeeAmount = "Non-Applicable"

                    newTuple = (result[0], result[1], lateFeeAmount)
                    tree6b.insert("", tk.END, values=newTuple)
                else:
                    tree6b.insert("", tk.END, values=result)      
            tree6b.pack(padx=10, pady=10)
        else:
            errorLabel = tk.Label(querySixBOutputFrame, text="Book ID does not exist", font=defaultFont, bg=_uta_blue, fg=_white)
            errorLabel.pack(side=tk.TOP)
    

    Q6bConnection.commit()
    Q6bConnection.close()

querySixBInputFrame = tk.Frame(tab6_b, background=_uta_orange)
querySixBInputFrame.pack(side=tk.LEFT, fill="both")

Q6bFiltersLabel = tk.Label(querySixBInputFrame, text="Search for a Book", font=frameTitle, bg=_uta_orange, fg=_white)
Q6bFiltersLabel.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

Q6bBookIDEntry = tk.Entry(querySixBInputFrame, font=defaultFont)
Q6bBookIDEntryLabel = tk.Label(querySixBInputFrame, text="Book ID", font=defaultFont, bg=_uta_orange, fg=_white)
Q6bBookIDEntryLabel.grid(row=6, column=0, sticky="sw", padx=10)
Q6bBookIDEntry.grid(row=7, column=0, sticky="sw", padx=10)

Q6bBookTitleEntry = tk.Entry(querySixBInputFrame, font=defaultFont)
Q6bBookTitleEntryLabel = tk.Label(querySixBInputFrame, text="Book Title", font=defaultFont, bg=_uta_orange, fg=_white)
Q6bBookTitleEntryLabel.grid(row=8, column=0, sticky="sw", padx=10)
Q6bBookTitleEntry.grid(row=9, column=0, sticky="sw", padx=10)

querySixBOutputFrame = tk.Frame(tab6_b, background=_uta_blue)
querySixBOutputFrame.pack(side=tk.RIGHT, fill="both", expand=True)

Q6bOutputLabel = tk.Label(querySixBOutputFrame, text="Output", font=frameTitle, bg=_uta_blue, fg=_white)
Q6bOutputLabel.pack(side=tk.TOP)

Q6bSubmitButton = tk.Button(querySixBInputFrame, text="Submit", font=defaultFont,
                           command=Q6bSubmit).grid(row=14, column=0, columnspan=2, pady=10)
# ----------------------------------


# global variables

errorLabel = tk.Label()
resultLabel = tk.Label()
resultFrame: tk.Frame()

tree1 = ttk.Treeview(queryOneOutputFrame, columns=("1", "2", "3", "4", "5", "6", "7"), show='headings', height=20)
tree2 = ttk.Treeview(queryTwoOutputFrame, columns=("1", "2", "3", "4"), show='headings', height=20)
tree3 = ttk.Treeview(queryThreeOutputFrame, columns=("1", "2", "3"), show='headings', height=20)
tree4 = ttk.Treeview(queryFourOutputFrame, columns=("1", "2"), show='headings', height=10)
tree5 = ttk.Treeview(queryFiveOutputFrame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), show='headings', height=20)
tree6a = ttk.Treeview(querySixAOutputFrame, columns=("1", "2", "3"), show='headings', height=10)
tree6b = ttk.Treeview(querySixBOutputFrame, columns=("1", "2", "3"), show='headings', height=10)

# creates the mainloop of the GUI
LMS_GUI_WINDOW.mainloop()