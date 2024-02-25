import sqlite3
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def check_buro():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("table.db")
    if not db.open():
        print("Не удалось открыть базу данных")
        return

    query = QSqlQuery()
    query.prepare("SELECT DISTINCT name_buro FROM buro")
    if not query.exec():
        print("Ошибка выполнения запроса")
        return

    while query.next():
        name_buro = query.value(0)
        print(name_buro)
    #     self.list_buro.addItem(name_buro)

    db.close()

    print(name_buro)


check_buro()
