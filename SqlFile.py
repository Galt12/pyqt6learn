import sqlite3


def create_table_user():
    conn = sqlite3.connect("table.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password INTEGER,
        id_buro INTEGER REFERENCES buro (id)
    )"""
    )
    conn.commit()
    conn.close()


def create_table_buro():
    conn = sqlite3.connect("table.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS buro (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name_buro TEXT
              )"""
    )
    conn.commit()
    conn.close()


def insert_user(name, password, id_buro):
    conn = sqlite3.connect("table.db")
    c = conn.cursor()
    c.execute(
        """INSERT INTO users (name, password, id_buro) VALUES (?,?,?)""",
        (name, password, id_buro),
    )
    conn.commit()
    conn.close()


def insert_buro(name_buro):
    conn = sqlite3.connect("table.db")
    c = conn.cursor()
    c.execute("""INSERT INTO buro (name_buro) VALUES (?)""", (name_buro,))
    conn.commit()
    conn.close()


def add_items(value):
    conn = sqlite3.connect("table.db")
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO orders (
            zakaz, izdelie, lz_izv, number_lz, kol_list, id_user, date, id_works)
            VALUES (?,?,?,?,?,?,?,?)""",
        value,
    )
    conn.commit()
    conn.close()


def add_user(user_info):
    conn = sqlite3.connect("table.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, password, id_buro) VALUES (?,?,?)",
        (user_info),
    )
    conn.commit()
    conn.close()


def add_date():
    conn = sqlite3.connect("table.db")
    cur = conn.cursor()
    cur.execute(
        """ALTER TABLE orders
        ADD COLUMN  date DATE;"""
    )

    conn.commit()
    conn.close()


def info():
    conn = sqlite3.connect("table.db")
    cur = conn.cursor()
    cur.execute(
        """SELECT DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'orders' AND COLUMN_NAME = 'date'"""
    )

    conn.commit()
    conn.close()

