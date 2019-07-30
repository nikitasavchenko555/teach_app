import sqlite3
from logging import basicConfig, error, info
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
import kivy.uix.textinput
from kivy.uix.popup import Popup
from kivy.uix.button import Button

import conf_rep
import datepicker


def sql_connection_check():
    # проверяем наличие бд, если нет, создаем
    try:
        conn = sqlite3.connect('rep.db')
        info("Соединение с БД успешно установлено")
    except:
        error("Возникла ошибка. Создаем новую базу")
    finally:
        conn.close()


# функци для получения всего списка уроков
def sql_table_select():
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        cur_select = cursor_table.execute("select * from list_lessons")
        return cur_select
    except FileNotFoundError:
        cursor_table.execute(
            "create table list_lessons (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "name text, themas text, date_lessons text, salary numeric, check_state numeric, check_salary numeric)")


# функция для получения статистики

def sql_table_select_stat(name=None):
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    if name:
        Logger.info("Тянем стату по ученику {}")
        select_stat = """select l.date_lessons, l.check_state, l.check_salary from list_lessons l
        where l.name = '{}'""".format(name)
        Logger.info("Запрос {}".format(select_stat))
    else:
        select_stat = 'select DISTINCT l.name from list_lessons l'
    try:
        cur_select = cursor_table.execute(select_stat)
        return cur_select
    except Exception as err:
        Logger.info('Возникла ошибка {}'.format(err.args))


def sql_table_insert(username, Unit, Cost, date, hour, check_state, check_salary):
    conn = sqlite3.connect('rep.db')
    info("Соединение с БД успешно установлено")
    cursor_table = conn.cursor()
    try:
        Logger.info('час: {}'.format(hour))
        date_str = "{} {}".format(date, hour)
        Logger.info("полученная дата: {}".format(date_str))
        cur_insert = """insert into list_lessons (name, themas, date_lessons,salary, check_state, check_salary )
         values ('{0}', '{1}', '{2}', '{3}', {4}, {5})""".format(username, Unit, date_str, Cost, check_state,
                                                                 check_salary)
        Logger.info(cur_insert)
        cur_insert_result = cursor_table.execute(cur_insert)
        conn.commit()
        return cur_insert_result
    except Exception as e:
        Logger.error(str(e))


class MyLayout(BoxLayout):
    pass


class ViewUnit(ModalView):
    def close_child(self):
        Logger.info('Закрываем окно для добавления записи')
        self.dismiss()

    def update_child(self, dict_record):
        Logger.info('Открываем окно редактирования')
        Logger.info('Получены парамметры {}'.format(dict_record))
        self.ids.username.text = dict_record['name']
        self.ids.Unit.text = dict_record['unit']
        self.ids.Cost.text = str(dict_record['cost'])
        self.ids.date.text = str(dict_record['date'])
        if dict_record['check_state'] == 1:
            self.ids.unit_check_state.text = 'урок пройден'
            self.ids.unit_check_state.color = (255, 64, 64, 1)
        elif dict_record['check_state'] == 0:
            self.ids.unit_check_state.text = 'урок не пройден'
            self.ids.unit_check_state.color = [245, 7, 0, 1]
        if dict_record['check_salary'] == 1:
            self.ids.unit_check_salary.text = 'урок оплачен'
            self.ids.unit_check_salary.color = [255, 64, 64, 1]
        elif dict_record['check_salary'] == 0:
            self.ids.unit_check_salary.text = 'урок не оплачен'
            self.ids.unit_check_salary.color = [245, 7, 0, 1]

class ViewStat(ModalView):
    pass


class RepCheckAppBoxLayout(BoxLayout):
    info("Главный виджет")

    def child_save(self):
        Logger.info('Запускаем окно для добавления записи')
        view = ViewAddEvent(size_hint=(1, 1))
        view.open()

    def child_view(self):
        Logger.info('Запускаем окно для вывода расписания')
        view = SchedulerView(size_hint=(1, 1))
        view.open()
        view.view_shed()

    def stat_view_all(self):
        Logger.info('Запускаем окно для вывода cтатистики')
        view = StatView(size_hint=(1, 1))
        view.get_all_stat()
        view.open()


