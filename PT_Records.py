import sqlite3


class Records:
    def __init__(self, record, point):
        self.record = record
        self.point = point

    # The user's existing record. Accessing the database.
    def user_record(self):
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        file_login = open('login.txt', 'r')
        login = file_login.read()
        record_bd = cur.execute(f"""SELECT record FROM PT_Entry WHERE login = ?""", (login,)).fetchone()
        con.close()
        file_login.close()
        return record_bd[0]

    # Record the user's record.
    def next_record(self):
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        file_login = open('login.txt', 'r')
        login = file_login.read()
        self.record = cur.execute("""SELECT record FROM PT_Entry WHERE login = ?""", (login,)).fetchone()
        self.record = self.record[0]
        rec = max(int(self.record), self.point)
        cur.execute("""UPDATE PT_Entry SET record = ? WHERE login = ?""", (rec, login))
        con.commit()
        con.close()
        file_login.close()
