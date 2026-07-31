"""CS4092 project: CLI business-logic layer over the e-commerce SQLite database."""
import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "ecommerce.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    first_run = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    if first_run:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.commit()
    return conn


def prompt_int(label):
    while True:
        raw = input(label)
        if raw.isdigit():
            return int(raw)
        print("Please enter a whole number.")


def prompt_float(label):
    while True:
        raw = input(label)
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number.")


# --- Staff actions -------------------------------------------------------

def staff_add_product(conn):
    print("\nStaff on file:")
    for row in conn.execute("SELECT staff_id, name FROM Staff"):
        print(f"  {row[0]}: {row[1]}")
    staff_id = prompt_int("Your staff_id: ")
    name = input("Product name: ").strip()
    price = prompt_float("Price: $")
    qty = prompt_int("Starting stock quantity: ")
    conn.execute(
        "INSERT INTO Product (name, price, quantity_in_stock, added_by_staff_id) "
        "VALUES (?, ?, ?, ?)",
        (name, price, qty, staff_id),
    )
    conn.commit()
    print(f"Added '{name}'.")


def staff_edit_product(conn):
    staff_view_inventory(conn)
    product_id = prompt_int("\nproduct_id to edit: ")
    row = conn.execute(
        "SELECT name, price, quantity_in_stock FROM Product WHERE product_id = ?",
        (product_id,),
    ).fetchone()
    if row is None:
        print("No such product.")
        return
    print(f"Current: name={row[0]}, price={row[1]}, stock={row[2]}")
    price = prompt_float("New price: $")
    qty = prompt_int("New stock quantity: ")
    conn.execute(
        "UPDATE Product SET price = ?, quantity_in_stock = ? WHERE product_id = ?",
        (price, qty, product_id),
    )
    conn.commit()
    print("Updated.")


def staff_view_inventory(conn):
    print("\nInventory:")
    for row in conn.execute(
        "SELECT product_id, name, price, quantity_in_stock FROM Product ORDER BY product_id"
    ):
        print(f"  [{row[0]}] {row[1]:<28} ${row[2]:>8.2f}  stock={row[3]}")


def staff_menu(conn):
    actions = {
        "1": staff_add_product,
        "2": staff_edit_product,
        "3": staff_view_inventory,
    }
    while True:
        print("\n-- Staff Menu --")
        print("1) Add product\n2) Edit product\n3) View inventory\n4) Back")
        choice = input("> ").strip()
        if choice == "4":
            return
        action = actions.get(choice)
        if action:
            action(conn)
        else:
            print("Invalid choice.")


# --- Customer actions ------------------------------------------------------

def customer_browse(conn):
    print("\nAvailable products:")
    for row in conn.execute(
        "SELECT product_id, name, price, quantity_in_stock FROM Product "
        "WHERE quantity_in_stock > 0 ORDER BY product_id"
    ):
        print(f"  [{row[0]}] {row[1]:<28} ${row[2]:>8.2f}  in stock: {row[3]}")


def customer_add_card(conn, customer_id):
    last4 = input("Card last 4 digits: ").strip()
    expiry = input("Expiry (YYYY-MM): ").strip()
    zip_code = input("Billing zip: ").strip()
    conn.execute(
        "INSERT INTO CreditCard (customer_id, card_last4, expiry, billing_zip) "
        "VALUES (?, ?, ?, ?)",
        (customer_id, last4, expiry, zip_code),
    )
    conn.commit()
    print("Card added.")


def customer_purchase(conn, customer_id):
    customer_browse(conn)
    product_id = prompt_int("\nproduct_id to buy: ")
    product = conn.execute(
        "SELECT name, price, quantity_in_stock FROM Product WHERE product_id = ?",
        (product_id,),
    ).fetchone()
    if product is None:
        print("No such product.")
        return

    cards = conn.execute(
        "SELECT card_id, card_last4 FROM CreditCard WHERE customer_id = ?",
        (customer_id,),
    ).fetchall()
    if not cards:
        print("You have no cards on file. Add one first.")
        return
    print("Your cards:")
    for card_id, last4 in cards:
        print(f"  {card_id}: ending in {last4}")
    card_id = prompt_int("card_id to use: ")
    if card_id not in [c[0] for c in cards]:
        print("That card isn't on your account.")
        return

    qty = prompt_int("Quantity: ")
    if qty > product[2]:
        print(f"Only {product[2]} in stock — cannot fulfill that quantity.")
        return

    today = datetime.date.today().isoformat()
    conn.execute(
        "INSERT INTO Purchase (customer_id, product_id, card_id, quantity, purchase_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (customer_id, product_id, card_id, qty, today),
    )
    conn.execute(
        "UPDATE Product SET quantity_in_stock = quantity_in_stock - ? WHERE product_id = ?",
        (qty, product_id),
    )
    conn.commit()
    print(f"Purchased {qty} x {product[0]} for ${qty * product[1]:.2f}.")


def customer_menu(conn):
    print("\nCustomers on file:")
    for row in conn.execute("SELECT customer_id, name FROM Customer"):
        print(f"  {row[0]}: {row[1]}")
    customer_id = prompt_int("Your customer_id: ")
    while True:
        print("\n-- Customer Menu --")
        print("1) Browse products\n2) Add credit card\n3) Purchase a product\n4) Back")
        choice = input("> ").strip()
        if choice == "1":
            customer_browse(conn)
        elif choice == "2":
            customer_add_card(conn, customer_id)
        elif choice == "3":
            customer_purchase(conn, customer_id)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")


def main():
    conn = get_connection()
    try:
        while True:
            print("\n=== E-Commerce Backend ===")
            print("1) Staff\n2) Customer\n3) Quit")
            choice = input("> ").strip()
            if choice == "1":
                staff_menu(conn)
            elif choice == "2":
                customer_menu(conn)
            elif choice == "3":
                break
            else:
                print("Invalid choice.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
