-- Task 1 --
CREATE TABLE IF NOT EXISTS Publisher(
    Publisher_name text PRIMARY KEY NOT NULL,
    phone_number varchar(10) NOT NULL,
    address text
);

CREATE TABLE IF NOT EXISTS Library_branch(
    Branch_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Branch_name text NOT NULL,
    Branch_address text NOT NULL
);

CREATE TABLE IF NOT EXISTS Borrower(
    Card_no INTEGER PRIMARY KEY NOT NULL,
    name text NOT NULL,
    address text NOT NULL,
    phone_number varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS Book(
    Book_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    Title text NOT NULL,
    Book_publisher text NOT NULL
);

CREATE TABLE IF NOT EXISTS Book_Loans(
    Book_id INTEGER NOT NULL,
    Branch_id INTEGER NOT NULL,
    Card_no INTEGER NOT NULL,
    Date_out text NOT NULL,
    Due_date text NOT NULL,
    Returned_date DATE,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES Library_branch(Branch_id),
    FOREIGN KEY (Card_no) REFERENCES Borrower(Card_no)
);

CREATE TABLE IF NOT EXISTS Book_copies(
    Book_id INTEGER NOT NULL,
    Branch_id INTEGER NOT NULL,
    No_of_copies INTEGER,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES Library_branch(Branch_id)
);

CREATE TABLE IF NOT EXISTS Book_authors(
    Book_id INTEGER NOT NULL,
    Author_name text NOT NULL,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id)
);
-- End Task 1 --

-- Task 2 --

.mode csv

.import --skip 1 ./CSV_Data/Publisher.csv Publisher
.import --skip 1 ./CSV_Data/Library_Branch.csv Library_branch
.import --skip 1 ./CSV_Data/Borrower.csv Borrower
.import --skip 1 ./CSV_Data/Book.csv Book
.import --skip 1 ./CSV_Data/Book_Loans.csv Book_Loans
.import --skip 1 ./CSV_Data/Book_Copies.csv Book_copies
.import --skip 1 ./CSV_Data/Book_Authors.csv Book_authors

.mode column
.header on

-- End Task 2 --