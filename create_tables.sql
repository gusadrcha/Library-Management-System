-- Task 1 --
CREATE TABLE IF NOT EXISTS Publisher(
    Publisher_name text PRIMARY KEY NOT NULL,
    phone_number varchar(10),
    address text
);

CREATE TABLE IF NOT EXISTS Library_branch(
    Branch_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Branch_name text,
    Branch_address text
);

CREATE TABLE IF NOT EXISTS Borrower(
    Card_no INTEGER PRIMARY KEY NOT NULL,
    name text,
    address text,
    phone_number varchar(10)
);

CREATE TABLE IF NOT EXISTS Book(
    Book_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    Title text,
    Book_publisher text
);

CREATE TABLE IF NOT EXISTS Book_Loans(
    Book_id INTEGER,
    Branch_id INTEGER,
    Card_no INTEGER,
    Date_out text,
    Due_date text,
    Returned_date DATE,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES Library_branch(Branch_id),
    FOREIGN KEY (Card_no) REFERENCES Borrower(Card_no)
);

CREATE TABLE IF NOT EXISTS Book_copies(
    Book_id INTEGER,
    Branch_id INTEGER,
    No_of_copies INTEGER,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES Library_branch(Branch_id)
);

CREATE TABLE IF NOT EXISTS Book_authors(
    Book_id INTEGER,
    Author_name text,
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