import tkinter as tk
from tkinter import ttk

import messagebox
import psycopg2

# Переменная шрифта
c_f = "GostBazis 12"

# Подключение к локальной БД компьютера
connection = psycopg2.connect(
    database="phoneSales_db",
    user="postgres",
    password="trust",
    host="localhost",
    port="5432")

# Главное окно при запуске
phone_sales = tk.Tk()
phone_sales.iconbitmap("favicon.ico")
phone_sales.title("phone_sales app from Stas Sanachev")
phone_sales.geometry("850x120+200+200")

# Меню
start_button_frame = tk.LabelFrame(phone_sales, text="Меню")
start_button_frame.pack(side="top", fill="x")

hello_text = tk.Label(start_button_frame, text="""Добро пожаловать в приложение по продаже телефонов
Доступный функционал зависит от роли вашей учётной записи""", font="GostBazis 16 bold italic underline")
hello_text.pack(side="top", fill="x", pady=5)


# Кнопка закрыть приложение
def close_phone_sales():
    connection.close()
    phone_sales.destroy()


# Фрейм пользователя при успешной авторизации
def create_user_frame():
    phone_sales.geometry("1150x600+100+200")
    user_frame = tk.LabelFrame(phone_sales, text="ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ")
    user_frame.pack(side="top", expand=True, fill="both", pady=5)
    # Пользователю сразу выводится список телефонов для заказа
    global connection
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id_phone, brand, memory_storage, ram, cpu FROM phones")
        phone_list = cursor.fetchall()
        cursor.close()
        connection.commit()
    except Exception as error:
        connection.rollback()
        messagebox.showerror(title='', message=f"Ошибка \n{error}")
    else:
        phone_columns = ("id_phone", "brand", "memory_storage", "ram", "cpu")
        table = ttk.Treeview(user_frame, columns=phone_columns, show="headings")
        table.heading("id_phone", text="id")
        table.heading("brand", text="Название")
        table.heading("memory_storage", text="Встроенная память")
        table.heading("ram", text="Оперативная память")
        table.heading("cpu", text="Процессор")
        for phone in phone_list:
            table.insert("", "end", iid=phone[0], values=phone[0:])
        table.pack(side="top", expand=True, fill="both")


