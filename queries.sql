-- Task 2 Query --
SELECT COUNT(*) FROM Publisher UNION ALL
SELECT COUNT(*) FROM Library_branch UNION ALL
SELECT COUNT(*) FROM Borrower UNION ALL
SELECT COUNT(*) FROM Book UNION ALL
SELECT COUNT(*) FROM Book_Loans UNION ALL
SELECT COUNT(*) FROM Book_copies UNION ALL
SELECT COUNT(*) FROM Book_authors;

-- Question 1 --
INSERT INTO Borrower (name, address, phone_number)
VALUES ('Gustavo Chavez', '200 N Stadium Dr, Seymour, TX 76380', '9032040703');

SELECT *
FROM Borrower
WHERE name = 'Gustavo Chavez';

-- Question 2 --
UPDATE Borrower
SET phone_number = '8377218965'
WHERE name = 'Gustavo Chavez';

SELECT *
FROM Borrower
WHERE name = 'Gustavo Chavez';

-- Question 3 -- 
UPDATE Book_copies
SET no_of_copies = no_of_copies + 1
WHERE branch_id = (SELECT branch_id
                   FROM library_branch
                   WHERE branch_name = 'East Branch');

-- Question 4a --
INSERT INTO Book (title, book_author)
VALUES ("Harry Potter and the Sorcerer's Stone", 'J.K. Rowling');

-- Question 4b --
INSERT INTO Library_branch
VALUES (null, 'North Branch', '456 NW, Irving, TX 76100'), (null, 'UTA Branch', '123 Cooper St, Arlington TX 76101');

-- Question 5 --
SELECT Title, Branch_name, julianday(Returned_date) - julianday(Date_out) as Borrowed
FROM Library_branch, Book, Book_loans WHERE Book_loans.Book_id = Book.Book_id AND 
Book_loans.Branch_id = Library_branch.Branch_id AND Date_out BETWEEN '2022-03-05' AND '2022-03-23';

-- Question 6 --
SELECT B.name FROM Borrower B, Book_Loans BL WHERE BL.Card_no = B.Card_no AND BL.Returned_date IS NULL;

-- Question 7 --
SELECT Branch_id,
      (SELECT COUNT(*) FROM (LIBRARY_BRANCH NATURAL JOIN BOOK_LOANS) joiner WHERE joiner.Branch_id=LBBL.Branch_id GROUP BY joiner.Branch_Id) as Returned,
      (SELECT COUNT(*)  FROM BOOK_LOANS as BL WHERE BL.Branch_id=LBBL.Branch_id and ((JULIANDAY(BL.Returned_date)>JULIANDAY(BL.Due_Date))) GROUP BY BL.Branch_id) as Late
FROM (LIBRARY_BRANCH NATURAL JOIN BOOK_LOANS) LBBL
GROUP BY LBBL.Branch_id;

-- Question 8 --
SELECT MAX(julianday(Returned_date) - julianday(Date_out)) as Max
FROM Book_loans;

-- Question 9 --
SELECT Title, Author_name, julianday(Returned_date) - julianday(Date_out) as Borrowed, Returned_date > Due_date as Late
FROM Book_authors, Borrower, Book_loans, Book
WHERE Borrower.name = 'Ethan Martinez' AND Borrower.Card_no = Book_Loans.Card_no 
AND Book.book_id = Book_Loans.book_id AND Book_authors.book_id = Book.book_id GROUP BY date_out;

-- Question 10 --
SELECT name, address
FROM Borrower, Book_Loans
WHERE Borrower.Card_no = Book_Loans.Card_no;
