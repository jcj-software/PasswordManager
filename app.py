import tkinter as tk
import ttkbootstrap as tbs
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
from tkinter import *
from tkinter.ttk import *

import pyperclip
import pystray
import PIL.Image as Img
from pystray import MenuItem, Menu

import threading
import sys
import pickle
import win32api
import win32con


def quit_window(icon: pystray.Icon):
    with open('data.dat', 'wb') as f:
        pickle.dump(lst, f)
    icon.stop()
    root.destroy()

def show_window():
    root.deiconify()

def on_exit():
    root.withdraw()

def jiesuo(button):
    try:
        with open('auth.dat', 'rb') as f:
            auth = pickle.load(f)
    except:
        auth = [False, '']
    
    if auth[0] == True:
        inp = askstring('Password Manager', '主密码：')
        if inp == auth[1]:
            button.pack_forget()
            mainFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        else:
            showinfo('Password Manager', '主密码错误')
    else:
        showinfo('Pasword Manager', '您还没有设置主密码！')
        auth[1] = askstring('Password Manager', '初始化主密码（设置后无法更改）：')
        auth[0] = True
        with open('auth.dat', 'wb') as f:
            pickle.dump(auth, f)

def password_add():
    add = askstring('Password Manager', '密码：')
    lst.append(add)
    password.insert("end", add)

root = tbs.Style('cosmo').master
root.title("Password Manager")
root.geometry("300x250")
root.iconbitmap('assets/icon.ico')
root.protocol('WM_DELETE_WINDOW', on_exit)
menu = (MenuItem("显示主窗口", show_window, default = True),
        Menu.SEPARATOR, MenuItem("退出", quit_window))
image = Img.open("assets/icon.ico")
icon = pystray.Icon("icon", image, "Password Manager", menu)
button_auth = Button(root, text = "解锁", command = lambda: jiesuo(button_auth))
button_auth.place(relx = 0.5, rely = 0.5, anchor = CENTER)
mainFrame = Frame(root)

password = Listbox(mainFrame, selectmode = "single")
password.pack(side = "top", pady = 10)
try:
    with open('data.dat', 'rb') as f:
        lst = pickle.load(f)
    for i in lst:
        password.insert("end", i)
except:
    lst = []

buttonFrame1 = Frame(mainFrame)
buttonFrame1.pack(side = "bottom", pady = 10)
button_add = Button(buttonFrame1, text = '添加', style = "Outline.TButton", command = password_add)
button_add.pack(side = "left", padx = 25)
button_delete = Button(buttonFrame1, text = '删除', style = "Outline.TButton", command = lambda x = password:x.delete(ACTIVE))
button_delete.pack(side = "right", padx = 25)
button_copy = Button(buttonFrame1, text = '复制', style = "Outline.TButton", command = lambda x = password:pyperclip(x.get(x.curselection())))
button_copy.pack(side = "bottom", padx = 25)


threading.Thread(target = icon.run, daemon = True).start()
on_exit()
root.mainloop()

