# See PyCharm help at
# https://www.jetbrains.com/help/pycharm/
# Взято с
# https://www.youtube.com/watch?v=d7wZeAhn7B0

# Импорт модуля tkinter для форм
import tkinter as tk
# Добавляем модуль ttk для отображения таблиц
from tkinter import ttk
# Импорт БД
import sqlite3


# Класс главного окна, наследованный от объекта библиотеки tkinter - frame
class Main(tk.Frame):
    # Конструктор с аргументами: 1. Текущий экземпляр класса. 2. Корневое окно программы
    def __init__(self, root):
        # В метод init базового класса передаем аргументы, переданные в root
        super().__init__(root)
        # Инициализиция объектов интерфейса при инициализациии класса при загрузке
        self.init_main()
        # Ссылаемся на экземпляр класса DB для последующего вызова
        # функция класса DB через переменную db в функции records
        self.db = db
        # Загружаем данные на форму
        self.view_records()

    # Ф-я для сохраненеия и инициализации объектов интерфейса
    def init_main(self):
        # Тулбар вверху формы (цвет фона и отступ)
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        # Отображаем тулбар с закреплением в верхней части окна и растягиваем по горизонтали
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Добавляем картинку для кнопки
        self.add_img = tk.PhotoImage(file='add.gif')
        # Задаем кнопку
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка редактировать
        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка Удалить
        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить выделенные', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка Поиск
        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка Обновить
        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Виджет Treeview передаем self и 4 колонки
        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')
        # Параметры к колонкам
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("description", width=355, anchor=tk.CENTER)
        self.tree.column("costs", width=150, anchor=tk.CENTER)
        self.tree.column("total", width=100, anchor=tk.CENTER)
        # Названия колонкам
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')
        # Вывод в главное окно с выравниванием по левой стороне
        self.tree.pack(side=tk.LEFT)

        # Полоса прокрутки
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Ф-я вызова дочернего окна
    def open_dialog(self):
        # Класс child
        Child()

    # Промежуточная функция для вызова записи в БД
    def records(self, description, costs, total):
        # Для доступа у функциям класса DB нужно создать экземпляр класса
        self.db.insert_data(description, costs, total)
        # Перезаливваем данные
        self.view_records()

    # Функция вывода данных БД на форму
    def view_records(self):
        self.db.c.execute(
            '''SELECT id, description, costs, total FROM finance'''
        )
        # Очистка списка для перезаполнения после добавления
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Перезаполняем список новое добавлять после предудущего
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Функция обновления записи
    def update_record(self, description, costs, total):
        # Передаем все поля и id как первый элемент их списка выделенных и порядковый номер столбца
        self.db.c.execute(
            '''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
            (description, costs, total, self.tree.set(self.tree.selection()[0], '#1'))
        )
        self.db.conn.commit()
        self.view_records()

    # Функция удаления
    def delete_records(self):
        # Цикл удаление нескольких записей
        # Запятая (self.tree.set(select, '#1'),)) - для удаление при более 10 записей
        for selection_item in self.tree.selection():
            self.db.c.execute(
                '''DELETE FROM finance WHERE id=?''', (self.tree.set(selection_item, '#1'),)
            )
        self.db.conn.commit()
        self.view_records()

    # Функция кнопки Редактировать
    def open_update_dialog(self):
        # вызов класса Update
        Update()

    # Функция открываем окно поиска
    def open_search_dialog(self):
        Search()

    # Функция поиска
    def search_records(self, desctiption):
        desctiption = ('%' + desctiption + '%',)
        self.db.c.execute(
            '''SELECT id, description, costs, total FROM finance WHERE description LIKE ?''', desctiption
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


# Класс для дочернего окна с наследованием от Toplevel
class Child(tk.Toplevel):
    # Конструктор класса и метод super()
    def __init__(self):
        super().__init__(root)
        # Инициализация объектов
        self.init_child()
        # Предаем класс Main в Child для доступа к функциям класса Main
        self.view = app

    # Функция инициализиции объектов и виджетов окна
    def init_child(self):
        # Имя, размер и запрет на изменение
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        # Подписи полей
        label_desctiption = tk.Label(self, text='Наименование:')
        label_desctiption.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        # Поля ввода описания
        self.entry_desctiption = ttk.Entry(self)
        # Координаты расположения
        self.entry_desctiption.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        # Выпадающий список
        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        # Кнопка закрыть
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        # Кнопка добавить
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_desctiption.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_money.get()))
        # Добавляем функции модального, т.е прехватываем фокус не нем до закрытия
        self.grab_set()
        self.focus_set()


# Класс формы для удаления, через наследование от класса Child (форма добавления)
class Update(Child):
    # конструктор
    def __init__(self):
        super().__init__()
        # Применение изменений через вызов функции
        self.init_edit()
        # Передаем функции из класса main
        self.view = app
        self.db = db
        # добавляем в конструктор
        self.default_data()

    # Меняем подпись формы и кнопка удалить
    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_desctiption.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))
        # Убираем кнопку OK
        self.btn_ok.destroy()

    # Функция получения данных из БД
    def default_data(self):
        self.db.c.execute(
            '''SELECT id, description, costs, total FROM finance WHERE id=?''',
            (self.view.tree.set(self.view.tree.selection()[0], '#1'),)
        )
        row = self.db.c.fetchone()
        # Выводим значения в поля формы
        self.entry_desctiption.insert(0, row[1])
        # Если Расход, то прставить его иначе по умолчанию будет доход
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_money.insert(0, row[3])

# Класс формы поиска
class Search(tk.Toplevel):
    # Конструктор
    def __init__(self):
        super().__init__()
        self.init_search()
        # Добавляем класс main для вызова его функций
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        lable_search = tk.Label(self, text='Поиск')
        lable_search.place(x=50, y=20)

        # Поле для поиска
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cansel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    # Конструктор класса
    def __init__(self):
        # Соединение с БД
        self.conn = sqlite3.connect('finance.db')
        # Создание экземпляр класса курсор
        self.c = self.conn.cursor()
        # Запрос на создание таблицы
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (id integer primary key, description text, costs text, total real)'''
        )
        # Выполняем запрос
        self.conn.commit()

    # Ф-я добавления записи
    def insert_data(self, description, costs, total):
        self.c.execute(
            '''INSERT INTO finance(description, costs, total) VALUES(?, ?, ?)''',
            (description, costs, total)
        )
        self.conn.commit()


# Базовая конструкция
# Если скрипт запущен как корневая программа, то выполнится
if __name__ == "__main__":
    root = tk.Tk()
    # Именно после root
    # Для доступа у функциям класса DB нужно создать экземпляр класса
    # и потом можем использовать его в конструкторе класса Main
    db = DB()
    app = Main(root)
    # Пременяем метод pack для упаковки
    app.pack()
    # Название окна
    root.title("Household finance")
    # Размеры окна
    root.geometry("650x450+300+200")
    # Запрет изменения размеров по вертикали и горизонтали
    root.resizable(False, False)
    # Обязательно последняя строка
    root.mainloop()
