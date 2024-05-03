from tkinter import *
import os
import ctypes


class GUI():
    def __init__(self):
        self.msg = None
        self.entryMsg = None
        self.labelBottom = None
        self.textCons = None
        self.name = None
        self.bg_blue = "#6a788f"
        self.bg_dark_blue = "#283140"
        self.bg_light_blue = "#47566e"
        self.text_color = "white"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CS5173.product.id")
        icon = os.path.join(os.path.dirname(__file__), "messageicon.ico")

        self.root = Tk()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.root.withdraw()
        self.root.geometry("600x900")
        self.root.resizable(0, 0)
        self.root.configure(bg=self.bg_blue)
        self.root.iconbitmap(icon)
        self.root.wm_title("Secure P2P Messaging")

        self.login = Toplevel()
        self.login.geometry("600x400")
        self.login.resizable(0, 0)
        self.login.wm_title("Passphrase Entry")
        self.login.iconbitmap(icon)
        self.login.configure(bg=self.bg_blue)

        self.pas = Label(self.login, text="Enter Passphrase", justify="center", font="Courier 18")
        self.pas.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.pas.configure(bg=self.bg_blue)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.entryName.config(bg=self.bg_light_blue,fg=self.text_color)
        self.entryName.focus()
        self.go = Button(self.login, text="Enter", font="Courier 18 bold",
                         bg=self.bg_light_blue,
                         fg=self.text_color,
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.root.mainloop()

    def goAhead(self, passkey):
        self.login.destroy()
        self.layout(passkey)

    def layout(self, name):
        self.name = name
        self.root.deiconify()

        self.textCons = Text(self.root,
                             width=1,
                             height=1,
                             bg=self.bg_dark_blue,
                             fg=self.text_color,
                             font="Courier 14",
                             )
        self.textCons.place(relwidth=2, relheight=2, relx=-0.1)
        self.labelBottom = Label(self.root, bg=self.bg_blue, height=5)

        self.labelBottom.place(relwidth=1, rely=0.94)
        self.entryMsg = Entry(self.labelBottom,
                              bg=self.bg_light_blue,
                              fg=self.text_color,
                              font="Courier 14")
        self.entryMsg.place(relwidth=0.75,
                            relheight=0.4,
                            rely=0.1,
                            relx=0.01)

        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Courier 20 bold",
                                bg=self.bg_light_blue,
                                fg=self.text_color,
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.78,
                             rely=0.11,
                             relheight=0.4,
                             relwidth=0.20)
        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=0.46, relx=0.52, rely=0.005)
        scrollbar.config(command=self.textCons.yview, bg=self.bg_blue)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)

    def receive(self):
        print("Recieved")

    def sendMessage(self):
        print("Sent")
gui = GUI()
