-- 

create database if not exists data201project;

use data201project;

drop table laptops;
create table laptops (laptop varchar(150) not null,
	brand varchar(25) not null,
    model varchar(15) not null,
    `cpu` varchar(25) not null,
    ram int not null,
    `storage` int not null,
    storage_type varchar(10) not null,
    gpu varchar(30) not null,
    screen decimal(4, 2) not null,
    final_price decimal(9, 2) not null,
    cpu_brand varchar(15) not null,
    cpu_series varchar(15) not null,
    touch int not null,
    is_new int not null,
    has_discrete_gpu int not null,
    price_per_ram_gb decimal(7, 2) not null,
    price_per_storage_gb decimal(7, 5) not null,
    price_tier varchar(20) not null,
    ram_tier varchar(20) not null
);


SHOW VARIABLES LIKE "secure_file_priv";

SET GLOBAL local_infile = 1;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 9.3\\Uploads\\laptops_cleaned.csv'
INTO TABLE laptops
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- adding performance column
ALTER TABLE laptops ADD COLUMN performance INT;

UPDATE laptops 
SET performance = ROUND((ram * 0.5) + (storage * 0.05) + (price_per_ram_gb * 10));