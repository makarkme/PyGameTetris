import sqlite3


class Records:
    def __init__(self, record, point):
        self.record = record
        self.point = point
        self.none = None

    # Рекорд пользователя
    def record(self):
        self.none = None
        with open('record') as f:
            return f.readline()

    # Обновление рекорда пользователя
    def next_record(self):
        rec = max(int(self.record), self.point)
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        cur.execute("""UPDATE PT_Entry SET record = 100 WHERE login = 'asd'""")
        con.commit()