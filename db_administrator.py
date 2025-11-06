#This file is going to have the administrator for the databank
import _sqlite3

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
    return item * quantity

#FUNCTIONS TO MANIPULATE ORDERS
def new_order(item_id, quantity, total_value):
    c.execute("INSERT INTO orders (id, item_id, quantity, total_value), VALUES (?, ?, ?, ?)",
              (item_id, quantity, total_value))
    conn.commit()