# окно для добавления новых уроков
class ViewAddEvent(ModalView):
    def close_child(self):
        Logger.info('Закрываем окно для добавления записи')
        self.dismiss()

    def add_record(self, username, Unit, Cost, date, hour, check_state, check_salary):
        Logger.info('добавляем атрибуты')
        str_log = "Получены атрибуты: {}, '{}', {}, {}, {}, {}, {}".format(username, Unit, Cost, date, hour,
                                                                           check_state, check_salary)
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
            popup = Popup(title='Запись изменена', content=content)
            content.bind(on_press=popup.dismiss)
            popup.open()


class ViewUpdateEvent(ModalView):
    pass


# окно расписания
class SchedulerView(ModalView):
    dict_shed = {}
    def close_child(self):
        Logger.info('Закрываем окно для добавления записи')
        self.dismiss()

    def view_shed(self, dict_shed={}):
        if sql_table_select():
            result_select = sql_table_select().fetchall()
            Logger.info('Получили значение {} и тип {}'.format(result_select, type(result_select)))
            tv = MyLayout(orientation='vertical')
            self.add_widget(tv)
            for result in result_select:
                Logger.info('Вошли в цикл')
                Logger.info('Получили значение {} и тип выгрузки {}'.format(result, type(result)))
                dict_shed = dict(id=result[0], name=result[1], unit=result[2], date=result[3], cost=result[4],
                                 check_state=result[5], check_salary=result[6])
                Logger.info("словарь {}".format(dict_shed))
                # self.ids.add(dict_shed['name'])
                button = Button(text=str(dict_shed['date'] + ' ' + dict_shed['name']), font_size=30)
                button.bind(on_press=lambda s: self.view_unit(dict_shed))
                tv.add_widget(button)

    def view_unit(self, dict_shed):
        Logger.info("Вызов окна просмотра урока")
        view = ViewUnit()
        view.update_child(dict_shed)
        view.open()


# окно для получения статистики
class StatView(ModalView):
    name = None

    def get_all_stat(self):
        result_select_stat = sql_table_select_stat().fetchall()
        stat_view = MyLayout(orientation='vertical')
        Logger.info('Получили массив имен учеников {}'.format(result_select_stat))
        self.add_widget(stat_view)
        for result in result_select_stat:
            Logger.info(type(result[0]))
            button = Button(text=result[0], font_size=30)
            button.bind(on_press=lambda btn: self.view_stat_name(result[0]))
            stat_view.add_widget(button)

    def view_stat_name(self, name):
        Logger.info("Вызов окна просмотра cтаты по ученику")
        result_stat_name = sql_table_select_stat(name).fetchall()
        view = ViewStat()
        stat_view_all = MyLayout(orientation='vertical')
        stat_view_prew = MyLayout(orientation='horizontal')
        stat_view_mass = MyLayout(orientation='horizontal')
        label_prew_date = Label(text="Дата занятия", size=(.3, .3), pos=(self.x+100, self.y+100))
        label_prew_state = Label(text="Было/не было", size=(.3, .3))
        label_prew_salary = Label(text="Оплачено/не оплачено", size=(.3, .3))
        stat_view_prew.add_widget(label_prew_date)
        stat_view_prew.add_widget(label_prew_state)
        stat_view_prew.add_widget(label_prew_salary)
        for result in result_stat_name:
            dict_result = dict(date=result[0], check_state=result[1], check_salary=result[2])
            if dict_result['check_state'] == 1:
                label_state = Label(text='Да')
            else:
                label_state = Label(text='Нет')
            if dict_result['check_salary'] == 1:
                label_salary = Label(text='Да')
            else:
                label_salary = Label(text='Нет')
            label_date = Label(text=dict_result['date'])
            stat_view_mass.add_widget(label_date)
            stat_view_mass.add_widget(label_state)
            stat_view_mass.add_widget(label_salary)
        stat_view_all.add_widget(stat_view_prew)
        stat_view_all.add_widget(stat_view_mass)
        view.add_widget(stat_view_all)
        self.dismiss()
        view.open()


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
