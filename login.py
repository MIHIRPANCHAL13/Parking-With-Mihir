from tkinter import *
from tkinter import messagebox
import random
import re

from tkinter import ttk

import mysql.connector
from PIL import Image
from PIL import ImageTk

from front import Smart_Parking_System


captcha_code = ""
register_window = None



def register():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="login")
    mycursor = mysqldb.cursor()

    uname = e1_register\
        .get()
    password = e2_register.get()

    if uname and password:
        # Password validation criteria
        if len(password) < 6 or len(password) > 16:
            messagebox.showinfo("", "Password should be between 6 to 16 characters.")
        elif not re.search(r'[A-Z]', password):
            messagebox.showinfo("", "Password should contain at least one capital letter.")
        elif not re.search(r'\W', password):
            messagebox.showinfo("", "Password should contain at least one special character.")
        else:
            sql = "INSERT INTO login (username, password) VALUES (%s, %s)"
            values = (uname, password)
            mycursor.execute(sql, values)
            mysqldb.commit()
            messagebox.showinfo("", "Registration successful!")
            clear_fields()
    else:
        messagebox.showinfo("", "Please fill in all the fields.")


def clear_fields():
    e1_login.delete(0, END)
    e2_login.delete(0, END)
    e1_register.delete(0, END)
    e2_register.delete(0, END)


def login():
    if verify_captcha():
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="login")
        mycursor = mysqldb.cursor()

        uname = e1_login.get()
        password = e2_login.get()

        sql = "select * from login where username=%s and password=%s"

        mycursor.execute(sql, [(uname), (password)])
        results = mycursor.fetchall()
        if results:
            messagebox.showinfo("", "Login success:")
            root.destroy()
            rootx = Tk()
            sps = Smart_Parking_System(rootx)
            rootx.mainloop()
        else:
            messagebox.showinfo("", "Incorrect username and password")
    else:
        messagebox.showinfo("", "Incorrect captcha")


def generate_captcha():
    global captcha_code
    captcha_code = str(random.randint(10000, 99999))
    captcha_label.config(text=captcha_code)


def verify_captcha():
    captcha_input = captcha_entry.get()
    return captcha_input == captcha_code

def open_register_window():
    global register_window, e1_register, e2_register
    if register_window:
        register_window.destroy()

    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("500x300+500+300")
    register_window.config(bg="#ffffff")

    Label(register_window, text="Register", fg='#57a1f8', bg="#ffffff", font=('Microsoft YaHei UI Light', 24, 'bold')).pack(pady=10)

    Label(register_window, text="Username", fg='black', bg="#ffffff", font=('Microsoft YaHei UI Light', 12, 'bold')).pack()
    e1_register = Entry(register_window, font=("Helvetica", 12))
    e1_register.pack(pady=5)

    Label(register_window, text="Password", fg='black', bg="#ffffff", font=('Microsoft YaHei UI Light', 12, 'bold')).pack()
    e2_register = Entry(register_window, show="*", font=("Helvetica", 12))
    e2_register.pack(pady=5)

    # Password rules label
    password_rules_label = Label(register_window, text="- Should start with a capital letter\n- Should have a length between 6 and 16 characters\n- Should contain at least one special character", fg='black', bg="#ffffff", font=('Microsoft YaHei UI Light', 8,))
    password_rules_label.pack(pady=5)

    ttk.Button(register_window, text="Register", command=register).pack(pady=10)



root = Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.config(bg="#ffffff")

# Create captcha widget
captcha_frame = Frame(root, bg="#ffffff")
captcha_frame.place(x=500, y=220)
captcha_label = Label(captcha_frame, font=("Helvetica", 12), bg="#ffffff")
captcha_label.pack(side=LEFT, padx=5)
generate_captcha_button = ttk.Button(captcha_frame, text="Generate", command=generate_captcha)
generate_captcha_button.pack(side=LEFT, padx=5)
captcha_entry = Entry(captcha_frame, font=("Helvetica", 12))
captcha_entry.pack(side=LEFT, padx=5)

img = Image.open("13.png")
img = ImageTk.PhotoImage(img)
img_label = Label(root, image=img, bg="#ffffff")
img_label.place(x=70, y=70)

Label(root, text="Login", fg='#57a1f8', bg="#ffffff", font=('Microsoft YaHei UI Light', 24, 'bold')).place(x=500, y=10)
Label(root, text="Username", fg='black', bg="#ffffff", font=('Microsoft YaHei UI Light', 12, 'bold')).place(x=500, y=100)
Label(root, text="Password", fg='black', bg="#ffffff", font=('Microsoft YaHei UI Light', 12, 'bold')).place(x=500, y=150)
Label(root, text="Don't have an account?", fg='black', font=('Microsoft YaHei UI light', 8, 'bold')).place(x=450, y=355)

e1_login = Entry(root, font=("Helvetica", 12))
e1_login.place(x=600, y=100)
e2_login = Entry(root, show="*", font=("Helvetica", 12))
e2_login.place(x=600, y=150)

ttk.Button(root, text="Login", command=login).place(x=600, y=280, width=120, height=35)
ttk.Button(root, text="Register", command=open_register_window).place(x=600, y=350, width=120, height=35)

root.mainloop()
