import wx  # The same as PyQt, only better.
from PyGameTetris import main
from threading import Thread
import sqlite3


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        # Setting variables + arguments.
        wx.Frame.__init__(self, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
            wx.CLOSE_BOX | wx.CLIP_CHILDREN, title=title, parent=parent, size=(550, 660))

        self.game, self.menu, self.button_game_start, self.button_statistics, self.statistics, self.text_4, \
            self.text_5, self.text_6, self.button_back_s, self.text_7, self.rules, self.button_back_r, \
            self.button_rules, self.button_rules, self.quit, self.name, self.record, \
            self.num_name = None, None, None, None, None, None, None, None, None, None, None, None, None, \
            None, None, None, None, None

        self.login = wx.Panel(self, size=self.GetSize())  # The first window is the account login.

        self.font_1 = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.font_2 = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.font_3 = wx.Font(13, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)

        self.text_1 = wx.StaticText(self.login, label="Введите логин и пароль",
                                    size=(300, 50), pos=(120, 130), style=wx.ALIGN_CENTER)
        self.text_1.SetForegroundColour((14, 41, 75))
        self.text_1.SetFont(self.font_1)
        self.text_1.Fit()
        self.text_2 = wx.StaticText(self.login, label="Логин: ", pos=(60, 200), size=(50, 20), style=wx.ALIGN_CENTER)
        self.text_2.SetForegroundColour((14, 41, 75))
        self.text_2.SetFont(self.font_2)
        self.text_2.Fit()
        self.text_3 = wx.StaticText(self.login, label="Пароль: ", pos=(60, 235), size=(50, 20), style=wx.ALIGN_CENTER)
        self.text_3.SetForegroundColour((14, 41, 75))
        self.text_3.SetFont(self.font_2)
        self.text_3.Fit()

        self.name = wx.TextCtrl(self.login, size=(300, 30), pos=(120, 200))
        self.password = wx.TextCtrl(self.login, size=(300, 30), pos=(120, 235))

        self.button_login = wx.Button(self.login, label="Войти", size=(300, 50), pos=(120, 285))
        self.button_login.SetForegroundColour((14, 41, 75))
        self.button_login.SetFont(self.font_1)
        self.button_login.Bind(wx.EVT_BUTTON, self.login_)

        self.login.Bind(wx.EVT_ERASE_BACKGROUND, self.background)  # Setting the background.

    def background(self, evt):  # Loading the background + setting the priority on the screen.
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        bmp = wx.Bitmap("data/background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def login_(self, event):  # Working with the database.
        login = list()
        password = list()
        rec = list()
        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        fetch = cur.execute("""SELECT * FROM PT_Entry""").fetchall()
        for elem in fetch:
            login.append(str(elem[1]))
            password.append(str(elem[2]))
            rec.append(str(elem[3]))
        if self.name.GetValue() not in login and self.name.GetValue() != "" and self.password.GetValue() != "":
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
                file_login = open("login.txt", "w")  # Writing the username to a txt file.
                file_login.write(self.name.GetValue())
                file_login.close()
                self.record = rec[self.num_name]
                self.login.Hide()
                self.menu_()

    def menu_(self):  # The main window. From this you can get into the statistics, rules and game window.
        self.menu = wx.Panel(self, size=self.GetSize())
        self.menu.Bind(wx.EVT_ERASE_BACKGROUND, self.background)
        self.menu.Hide()
        self.menu.Show()
        self.menu.Bind(wx.EVT_ERASE_BACKGROUND, self.background)
        self.button_game_start = wx.Button(self.menu, label="Начать игру", size=(300, 50), pos=(120, 170))
        self.button_game_start.SetForegroundColour((14, 41, 75))
        self.button_game_start.SetFont(self.font_1)
        self.button_statistics = wx.Button(self.menu, label="Cтатистика", size=(300, 50), pos=(120, 270))
        self.button_statistics.SetForegroundColour((14, 41, 75))
        self.button_statistics.SetFont(self.font_1)
        self.button_rules = wx.Button(self.menu, label="Правила", size=(300, 50), pos=(120, 370))
        self.button_rules.SetForegroundColour((14, 41, 75))
        self.button_rules.SetFont(self.font_1)

        self.button_game_start.Bind(wx.EVT_BUTTON, self.game_start_)
        self.button_statistics.Bind(wx.EVT_BUTTON, self.statistics_)
        self.button_rules.Bind(wx.EVT_BUTTON, self.rules_)

    def game_start_(self, event):  # Launching Tetris.
        self.Hide()
        self.game = Thread(target=main, args=(self.quit,))
        self.game.start()
        self.game.join()
        self.quit = True
        self.Show()

    def statistics_(self, event):
        self.menu.Hide()
        self.statistics = wx.Panel(self, size=self.GetSize())
        self.statistics.Bind(wx.EVT_ERASE_BACKGROUND, self.background)

        con = sqlite3.connect("PyGameTetris_db.sqlite")
        cur = con.cursor()
        file_login = open('login.txt', 'r')
        login = file_login.read()
        self.record = cur.execute("""SELECT record FROM PT_Entry WHERE login = ?""", (login,)).fetchone()
        self.record = self.record[0]

        self.text_5 = wx.StaticText(self.statistics, label="Ваш игровой рекорд: ",
                                    size=(300, 50), pos=(120, 130), style=wx.ALIGN_CENTER)
        self.text_5.SetForegroundColour((14, 41, 75))
        self.text_5.SetFont(self.font_1)
        self.text_5.Fit()
        self.text_6 = wx.StaticText(self.statistics, label=f"{self.record}",
                                    size=(300, 50), pos=(120, 200), style=wx.ALIGN_CENTER)
        self.text_6.SetForegroundColour((14, 41, 75))
        self.text_6.SetFont(self.font_1)
        self.text_6.Fit()

        self.button_back_s = wx.Button(self.statistics, label="Вернуться", size=(300, 50), pos=(120, 500))
        self.button_back_s.SetForegroundColour((14, 41, 75))
        self.button_back_s.SetFont(self.font_1)
        self.button_back_s.Bind(wx.EVT_BUTTON, lambda a: self.back_(a, "s"))

    def back_(self, event, type_):  # A function that allows you to get back to the main menu.
        if type_ == "s":
            self.statistics.Hide()
        if type_ == "r":
            self.rules.Hide()
        self.menu.Show()

    def rules_(self, event):  # A window with rules.
        self.menu.Hide()
        self.rules = wx.Panel(self, size=self.GetSize())
        self.rules.Bind(wx.EVT_ERASE_BACKGROUND, self.background)

        self.text_7 = wx.StaticText(self.rules, label="Случайные фигурки тетрамино падают сверху в прямоугольный "
                                                      "стакан шириной 10 \n и высотой 20 клеток. В полёте игрок может "
                                                      "поворачивать фигурку на 90° и двигать её \n по горизонтали. "
                                                      "Также можно «сбрасывать» фигурку, то есть ускорять её падение.\n"
                                                      "Фигурка летит до тех пор, пока не наткнётся на другую фигурку, "
                                                      "либо на дно стакана. \n Если при этом заполнился горизонтальный "
                                                      "ряд из 10 клеток, он пропадает и всё,\n что выше него, "
                                                      "опускается "
                                                      "на одну клетку. Дополнительно показывается фигурка, \n которая "
                                                      "будет следовать после текущей — это подсказка, которая "
                                                      "позволяет игроку \n планировать действия. Темп игры постепенно "
                                                      "ускоряется. Игра заканчивается,\nкогда игрок пройдёт 5 уровней. "
                                                      "Игрок получает очки за каждый заполненный "
                                                      "ряд, \n поэтому его задача — заполнять ряды, не заполняя сам "
                                                      "стакан (по вертикали) \n как можно дольше, чтобы таким образом "
                                                      "получить как можно больше очков.", pos=(25, 50), size=(485, 400))
        self.text_7.SetForegroundColour((14, 41, 75))
        self.text_7.SetFont(self.font_3)
        self.text_7.Fit()

        self.button_back_r = wx.Button(self.rules, label="Вернуться", size=(300, 50), pos=(120, 500))
        self.button_back_r.SetForegroundColour((14, 41, 75))
        self.button_back_r.SetFont(self.font_1)
        self.button_back_r.Bind(wx.EVT_BUTTON, lambda a: self.back_(a, "r"))


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow(None, "PyGameTetris")
    frame.Show()
    app.MainLoop()
