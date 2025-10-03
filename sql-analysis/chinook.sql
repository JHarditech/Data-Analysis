-- Testing connection
--SELECT * FROM Artist LIMIT 5; 

-- Check tables and show column headings
SELECT * FROM sqlite_master WHERE type = 'table';

-- Querying each table 
SELECT * FROM Album LIMIT 5;
SELECT * FROM Artist LIMIT 5;
SELECT * FROM Customer LIMIT 5;
SELECT * FROM Employee LIMIT 5;
SELECT * FROM Genre LIMIT 5;
SELECT * FROM Invoice LIMIT 5;
SELECT * FROM InvoiceLine LIMIT 5;
SELECT * FROM MediaType LIMIT 5;
SELECT * FROM Playlist LIMIT 5;
SELECT * FROM PlaylistTrack LIMIT 5;
SELECT * FROM Track LIMIT 5;


-- Check row counts
SELECT COUNT(*) FROM Album;
SELECT COUNT(*) FROM Artist;
SELECT COUNT(*) FROM Customer;
SELECT COUNT(*) FROM Employee;
SELECT COUNT(*) FROM Genre;
SELECT COUNT(*) FROM Invoice;
SELECT COUNT(*) FROM InvoiceLine;
SELECT COUNT(*) FROM MediaType;
SELECT COUNT(*) FROM Playlist; 
SELECT COUNT(*) FROM PlaylistTrack;
SELECT COUNT(*) FROM Track;

-- Identity check
PRAGMA integrity_check;

-- Checking for NULLs and negative values
SELECT * FROM InvoiceLine 
    WHERE UnitPrice IS NULL;
SELECT * FROM InvoiceLine 
    WHERE Quantity IS NULL;
SELECT COUNT(*) FROM InvoiceLine 
    WHERE UnitPrice <= 0;
SELECT COUNT(*) FROM InvoiceLine 
    WHERE Quantity <= 0;


-- Checking for duplicate IDs
SELECT InvoiceId, COUNT(*) AS count
    FROM Invoice
    GROUP BY InvoiceId
    HAVING COUNT(*) >= 1

