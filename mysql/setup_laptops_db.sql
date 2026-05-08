-- Laptop Price Analysis Database Setup
-- This script creates the project database, creates the laptops table,
-- loads the cleaned CSV file, and adds a performance score column.

CREATE DATABASE IF NOT EXISTS laptops_db;

USE laptops_db;

DROP TABLE IF EXISTS laptops;

CREATE TABLE laptops (
    laptop VARCHAR(150) NOT NULL,
    brand VARCHAR(25) NOT NULL,
    model VARCHAR(50) NOT NULL,
    cpu VARCHAR(50) NOT NULL,
    ram INT NOT NULL,
    storage INT NOT NULL,
    storage_type VARCHAR(10) NOT NULL,
    gpu VARCHAR(30) NOT NULL,
    screen DECIMAL(4, 2) NOT NULL,
    final_price DECIMAL(9, 2) NOT NULL,
    cpu_brand VARCHAR(15) NOT NULL,
    cpu_series VARCHAR(25) NOT NULL,
    touch INT NOT NULL,
    is_new INT NOT NULL,
    has_discrete_gpu INT NOT NULL,
    price_per_ram_gb DECIMAL(7, 2) NOT NULL,
    price_per_storage_gb DECIMAL(7, 5) NOT NULL,
    price_tier VARCHAR(20) NOT NULL,
    ram_tier VARCHAR(20) NOT NULL
);

-- Check the secure file upload directory.
-- The CSV file must be placed in this directory if using LOAD DATA INFILE.
SHOW VARIABLES LIKE 'secure_file_priv';

-- Enable local infile loading if needed.
SET GLOBAL local_infile = 1;

-- Load cleaned laptop dataset.
-- Update this path if your MySQL upload folder is different.
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 9.3\\Uploads\\laptops_cleaned.csv'
INTO TABLE laptops
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Add performance column for dashboard analysis.
ALTER TABLE laptops
ADD COLUMN performance INT;

-- Temporarily disable safe update mode for full-table update.
SET SQL_SAFE_UPDATES = 0;

UPDATE laptops
SET performance = ROUND((ram * 0.5) + (storage * 0.05) + (price_per_ram_gb * 10));

SET SQL_SAFE_UPDATES = 1;

-- Verify loaded data.
SELECT laptop, brand, ram, storage, price_per_ram_gb, performance
FROM laptops
LIMIT 10;