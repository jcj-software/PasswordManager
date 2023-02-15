import tkinter as tk
import ttkbootstrap as tbs
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
from tkinter import *
from tkinter.ttk import *

import openai
import pystray
import PIL.Image as Img
from pystray import MenuItem, Menu

import threading
import sys
import pickle

openai.api_key = ''

def quit_window(icon: pystray.Icon):
    icon.stop()
    root.destroy()

def show_window():
    root.deiconify()

def on_exit():
    root.withdraw()
    
def ask():
    global api
    openai.api_key = api.get()
    global inp
    text = inp.get("0.0", "end")
    try:
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = text,
            temperature = 0,
            max_tokens = 1000,
            top_p = 1,
            frequency_penalty = 0.0,
            presence_penalty = 0.0,
            stop = None
        )
        global bot
        bot.insert(INSERT, str(response.choices[0].text + '\n'))
    except openai.error.AuthenticationError:
        showerror("ChatGPT-China", "Api Key Error! ")
    except:
        showerror("ChatGPT-China", "Unknown Error! ")

root = tbs.Style('cosmo').master
root.title("ChatGPT-China")
root.geometry("500x300")
root.iconbitmap('assets/icon.ico')
root.protocol('WM_DELETE_WINDOW', on_exit)
menu = (MenuItem("显示主窗口", show_window, default = True),
        Menu.SEPARATOR, MenuItem("退出", quit_window))
image = Img.open("assets/icon.ico")
icon = pystray.Icon("icon", image, "ChatGPT-China", menu)

apiLabel = Label(text = "Api Key：")
apiLabel.pack()

global api
api = Entry()
api.pack()

inpLabel = Label(text = "输入：")
inpLabel.pack()

global inp
inp = Text(root, width = 100, height = 3)
inp.pack(padx = 25, pady = 10)

run = Button(root, text = "询问", command = ask)
run.pack(padx = 25, pady = 10)

botLabel = Label(text = "返回：")
botLabel.pack()

global bot
bot = Text(root, width = 100, height = 3)
bot.pack(padx = 25, pady = 10)

threading.Thread(target = icon.run, daemon = True).start()
on_exit()
root.mainloop()

