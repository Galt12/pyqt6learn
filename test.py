import sqlite3

def add_date():
    conn = sqlite3.connect("table.db")
    cur = conn.cursor()
    cur.execute(
        """SELECT date 
        FROM orders
        """
    )

    conn.commit()
    conn.close()