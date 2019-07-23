import sqlite3
from datetime import datetime
from logging import basicConfig, error, info
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.uix.modalview import ModalView
import kivy.uix.textinput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
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
            "name text, themas text, date_lessons text, salary numeric, check_state real, check_salary real)")


def sql_table_insert(username, Unit, Cost, date, hour, check_state, check_salary):
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        Logger.info('час: {}'.format(hour))
        date_str = "{} {}".format(date, hour)
        Logger.info("полученная дата: {}".format(date_str))
        cur_insert = """insert into list_lessons (name, themas, date_lessons,salary, check_state, check_salary )
         values ('{0}', '{1}', '{2}', '{3}', {4}, {5})""".format(username, Unit, date_str, Cost, check_state, check_salary)
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

    def add_record(self, username, Unit, Cost, date, hour, check_state, check_salary):
        Logger.info('добавляем атрибуты')
        str_log = "Получены атрибуты: {}, '{}', {}, {}, {}, {}, {}".format(username, Unit, Cost, date, hour, check_state, check_salary)
        Logger.info(str_log)
        if check_state:
            check_state = 1
        else:
            check_state = 0
        if check_salary:
            check_salary = 1
        else:
            check_salary = 0
        if sql_table_insert(username, Unit, Cost, date, hour, check_state, check_salary):
            content = Button(text='закрыть окно')
            popup = Popup(title='Запись добавлена', content=content)
            content.bind(on_press=popup.dismiss)
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