# Фрейм администратора при успешной авторизации
def create_admin_frame():
    phone_sales.geometry("1150x600+100+200")
    admin_frame = tk.LabelFrame(phone_sales, text="ИНТЕРФЕЙС АДМИНИСТРАТОРА")
    admin_frame.pack(side="top", fill="both", pady=5)

    # Фрейм управления пользователями
    def manage_users():
        admin_menu_frame.destroy()
        manage_users_frame = tk.LabelFrame(admin_frame, text="Управление пользователями")
        manage_users_frame.pack(side="top", fill="both")

        # Вывести таблицу пользователей
        global connection
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            users_list = cursor.fetchall()
            cursor.close()
            connection.commit()
        except Exception as error:
            connection.rollback()
            messagebox.showerror(title='', message=f"Ошибка \n{error}")
        else:
            user_columns = ("id_user", "name", "login", "password", "admin_competence", "exist")
            table = ttk.Treeview(manage_users_frame, columns=user_columns, show="headings")
            table.heading("id_user", text="id")
            table.heading("name", text="Имя пользователя")
            table.heading("login", text="Логин")
            table.heading("password", text="Пароль")
            table.heading("admin_competence", text="Администрирование")
            table.heading("exist", text="Доступ")
            for user in users_list:
                table.insert("", "end", iid=user[0], values=user[0:])
            table.pack(side="top", expand=True, fill="both")

        def admin_t():
            global connection
            try:
                index = table.focus()
                cursor = connection.cursor()
                cursor.execute("UPDATE users SET admin_competence=True WHERE id_user=%s", (index,))
                cursor.close()
                connection.commit()
            except Exception as error:
                connection.rollback()
                messagebox.showerror(title='', message=f"Ошибка \n{error}")
            else:
                messagebox.showinfo(title="", message="Права пользователя изменены")
                manage_users_frame.destroy()
                manage_users()

        def admin_f():
            global connection
            try:
                index = table.focus()
                cursor = connection.cursor()
                cursor.execute("UPDATE users SET admin_competence=False WHERE id_user=%s", (index,))
                cursor.close()
                connection.commit()
            except Exception as error:
                connection.rollback()
                messagebox.showerror(title='', message=f"Ошибка \n{error}")
            else:
                messagebox.showinfo(title="", message="Права пользователя изменены")
                manage_users_frame.destroy()
                manage_users()

        def access_t():
            global connection
            try:
                index = table.focus()
                cursor = connection.cursor()
                cursor.execute("UPDATE users SET exist=True WHERE id_user=%s", (index,))
                cursor.close()
                connection.commit()
            except Exception as error:
                connection.rollback()
                messagebox.showerror(title="", message=f"Ошибка \n{error}")
            else:
                messagebox.showinfo(title="", message="Пользователь разблокирован")
                manage_users_frame.destroy()
                manage_users()

        def access_f():
            global connection
            try:
                index = table.focus()
                cursor = connection.cursor()
                cursor.execute("UPDATE users SET exist=False WHERE id_user=%s", (index,))
                cursor.close()
                connection.commit()
            except Exception as error:
                connection.rollback()
                messagebox.showerror(title='', message=f"Ошибка \n{error}")
            else:
                messagebox.showinfo(title="", message="Пользователь заблокирован")
                manage_users_frame.destroy()
                manage_users()

        btn_admin_t = tk.Button(manage_users_frame, text="Назначить администратором", font=c_f, command=admin_t)
        btn_admin_t.pack(side="left", expand=True, fill="x")
        btn_admin_f = tk.Button(manage_users_frame, text="Разжаловать из администраторов", font=c_f, command=admin_f)
        btn_admin_f.pack(side="left", expand=True, fill="x")
        btn_access_t = tk.Button(manage_users_frame, text="Разблокировать пользователя", font=c_f, command=access_t)
        btn_access_t.pack(side="left", expand=True, fill="x")
        btn_access_f = tk.Button(manage_users_frame, text="Заблокировать пользователя", font=c_f, command=access_f)
        btn_access_f.pack(side="left", expand=True, fill="x")

    # Фрейм управления товаром
    def manage_phones():
        admin_menu_frame.destroy()
        manage_phones_frame = tk.LabelFrame(admin_frame, text="Управление товаром")
        manage_phones_frame.pack(side="top", fill="both")
        global connection
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id_phone, brand, memory_storage, ram, cpu FROM phones")
            phone_list = cursor.fetchall()
            cursor.close()
            connection.commit()
        except Exception as error:
            connection.rollback()
            messagebox.showerror(title='', message=f"Ошибка \n{error}")
        else:
            phone_columns = ("id_phone", "brand", "memory_storage", "ram", "cpu")
            table = ttk.Treeview(manage_phones_frame, columns=phone_columns, show="headings")
            table.heading("id_phone", text="id")
            table.heading("brand", text="Название")
            table.heading("memory_storage", text="Встроенная память")
            table.heading("ram", text="Оперативная память")
            table.heading("cpu", text="Процессор")
            for phone in phone_list:
                table.insert("", "end", iid=phone[0], values=phone[0:])
            table.pack(side="top", expand=True, fill="both")

        def del_phone():
            global connection
            try:
                index = table.focus()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM phones WHERE id_phone=%s", (index,))
                cursor.close()
                connection.commit()
            except Exception as error:
                connection.rollback()
                messagebox.showerror(title='', message=f"Ошибка \n{error}")
            else:
                messagebox.showinfo(title="", message="Телефон удалён")
                manage_phones_frame.destroy()
                manage_phones()

        def add_phone():
            btn_del_phone.config(state="disabled")
            btn_add_phone.config(state="disabled")
            add_phone_frame = tk.LabelFrame(manage_phones_frame, text="Добавление телефона")
            add_phone_frame.pack(side="bottom", expand=True, fill="x")

            ins_brand = tk.StringVar()
            ins_brand_label = tk.Label(add_phone_frame, text="Название", font=c_f)
            ins_brand_label.pack(side="left", padx=5)
            ins_brand_entry = tk.Entry(add_phone_frame, font=c_f, width=20, textvariable=ins_brand)
            ins_brand_entry.pack(side="left", padx=5)
            ins_memory_storage = tk.StringVar()
            ins_memory_storage_label = tk.Label(add_phone_frame, text="Встроенная память", font=c_f)
            ins_memory_storage_label.pack(side="left", padx=5)
            ins_memory_storage_entry = tk.Entry(add_phone_frame, font=c_f, width=5, textvariable=ins_memory_storage)
            ins_memory_storage_entry.pack(side="left", padx=5)
            ins_ram = tk.StringVar()
            ins_ram_label = tk.Label(add_phone_frame, text="Оперативная память", font=c_f)
            ins_ram_label.pack(side="left", padx=5)
            ins_ram_entry = tk.Entry(add_phone_frame, font=c_f, width=5, textvariable=ins_ram)
            ins_ram_entry.pack(side="left", padx=5)
            ins_cpu = tk.StringVar()
            ins_cpu_label = tk.Label(add_phone_frame, text="Процессор", font=c_f)
            ins_cpu_label.pack(side="left", padx=5)
            ins_cpu_entry = tk.Entry(add_phone_frame, font=c_f, width=5, textvariable=ins_cpu)
            ins_cpu_entry.pack(side="left", padx=5)

            def add_row():
                global connection
                try:
                    cursor = connection.cursor()
                    cursor.execute("""INSERT INTO phones (brand, memory_storage, ram, cpu) VALUES (%s, %s, %s, %s)""",
                                   (ins_brand.get(), ins_memory_storage.get(), ins_ram.get(), ins_cpu.get()))
                    cursor.close()
                    connection.commit()
                except Exception as error:
                    connection.rollback()
                    messagebox.showerror(title='', message=f"Ошибка \n{error}")
                else:
                    messagebox.showinfo(title="", message="Телефон добавлен в базу")
                    manage_phones_frame.destroy()
                    manage_phones()

            btn_add_row = tk.Button(add_phone_frame, text="ЗАПИСАТЬ", font=c_f, command=add_row)
            btn_add_row.pack(side="right", fill="x")

        btn_del_phone = tk.Button(manage_phones_frame, text="Удалить телефон", font=c_f, command=del_phone)
        btn_del_phone.pack(side="bottom", expand=True, fill="x")
        btn_add_phone = tk.Button(manage_phones_frame, text="Добавить телефон", font=c_f, command=add_phone)
        btn_add_phone.pack(side="bottom", expand=True, fill="x")

    admin_menu_frame = tk.LabelFrame(admin_frame, text="Meню функций администратора")
    admin_menu_frame.pack(side="top", fill="x")
    btn_manage_users = tk.Button(admin_menu_frame, text="Управлять пользователями", font=c_f, command=manage_users)
    btn_manage_users.pack(side="left", expand=True, fill="x")
    btn_manage_phones = tk.Button(admin_menu_frame, text="Управлять товаром", font=c_f, command=manage_phones)
    btn_manage_phones.pack(side="left", expand=True, fill="x")


