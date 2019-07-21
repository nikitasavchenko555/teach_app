import sqlite3
from logging import basicConfig, error, info
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.uix.modalview import ModalView
import kivy.uix.textinput

import conf_rep


def sql_connection_check():
    # проверяем наличие бд, если нет, создаем
    try:
        conn: Connection = sqlite3.connect('rep.db')
        info("Соединение с БД успешно установлено")
    except:
        error("Возникла ошибка. Создаем новую базу")
    finally:
        conn.close()


def sql_table():
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        cursor_table.execute("select * from list_lessons")
    except:
        cursor_table.execute(
            "create table list_lessons (id integer PRIMARY KEY, themas text, house_ex text, date_lessons text, check_salary numeric)")
        conn.commit()


class MyLayout():
    pass




class RepCheckAppBoxLayout(BoxLayout):
    info("Главный виджет")
    def child_save(self):
        Logger.info('Запускаем окно для добавления записи')
        view = ViewAddEvent()
        view.open()

class ViewAddEvent(ModalView):
    def close_child(self):
        Logger.info('Закрываем окно для добавления записи')
        self.dismiss()

class RepCheckApp(kivy.app.App):
    def build(self):
        # info("пробум запуск главного виджета")
        return RepCheckAppBoxLayout()


if __name__ == '__main__':
    basicConfig(filename="reper.txt", level=conf_rep.log_level)
    info("Файл логов начат")
    sql_connection_check()
    sql_table()
    RepCheckApp().run()
