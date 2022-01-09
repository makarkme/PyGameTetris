import wx
from PyGameTetris import main
from threading import Thread
import sqlite3


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, title=title, parent=parent, size=(550, 660))

        self.game, self.menu, self.button_game_start, self.button_statistics = None, None, None, None
        self.button_rules = None
        self.quit = False

        self.login = wx.Panel(self, size=self.GetSize())
        self.text_1 = wx.StaticText(self.login, label="Введите логин и пароль", pos=(200, 170))
        self.text_1.Fit()
        self.text_2 = wx.StaticText(self.login, label="Логин: ", pos=(60, 200))
        self.text_2.Fit()
        self.text_3 = wx.StaticText(self.login, label="Пароль: ", pos=(60, 232))
        self.text_3.Fit()

        self.name = wx.TextCtrl(self.login, size=(300, 20), pos=(120, 200))
        self.password = wx.TextCtrl(self.login, size=(300, 20), pos=(120, 230))

        self.button_login = wx.Button(self.login, label="Войти", size=(300, 50), pos=(120, 270))
        self.button_login.Bind(wx.EVT_BUTTON, self.login_)

    def login_(self, event):
        login = []
        password = []
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        fetch = cur.execute("""SELECT * FROM PT_Entry""").fetchall()
        for elem in fetch:
            login.append(str(elem[1]))
            password.append(str(elem[2]))
        if self.name.GetValue() not in login:
            cur.execute(f"""INSERT INTO PT_Entry(login, password) VALUES \
             ('{self.name.GetValue()}', '{self.password.GetValue()}')""")
            con.commit()
            self.login.Hide()
            self.menu_()
        elif self.name.GetValue() in login:
            num_name = login.index(self.name.GetValue())
            if self.password.GetValue() != password[num_name]:
                print(login)
                print(password)
                self.text_4 = wx.StaticText(self.login, label="Неверный пароль", pos=(220, 350))
                self.text_4.Fit()
            else:
                self.login.Hide()
                self.menu_()

    def menu_(self):
        self.menu = wx.Panel(self, size=self.GetSize())
        self.button_game_start = wx.Button(self.menu, label="Начать игру", size=(100, 50), pos=(220, 170))
        self.button_statistics = wx.Button(self.menu, label="Cтатистика", size=(100, 50), pos=(220, 270))
        self.button_rules = wx.Button(self.menu, label="Правила", size=(100, 50), pos=(220, 370))

        self.button_game_start.Bind(wx.EVT_BUTTON, self.game_start)
        self.button_statistics.Bind(wx.EVT_BUTTON, self.statistics)
        self.button_rules.Bind(wx.EVT_BUTTON, self.rules)

    def game_start(self, event):
        self.game = Thread(target=main, args=(self.quit,))
        self.game.start()
        self.game.join()
        if not self.game.is_alive():
            self.quit = True

    def statistics(self, event):
        pass

    def rules(self, event):
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow(None, "PyGameTetris")
    frame.Show()
    app.MainLoop()
