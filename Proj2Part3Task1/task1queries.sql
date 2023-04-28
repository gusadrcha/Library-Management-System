-- Query 1 --
ALTER TABLE book_loans ADD COLUMN Late INTEGER DEFAULT 0;
UPDATE book_loans
SET Late = 1
WHERE Returned_date > Due_date;


-- Query 2 --
ALTER TABLE Library_Branch ADD COLUMN LateFee INTEGER DEFAULT 0;
UPDATE Library_Branch
SET LateFee = (
    SELECT COUNT(Late) * 10
    FROM Book_Loans BL
    WHERE BL.Branch_id = Library_Branch.Branch_id
    AND BL.Returned_date > BL.Due_date
)
WHERE EXISTS (
    SELECT 1
    FROM Book_Loans BL
    WHERE BL.Branch_id = Library_Branch.Branch_id
    AND BL.Returned_date > BL.Due_date
);

