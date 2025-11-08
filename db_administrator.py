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

#FUNCTIONS TO MANIPULATE ORDERS
def new_order(item_id, quantity):
    if quantity <= 0:
        raise ValueError("The amount of items must be positive")
    c.execute("SELECT name, price FROM items WHERE id = ?", (item_id,))
    row = c.fetchone()
    if row is None:
        raise ValueError("Item not found")

    name, price = row
    total = calculate_amount(price, quantity)
    with conn:
        c.execute("INSERT INTO orders (item_name, quantity, total_value) "
                  "VALUES (?, ?, ?)",
                  (name, quantity, total))


def finish_order():
    try:
        with conn:
            c.execute('''INSERT INTO orders_history (date, items, total)
                      SELECT ?, group_concat(item_name), sum(total_value) FROM orders''',
                      (datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),))
            c.execute ('DELETE FROM orders')
    except _sqlite3.Error as e:
        print(f"Error to finish the purchase: {e}")