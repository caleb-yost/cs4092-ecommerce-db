-- CS4092 Project: E-Commerce Backend
-- Schema creation + sample data (SQLite dialect)
-- Run with: sqlite3 ecommerce.db < schema.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Purchase;
DROP TABLE IF EXISTS CreditCard;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Staff;

CREATE TABLE Staff (
    staff_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    role        TEXT NOT NULL
);

CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    phone       TEXT
);

CREATE TABLE Product (
    product_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name               TEXT NOT NULL,
    price              DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    quantity_in_stock  INTEGER NOT NULL CHECK (quantity_in_stock >= 0),
    added_by_staff_id  INTEGER NOT NULL,
    FOREIGN KEY (added_by_staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE CreditCard (
    card_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL,
    card_last4    TEXT NOT NULL,
    expiry        TEXT NOT NULL,
    billing_zip   TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Purchase (
    purchase_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id    INTEGER NOT NULL,
    product_id     INTEGER NOT NULL,
    card_id        INTEGER NOT NULL,
    quantity       INTEGER NOT NULL CHECK (quantity > 0),
    purchase_date  TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (card_id) REFERENCES CreditCard(card_id)
);

-- Sample data -----------------------------------------------------------

INSERT INTO Staff (name, role) VALUES
    ('Alice Nguyen', 'Inventory Manager'),
    ('Marcus Webb',  'Catalog Admin');

INSERT INTO Customer (name, email, phone) VALUES
    ('Jordan Lee',    'jordan.lee@example.com',    '555-0101'),
    ('Priya Shah',    'priya.shah@example.com',    '555-0102'),
    ('Sam Whitfield', 'sam.whitfield@example.com', '555-0103');

INSERT INTO Product (name, price, quantity_in_stock, added_by_staff_id) VALUES
    ('Wireless Mouse',        24.99,  50, 1),
    ('Mechanical Keyboard',  129.99,  20, 1),
    ('27" Monitor',          249.99,  15, 2),
    ('USB-C Hub',             39.99,  75, 2),
    ('Noise-Cancelling Headphones', 179.99, 30, 1);

INSERT INTO CreditCard (customer_id, card_last4, expiry, billing_zip) VALUES
    (1, '4242', '2028-01', '45202'),
    (2, '1881', '2027-09', '45219'),
    (3, '9911', '2029-03', '45211'),
    (1, '5566', '2026-11', '45202');

INSERT INTO Purchase (customer_id, product_id, card_id, quantity, purchase_date) VALUES
    (1, 2, 1, 1, '2026-06-01'),
    (1, 4, 4, 2, '2026-06-15'),
    (2, 3, 2, 1, '2026-06-20'),
    (3, 5, 3, 1, '2026-07-02'),
    (2, 1, 2, 3, '2026-07-10'),
    (3, 2, 3, 1, '2026-07-18');
