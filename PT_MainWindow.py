import wx
from PyGameTetris import main
from threading import Thread
import sqlite3


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                                      wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title=title, parent=parent, size=(550, 660))

        self.game, self.menu, self.button_game_start, self.button_statistics = None, None, None, None
        self.statistics, self.text_4, self.text_5, self.text_6, self.button_back_s = None, None, None, None, None
        self.text_7, self.rules, self.button_back_r = None, None, None
        self.button_rules = None
        self.quit = False
        self.name = None
        self.record, self.num_name = None, None

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

        self.login.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        bmp = wx.Bitmap("data/background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def login_(self, event):
        login = []
        password = []
        rec = []
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        fetch = cur.execute("""SELECT * FROM PT_Entry""").fetchall()
        for elem in fetch:
            login.append(str(elem[1]))
            password.append(str(elem[2]))
            rec.append(str(elem[3]))
        if self.name.GetValue() not in login:
            cur.execute(f"""INSERT INTO PT_Entry(login, password) VALUES \
                 ('{self.name.GetValue()}', '{self.password.GetValue()}')""")
            con.commit()
            con.close()
            file_login = open("login.txt", "w")
            file_login.write(self.name.GetValue())
            file_login.close()
            self.record = 0
            self.login.Hide()
            self.menu_()
        elif self.name.GetValue() in login:
            self.num_name = login.index(self.name.GetValue())
            if self.password.GetValue() != password[self.num_name]:
                self.text_4 = wx.StaticText(self.login, label="Неверный пароль", pos=(220, 350))
                self.text_4.Fit()
            else:
                file_login = open("login.txt", "w")
                file_login.write(self.name.GetValue())
                file_login.close()
                self.record = rec[self.num_name]
                self.login.Hide()
                self.menu_()

    def menu_(self):
        self.menu = wx.Panel(self, size=self.GetSize())
        self.menu.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.menu.Hide()
        self.menu.Show()
        self.menu.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.button_game_start = wx.Button(self.menu, label="Начать игру", size=(100, 50), pos=(220, 170))
        self.button_statistics = wx.Button(self.menu, label="Cтатистика", size=(100, 50), pos=(220, 270))
        self.button_rules = wx.Button(self.menu, label="Правила", size=(100, 50), pos=(220, 370))

        self.button_game_start.Bind(wx.EVT_BUTTON, self.game_start_)
        self.button_statistics.Bind(wx.EVT_BUTTON, self.statistics_)
        self.button_rules.Bind(wx.EVT_BUTTON, self.rules_)

    def game_start_(self, event):
        self.Hide()
        self.game = Thread(target=main, args=(self.quit,))
        self.game.start()
        self.game.join()
        self.quit = True
        self.Show()

    def statistics_(self, event):
        self.menu.Hide()
        self.statistics = wx.Panel(self, size=self.GetSize())
        self.statistics.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.text_5 = wx.StaticText(self.statistics, label="Ваш игровой рекорд: ", pos=(200, 170))
        self.text_5.Fit()
        self.text_6 = wx.StaticText(self.statistics, label=f"{self.record}",
                                    pos=(230, 190))
        self.text_6.Fit()

        self.button_back_s = wx.Button(self.statistics, label="Вернуться", size=(100, 50), pos=(220, 370))
        self.button_back_s.Bind(wx.EVT_BUTTON, lambda a: self.back_(a, "s"))

    def back_(self, event, type_):
        if type_ == "s":
            self.statistics.Hide()
        if type_ == "r":
            self.rules.Hide()
        self.menu.Show()

    def rules_(self, event):
        self.menu.Hide()
        self.rules = wx.Panel(self, size=self.GetSize())
        self.rules.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.text_7 = wx.StaticText(self.rules, label="kfsdhkdfgfd ", pos=(200, 170))
        self.text_7.Fit()

        self.button_back_r = wx.Button(self.rules, label="Вернуться", size=(100, 50), pos=(220, 370))
        self.button_back_r.Bind(wx.EVT_BUTTON, lambda a: self.back_(a, "r"))


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow(None, "PyGameTetris")
    frame.Show()
    app.MainLoop()
