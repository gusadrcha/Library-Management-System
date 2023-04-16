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

-- Question 4 --
INSERT INTO Book (title, book_author)
VALUES ("Harry Potter and the Sorcerer's Stone", 'J.K. Rowling');

-- Question 7 --
SELECT Branch_id,
        (SELECT COUNT(*) FROM Book_Loans WHERE Returned_date IS NOT NULL) as Returned,
        (SELECT COUNT(*) FROM Book_Loans WHERE Returned_date IS NULL) as Borrowed,
        (SELECT COUNT(*) FROM Book_Loans WHERE Returned_date > Due_date GROUP BY Branch_id) as Late
FROM Book_Loans
GROUP BY Branch_id;

-- Question 8 --
SELECT MAX(julianday(Returned_date) - julianday(Date_out)) as Max
FROM Book_loans;

-- Question 9 --
SELECT Title, Author_name, julianday(Returned_date) - julianday(Date_out) as Borrowed, Returned_date > Due_date as Late
FROM Book_authors, Borrower, Book_loans, Book
WHERE Borrower.name = 'Ethan Martinez' AND Borrower.Card_no = Book_loans.Card_no
GROUP BY date_out;

-- Question 10 --
SELECT name, address
FROM Borrower, Book_Loans
WHERE Borrower.Card_no = Book_Loans.Card_no;