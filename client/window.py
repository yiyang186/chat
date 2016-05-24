
# encoding: utf-8
import Tkinter as tk
import tkMessageBox as tb
import socket
import select
import threading
import sys

def send_chats(event=None):
    my_socket.send(str_user.get() + ":" + str_send.get())
    str_send.set("")

def clear():
    text_recv.delete(0.0, tk.END)

def get_chats(s):
    my = [my_socket]
    while True:
        r, w, e=select.select(my, [], [])
        if s in r:
            try:
                info = my_socket.recv(1024).strip()
                text_recv.insert(tk.END, info + "\n")
            except socket.error:
                text_recv.insert(tk.END, "socket错误\n")
                exit()

host = socket.gethostname()
addr = (host, 3456)
my_socket = socket.socket()
my_socket.connect(addr)
thread_recv = threading.Thread(target=get_chats, args=(my_socket,))
thread_recv.start()

top = tk.Tk()
top.title('聊天')
top.geometry('430x320')

text_recv = tk.Text(top, width=60, height=20)
text_recv.grid(row=0, columnspan=4)

str_send = tk.StringVar()
entry_send = tk.Entry(top, textvariable=str_send, width=60)
entry_send.bind('<Return>', send_chats)
entry_send.grid(row=1, columnspan=4)

label_user = tk.Label(top, text=u"昵称", width=15, height=1)
label_user.grid(row=2, column=0)

str_user = tk.StringVar()
entry_user = tk.Entry(top, textvariable=str_user, width=15)
entry_user.grid(row=2, column=1)

button_send = tk.Button(top, text=u"发送", command=send_chats, width=10,
                        height=1)
button_send.grid(row=2, column=2)

button_clear = tk.Button(top, text=u"清空", command=clear, width=10, height=1)
button_clear.grid(row=2, column=3)

top.mainloop()


