-- Query 1 --
ALTER TABLE book_loans 
ADD COLUMN Late INTEGER DEFAULT 0;

UPDATE book_loans
SET Late = 1
WHERE Returned_date > Due_date;

-- Query 2 --
ALTER TABLE Library_Branch ADD COLUMN LateFee INTEGER DEFAULT 0;

UPDATE Library_Branch
SET LateFee = 10
WHERE Branch_id = 1;

UPDATE Library_Branch
SET LateFee = 20
WHERE Branch_id = 2;

UPDATE Library_Branch
SET LateFee = 30
WHERE Branch_id = 3;

UPDATE Library_branch
SET LateFee = 40
WHERE Branch_id = 4;

UPDATE Library_branch
SET LateFee = 50
WHERE Branch_id = 5;

-- Query 3 --
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