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
    c.execute("SELECT price FROM items WHERE id = ?", (item_id,))
    price = c.fetchone()[0]
    c.execute("SELECT name FROM items WHERE id = ?", (item_id,))
    name = c.fetchone()[0]
    c.execute("INSERT INTO orders (item_name, quantity, total_value) VALUES (?, ?, ?)",
              (name, quantity, calculate_amount(price, quantity)))
    conn.commit()

def finish_order():
    c.execute("BEGIN")
    c.execute('''INSERT INTO orders_history (date, items, total)
              SELECT ?, group_concat(item_name), sum(total_value) FROM orders''',
              (datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),))
    c.execute ('DELETE FROM orders')
    conn.commit()