# Кнопка открыть фрейм для регистрации нового пользователя
def open_sign_frame():
    btn_open_login_frame.config(state="disabled")
    btn_open_sign_frame.config(state="disabled")

    phone_sales.geometry("1150x170+200+200")

    sign_frame = tk.LabelFrame(phone_sales, text="Регистрация нового пользователя")
    sign_frame.pack(side="top", fill="both", pady=5)

    ins_name = tk.StringVar()
    ins_name_label = tk.Label(sign_frame, text="ФИО", font=c_f)
    ins_name_label.pack(side="left", padx=5)
    ins_name_entry = tk.Entry(sign_frame, font=c_f, width=20, textvariable=ins_name)
    ins_name_entry.pack(side="left", padx=5)

    ins_login = tk.StringVar()
    ins_login_label = tk.Label(sign_frame, text="Логин", font=c_f)
    ins_login_label.pack(side="left", padx=5)
    ins_login_entry = tk.Entry(sign_frame, font=c_f, width=20, textvariable=ins_login)
    ins_login_entry.pack(side="left", padx=5)

    ins_password = tk.StringVar()
    ins_password_label = tk.Label(sign_frame, text="Пароль", font=c_f)
    ins_password_label.pack(side="left", padx=5)
    ins_password_entry = tk.Entry(sign_frame, font=c_f, width=20, textvariable=ins_password)
    ins_password_entry.pack(side="left", padx=5)

    def registration():
        if len(ins_name.get()) > 0:
            if len(ins_login.get()) > 0:
                if len(ins_password.get()) > 0:
                    global connection
                    try:
                        cursor = connection.cursor()
                        cursor.execute(
                            """INSERT INTO users (name, login, password, admin_competence, exist) 
                                VALUES (%s, %s, %s, False, True)""",
                            (ins_name.get(), ins_login.get(), ins_password.get()))
                        cursor.close()
                        connection.commit()
                    except Exception as error:
                        connection.rollback()
                        messagebox.showerror(title='', message=f"Ошибка \n{error}")
                    else:
                        print(ins_name.get(), ins_login.get(), ins_password.get())
                        messagebox.showinfo(title="",
                                            message="Пользователь создан. Зайдите со своим логином и паролем.")
                        sign_frame.destroy()
                        btn_open_login_frame.config(state="normal")
                        btn_open_sign_frame.config(state="normal")
                else:
                    messagebox.showinfo(title="", message="Введите пароль")
            else:
                messagebox.showinfo(title="", message="Введите логин")
        else:
            messagebox.showinfo(title="", message="Введите имя")

    btn_registration = tk.Button(sign_frame, text="Зарегистрироваться", font=c_f, command=registration)
    btn_registration.pack(side="left", fill="x", expand=True)


