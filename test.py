import sqlite3

def user_name_list():
        con = sqlite3.connect('table.db')
        cur = con.cursor()
        x = cur.execute('''SELECT name FROM users''',)
        y = x.fetchall()
        print(y)
        con.commit()
        con.close()


user_name_list()