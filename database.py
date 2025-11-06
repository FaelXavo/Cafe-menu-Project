import _sqlite3
from db_administrator import *

# items: id, name, price, category
# orders: id, item_id, quantity, total_value
# history: id, date, items, total
# statistics: date, daily_total, monthly_total

conn = _sqlite3.connect('cafe_data.db')

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        category TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        item_name TEXT,
        quantity INTEGER,
        total_value INTEGER
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS orders_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date TEXT,
        items TEXT,
        total INTEGER
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY NOT NULL,
    quantity INTEGER,
    total INTEGER,
    month_total INTEGER
    )
''')

#testing area --------------------------
name = 'test5'
price = 2
category = 'drink'

#new_order(4, 2)
#insert_item(name, price, category)
#edit_price(new_price = 10000, name = name)
#delete_item(name)
