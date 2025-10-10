--      Connect and Sanity check the DB
-- Testing connection
SELECT * FROM Artist LIMIT 5; 

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

--      Sanity Checks (data quality quick tests)
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
SELECT AlbumId, COUNT(*) AS count
    FROM Album
    GROUP BY AlbumId
    HAVING COUNT(*) > 1;
SELECT ArtistId, COUNT(*)
    FROM Artist
    GROUP BY ArtistId
    HAVING COUNT(*) > 1;
SELECT CustomerId, COUNT(*) AS count 
    FROM Customer 
    GROUP BY CustomerId
    HAVING COUNT(*) > 1;
SELECT EmployeeId, COUNT(*) AS count
    FROM Employee
    GROUP BY EmployeeId
    HAVING COUNT(*) > 1;
SELECT GenreId, COUNT(*) AS count 
    FROM Genre
    GROUP BY GenreId
    HAVING COUNT(*) > 1;
SELECT InvoiceId, COUNT(*) AS count
    FROM Invoice
    GROUP BY InvoiceId
    HAVING COUNT(*) > 1;
SELECT InvoiceLineId, COUNT(*) AS count
    FROM InvoiceLine
    GROUP BY InvoiceLineId
    HAVING COUNT(*) > 1;
SELECT MediaTypeId, COUNT(*) AS count 
    FROM MediaType
    GROUP BY MediaTypeId
    HAVING COUNT(*) > 1;
SELECT PlaylistId, Count(*) AS count 
    FROM Playlist
    GROUP BY PlaylistId
    HAVING COUNT(*) > 1;
SELECT TrackID, COUNT(*) AS count 
    FROM Track
    GROUP BY TrackId
    HAVING COUNT(*) > 1;


--      Compute KPIs (core metrics)
-- Calculating Total Revenue
SELECT SUM(Total)
    FROM Invoice
SELECT SUM(UnitPrice * Quantity)
    FROM InvoiceLine

--Example JOIN - not needed
SELECT invoice.Total AS total, 
    invoice_line.UnitPrice AS unit_price,
    invoice_line.Quantity AS quantity, 
    (invoice_line.UnitPrice * invoice_line.Quantity) AS revenue
    FROM Invoice AS invoice
    JOIN InvoiceLine AS invoice_line
    ON invoice.InvoiceId = invoice_line.InvoiceId;

-- Finding number of customers 
SELECT DISTINCT COUNT(CustomerId)
    FROM Customer;
SELECT DISTINCT CustomerId, COUNT(CustomerId) AS count
    FROM Invoice
    GROUP BY CustomerId;
SELECT COUNT(DISTINCT CustomerId) AS unique_customers
    FROM Invoice;

-- Finding the number of Invoices/Transactions
SELECT COUNT(*) AS transactions
    FROM Invoice;

-- Average Invoice value 
SELECT AVG(Total)
    FROM Invoice
SELECT (SUM(Total)/COUNT(Total)) AS avg_total
    FROM Invoice;

-- Average items per invoice
SELECT InvoiceId, SUM(Quantity) AS quantity_sum
    FROM InvoiceLine
    GROUP BY InvoiceId;

SELECT AVG(items_per_invoice) AS avg_items_per_invoice
    FROM (
        SELECT InvoiceId, SUM(Quantity) AS items_per_invoice
            FROM InvoiceLine
            GROUP BY InvoiceId
    );

-- Average Revenue per Customer
SELECT CustomerId, SUM(Total) AS total_sum
    FROM Invoice
    GROUP BY CustomerId;

SELECT AVG(rev_per_customer) AS avg_rev_per_customer
    FROM (
        SELECT CustomerId, SUM(Total) AS rev_per_customer
    FROM Invoice
    GROUP BY CustomerId
    );

-- Revenue by Country
SELECT customer.Country AS country,
    SUM(invoice.Total) as country_total
        FROM Customer AS customer
        JOIN Invoice AS invoice
        ON customer.CustomerId = invoice.CustomerId
        GROUP BY customer.Country

-- Monthly Revenue
SELECT STRFTIME('%Y-%m', InvoiceDate) AS invoice_date,
    SUM(Total) AS total_per_month
    FROM Invoice
    GROUP BY invoice_date
    ORDER BY invoice_date
    
