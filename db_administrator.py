#This file is going to have the administrator for the databank
import _sqlite3
import datetime

conn = _sqlite3.connect('cafe_data.db')
c = conn.cursor()

#FUNCTIONS TO EDIT THE MENU
def insert_item(name, price, category):
    c.execute("INSERT INTO items (name, price, category) VALUES (?, ?, ?)",
              (name, price, category))
    conn.commit()

def edit_price(new_price, name):
    c.execute("UPDATE items set price = ? WHERE name = ?",
              (new_price, name))
    conn.commit()

def delete_item(name):
    c.execute("DELETE FROM items WHERE name = ?" ,
              (name,))
    conn.commit()

#FUNCTIONS TO CALCULATE
def calculate_amount(item, quantity):
    return int(item * quantity)

def start_order(table_number):
    c.execute("SELECT id FROM orders WHERE table_number = ? AND status = 'open'", (table_number,))
    row = c.fetchone()
    if row:
        return row[0]  #there is already an opened order on this table

    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with conn:
        c.execute("INSERT INTO orders (date, table_number) VALUES (?, ?)", (now, table_number))
        return c.lastrowid

#FUNCTIONS TO MANIPULATE ORDERS
def add_order_item(table_number, item_id, quantity):
    if quantity <= 0:
        raise ValueError("The amount of items must be positive")

    order_id = start_order(table_number)

    c.execute("SELECT name, price FROM items WHERE id = ?", (item_id,))
    row = c.fetchone()
    if row is None:
        raise ValueError("Item not found")

    name, price = row
    total = calculate_amount(price, quantity)
    with conn:
        c.execute("INSERT INTO order_items (order_id, item_name, quantity, total_value) "
                  "VALUES (?, ?, ?, ?)",
                  (order_id, name, quantity, total))

def finish_order(table_number):

    c.execute("SELECT id FROM orders WHERE table_number = ? AND status = 'open'", (table_number, ))
    row = c.fetchone()
    if not row:
        raise ValueError("No opened orders on this table")
    order_id = row[0]

    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    c.execute("""
        SELECT group_concat(item_name, ', '), sum(total_value)
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))
    items, total = c.fetchone()

    with conn:
        c.execute("""
                    INSERT INTO orders_history (date, items, total, table_number)
                    VALUES (?, ?, ?, ?)
                """, (now, items, total, table_number))
        c.execute("UPDATE orders SET status = 'closed' WHERE id = ?", (order_id,))
        c.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        print(f"The order of the table {table_number} was finished. Total: €{total:.2f}")
        return total

def get_open_tables():
    c.execute("SELECT id, table_number, date FROM orders WHERE status = 'open'")
    return [row[0] for row in c.fetchall()]

def statistics():
    c.execute(""" SELECT""")

def delete_data():
    with conn:
        c.execute("DELETE FROM items")
        c.execute("DELETE FROM orders")
        c.execute("DELETE FROM order_items")
        c.execute("DELETE FROM orders_history")