# Кнопка открыть фрейм для авторизации
def open_login_frame():
    btn_open_login_frame.config(state="disabled")
    btn_open_sign_frame.config(state="disabled")
    phone_sales.geometry("850x170+200+200")
    login_frame = tk.LabelFrame(phone_sales, text="Авторизация существующего пользователя")
    login_frame.pack(side="top", fill="both", pady=5)

    auth_login = tk.StringVar()
    auth_login_label = tk.Label(login_frame, text="Логин", font=c_f)
    auth_login_label.pack(side="left", padx=5)

    auth_login_entry = tk.Entry(login_frame, font=c_f, width=25, textvariable=auth_login)
    auth_login_entry.pack(side="left", padx=5)

    auth_password = tk.StringVar()
    auth_password_label = tk.Label(login_frame, text="Пароль", font=c_f)
    auth_password_label.pack(side="left", padx=5)
    auth_password_entry = tk.Entry(login_frame, show="*", font=c_f, width=25, textvariable=auth_password)
    auth_password_entry.pack(side="left", padx=5)

    # Проверка введённых логина и пароля
    def authorization():
        global connection
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT login, password, exist, admin_competence FROM users")
            list = cursor.fetchall()
            cursor.close()
            connection.commit()
        except Exception as e:
            connection.rollback()
            messagebox.showerror(title='', message=f"Ошибка \n{e}")
        else:
            login_list = []
            password_list = []
            exist_list = []
            admin_list = []
            for i in list:
                login_list.append(i[0])
                password_list.append(i[1])
                exist_list.append(i[2])
                admin_list.append(i[3])

            for j in range(len(login_list)):
                if login_list[j] == auth_login.get():
                    if password_list[j] == auth_password.get():
                        if exist_list[j] == True:
                            if admin_list[j] == True:
                                create_admin_frame()
                                login_frame.destroy()
                            else:
                                create_user_frame()
                                login_frame.destroy()
                        else:
                            messagebox.showinfo(title="", message="Отказано в доступе")
                            login_frame.destroy()

    def close_login_frame():
        login_frame.destroy()
        btn_open_login_frame.config(state="normal")
        btn_open_sign_frame.config(state="normal")

    btn_authorization = tk.Button(login_frame, text="Авторизоваться", font=c_f, command=authorization)
    btn_authorization.pack(side="left", fill="x", expand=True)
    btn_close_login_frame = tk.Button(login_frame, text="Отмена", font=c_f, command=close_login_frame)
    btn_close_login_frame.pack(side="left", fill="x", expand=True)


# БЛОК КНОПОК МЕНЮ
btn_open_login_frame = tk.Button(start_button_frame, text="Войти", font=c_f, underline=0, command=open_login_frame)
btn_open_login_frame.pack(expand=True, side="left", fill="x")

btn_open_sign_frame = tk.Button(start_button_frame, text="Зарегистрироваться", font=c_f, underline=0,
                                command=open_sign_frame)
btn_open_sign_frame.pack(expand=True, side="left", fill="x")

btn_close_phone_sales = tk.Button(start_button_frame, text="Выйти из приложения", font=c_f, underline=0,
                                  command=close_phone_sales)
btn_close_phone_sales.pack(expand=True, side="left", fill="x")

# START PROJECT
phone_sales.mainloop()
