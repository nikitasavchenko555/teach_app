import sqlite3
from datetime import datetime
from logging import basicConfig, error, info
import kivy.app
from kivy.uix.boxlayout import BoxLayout
import kivy.uix.label
from kivy.logger import Logger
from kivy.uix.modalview import ModalView
import kivy.uix.textinput
from kivy.uix.popup import Popup
import kivy.uix.button
import re

import conf_rep
import datepicker


def sql_connection_check():
    # проверяем наличие бд, если нет, создаем
    try:
        conn: Connection = sqlite3.connect('rep.db')
        info("Соединение с БД успешно установлено")
    except:
        error("Возникла ошибка. Создаем новую базу")
    finally:
        conn.close()


def sql_table_select():
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        cur_select = cursor_table.execute("select * from list_lessons")
        return cur_select
    except:
        cursor_table.execute(
            "create table list_lessons (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "name text, themas text, date_lessons text, salary numeric, check_salary numeric)")

def sql_table_insert(username,Unit, Cost, date, hour):
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        hour_1 = re.sub(r'\]', ':', str(hour))
        Logger.info('час: {}'.format(hour_1))
        date_str = datetime.combine(date, hour)
        Logger.info(date_str)
        date_str_1 = date_str.strftime("%d/%m/%y %H:%M")
        cur_insert = "insert into list_lessons values ({}, {}, {}, {}, {}, null)".format(username, str(Unit), date_str_1, Cost)
        Logger.info(cur_insert)
        cur_insert_result = cursor_table.execute(cur_insert)
        return cur_insert_result
    except Exception as e:
        Logger.error(str(e))


class MyLayout():
    pass




class RepCheckAppBoxLayout(BoxLayout):
    info("Главный виджет")
    def child_save(self):
        Logger.info('Запускаем окно для добавления записи')
        view = ViewAddEvent(size_hint=(1, 1))
        view.open()

class ViewAddEvent(ModalView):
    def close_child(self):
        Logger.info('Закрываем окно для добавления записи')
        self.dismiss()
    def add_record(self, username,Unit, Cost, date, hour):
        Logger.info('добавляем атрибуты')
        str_log = "Получены атрибуты: {}, '{}', {}, {}, {}".format(username,Unit, Cost, date, str(hour))
        Logger.info(str_log)
        if sql_table_insert(username,Unit, Cost, date, str(hour)):
            popup = Popup(title='Запись добавлена',
                          content=kivy.Button(text='закрыть окно'))
            popup.open()


class SchedulerView(ModalView):
    pass


class RepCheckApp(kivy.app.App):
    def build(self):
        # info("пробум запуск главного виджета")
        return RepCheckAppBoxLayout()


if __name__ == '__main__':
    basicConfig(filename="reper.txt", level=conf_rep.log_level)
    info("Файл логов начат")
    sql_connection_check()
    sql_table_select()
    RepCheckApp().run()
