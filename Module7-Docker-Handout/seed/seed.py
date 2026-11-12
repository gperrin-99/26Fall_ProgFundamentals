import sqlite3
import random
random.seed(42)
conn = sqlite3.connect("/data/sales.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS sales")
cur.execute("CREATE TABLE sales (id INTEGER PRIMARY KEY, month TEXT, product TEXT,
units INTEGER, price REAL)")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
"Nov", "Dec"]
products = {"Laptop": 999.0, "Phone": 699.0, "Tablet": 449.0}
rows = []
for month in months:
    for product, price in products.items():
        units = random.randint(20, 120)
        rows.append((month, product, units, price))

cur.executemany("INSERT INTO sales (month, product, units, price) VALUES (?, ?, ?,?)", rows)
conn.commit()
conn.close()
print(f"Created sales.db with {len(rows)} rows")