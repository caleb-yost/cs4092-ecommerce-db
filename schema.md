# Relational Schema — E-Commerce Backend

Derived directly from the [ER diagram](er_diagram.md). Notation: `PK` = primary key,
`FK` = foreign key.

## Staff
| Column | Type | Constraint |
|---|---|---|
| staff_id | INTEGER | PK |
| name | TEXT | NOT NULL |
| role | TEXT | NOT NULL |

`Staff(staff_id PK, name, role)`

## Customer
| Column | Type | Constraint |
|---|---|---|
| customer_id | INTEGER | PK |
| name | TEXT | NOT NULL |
| email | TEXT | NOT NULL, UNIQUE |
| phone | TEXT | |

`Customer(customer_id PK, name, email, phone)`

## Product
| Column | Type | Constraint |
|---|---|---|
| product_id | INTEGER | PK |
| name | TEXT | NOT NULL |
| price | DECIMAL(10,2) | NOT NULL |
| quantity_in_stock | INTEGER | NOT NULL |
| added_by_staff_id | INTEGER | FK → Staff(staff_id) |

`Product(product_id PK, name, price, quantity_in_stock, added_by_staff_id FK → Staff)`

## CreditCard
| Column | Type | Constraint |
|---|---|---|
| card_id | INTEGER | PK |
| customer_id | INTEGER | FK → Customer(customer_id) |
| card_last4 | TEXT | NOT NULL |
| expiry | TEXT | NOT NULL |
| billing_zip | TEXT | |

`CreditCard(card_id PK, customer_id FK → Customer, card_last4, expiry, billing_zip)`

## Purchase
| Column | Type | Constraint |
|---|---|---|
| purchase_id | INTEGER | PK |
| customer_id | INTEGER | FK → Customer(customer_id) |
| product_id | INTEGER | FK → Product(product_id) |
| card_id | INTEGER | FK → CreditCard(card_id) |
| quantity | INTEGER | NOT NULL |
| purchase_date | TEXT (ISO date) | NOT NULL |

`Purchase(purchase_id PK, customer_id FK → Customer, product_id FK → Product, card_id FK → CreditCard, quantity, purchase_date)`

## Summary
5 relations total (exceeds the individual-project minimum of 4): **Staff, Customer,
Product, CreditCard, Purchase**. Every foreign key references a primary key in another
relation, matching the cardinalities documented in the ER diagram. The full DDL is in
[schema.sql](schema.sql).