--      Top Performers - design & checks
-- Customers by revenue
SELECT SUM(invoice.Total) AS total_per_customer,
    customer.FirstName,
    customer.LastName,
    customer.City
    FROM Invoice AS invoice
    JOIN Customer AS customer
    ON invoice.CustomerId = customer.CustomerId
    GROUP BY customer.CustomerId
    ORDER BY total_per_customer DESC 
    LIMIT 10;

-- Tracks by revenue
SELECT TrackID,
    SUM(UnitPrice) AS total_per_track
    FROM InvoiceLine
    GROUP BY TrackID
    ORDER BY total_per_track DESC
    LIMIT 20;

SELECT track.TrackId AS track_id,
    track.Name AS song_name,
    album.Title As album,
    artist.NAME AS artist,
    SUM(invoice_line.UnitPrice) AS revenue_per_track
    FROM InvoiceLine AS invoice_line
    JOIN Track AS track
    ON invoice_line.TrackId = track.TrackId
    JOIN Album AS album
    ON track.AlbumId = album.AlbumId
    JOIN Artist AS artist
    ON album.ArtistId = artist.ArtistId
    GROUP BY track.TrackId 
    ORDER BY revenue_per_track DESC
    LIMIT 10;

-- Genres by revenue
SELECT GenreID,
    COUNT(GenreID)
    FROM Track
    GROUP BY GenreId;

SELECT genre.GenreID AS genre_id,
    genre.Name AS genre_name,
    SUM(invoice_line.UnitPrice * invoice_line.Quantity) AS revenue_per_genre
    FROM InvoiceLine AS invoice_line
    JOIN Track as track 
    ON invoice_line.TrackId = track.TrackId 
    JOIN Genre AS genre 
    ON genre.GenreId = track.GenreId
    GROUP BY genre.Name 
    ORDER BY revenue_per_genre DESC;
/* Worth noting that multiplying by quantity in the aggregation formula is 
unnecessary as the Quantity in InvoiceLine is always 1, but it's worth having in the
calculation in case that changes */


--      Time Series & Trends
-- Monthly revenue grouped by bucket
--No different to monthly revenue above, not sure what the intention is for this query
SELECT STRFTIME('%Y-%m', InvoiceDate) AS month_bucket,
    SUM(Total) AS revenue
    FROM Invoice
    GROUP BY month_bucket
    ORDER BY month_bucket;

-- Monthly order counts - distinct invoice ids per month
SELECT STRFTIME('%Y-%m', InvoiceDate) AS invoice_date,
    COUNT(DISTINCT InvoiceId)
    FROM Invoice
    GROUP BY invoice_date
    ORDER BY invoice_date;

-- Month-over-monnth growth
SELECT month, 
    revenue, 
    ROUND(revenue - LAG(revenue, 1) OVER (ORDER BY month), 2) AS monthly_change
    FROM (
        SELECT STRFTIME('%Y-%m', InvoiceDate) AS month,
            SUM(Total) AS revenue
            FROM Invoice
            GROUP BY month
            ORDER BY month
    );

--      Customer Behaviour & Cohorts
-- First purchase date for each customer
SELECT DISTINCT customer.CustomerId AS customer_id, 
    MIN(STRFTIME('%Y-%m-%d', invoice.InvoiceDate)) AS first_invoice
    FROM Customer AS customer 
    JOIN Invoice AS invoice 
    ON customer.CustomerId = invoice.CustomerId 
    GROUP BY customer.CustomerId 
    ORDER BY customer.CustomerId;

-- Number of invoices per customer
SELECT DISTINCT customer.CustomerId AS customer_id, 
    COUNT(invoice.CustomerId) AS number_of_invoices
    FROM Customer AS customer 
    JOIN Invoice AS invoice 
    ON customer.CustomerId = invoice.CustomerId 
    GROUP BY customer.CustomerId 
    ORDER BY customer.CustomerId;
--Check
SELECT COUNT(CustomerId)
    FROM Invoice
    GROUP BY CustomerId
    ORDER BY CustomerId;

-- Customer retention: purchased in two consecutive months
