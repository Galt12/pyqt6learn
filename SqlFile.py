
import sqlite3


from PyQt6.QtSql import QSqlDatabase, QSqlQuery



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
        "INSERT INTO users (name, password, id_buro, role) VALUES (?,?,?,'user')",
        (user_info),
    )
    conn.commit()
    conn.close()


def fetch_user_id(name):
    """Получение id пользователя"""
    with sqlite3.connect("table.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE name = ?", (name,))
        result = cur.fetchone()
    return result[0] if result else None


def fetch_orders_for_user_between_dates(user_id, start_date, end_date):
    """Получаем значения из таблицы работ, с учетом id и диапазона дат"""
    with sqlite3.connect("table.db") as conn:
        cur = conn.cursor()
        results = cur.execute(
            """
            SELECT zakaz, izdelie, lz_izv, number_lz, kol_list
            FROM orders
            WHERE orders.id_user = ?
            AND orders.date BETWEEN ? AND ?
        """,
            (user_id, start_date, end_date),
        )
        rows = list(results)
    return rows

def fetch_orders_for_monts(start_date, end_date):
    """Получаем значения из таблицы работ, с учетом id и диапазона дат"""
    with sqlite3.connect("table.db") as conn:
        cur = conn.cursor()
        results = cur.execute(
            """
            SELECT zakaz, izdelie, sum(kol_list)
            FROM orders
            WHERE orders.date BETWEEN ? AND ?
        """,
            (start_date, end_date),
        )
        rows = list(results)
    return rows




def fetch_sum_trudoemkost_for_user(user_id, start_date, end_date):
    with sqlite3.connect("table.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT SUM(kol_list) FROM orders WHERE id_user = ? AND orders.date BETWEEN ? AND ? ",
            (user_id, start_date, end_date),
        )
        result = cur.fetchone()
    return result[0]


def check_buro():
    list_buro = []
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("table.db")
    if not db.open():
        print("Не удалось открыть базу данных")
        return list_buro

    query = QSqlQuery()
    query.prepare("SELECT DISTINCT name_buro FROM buro")
    if not query.exec():
        print("Ошибка выполнения запроса")
        return list_buro

    while query.next():
        name_buro = query.value(0)
        list_buro.append(name_buro)
    db.close()

    return list_buro



def new_value():
    with sqlite3.connect("table.db") as conn:
        cur = conn.cursor()
        cur.execute("""
        UPDATE orders
        JOIN izdelia_zakaz ON orders.zakaz = izdelia_zakaz.zakaz_izdelie
        SET orders.izdelie = izdelia_zakaz.name_izdelie""",)
                    
        conn.commit()
        conn.close()

