from tkinter import *
import os
import ctypes
from AESAlgorithm import AESAlgorithm
from Crypto.Random import get_random_bytes
import socket
import threading
import re
import hashlib

class Client():
    def __init__(self, arg):
        self.nonce = None
        self.passkey = None
        self.FORMAT = 'ISO-8859-1'
        self.client_socket = None
        self.aes = AESAlgorithm(arg)
        self.buttonMsg = None
        self.cipher = None
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
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_blue)
        self.root.iconbitmap(icon)
        self.root.wm_title("Secure P2P Messaging")

        self.login = Toplevel()
        self.login.geometry("600x400")
        self.login.resizable(False, False)
        self.login.wm_title("Passphrase Entry")
        self.login.iconbitmap(icon)
        self.login.configure(bg=self.bg_blue)

        self.nameLabel = Label(self.login, text="Enter Name", justify="center", font="Courier 18")
        self.nameLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.nameLabel.configure(bg=self.bg_blue)

        self.nameEntry = Entry(self.login, font="Helvetica 14")
        self.nameEntry.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.nameEntry.config(bg=self.bg_light_blue, fg=self.text_color)
        self.nameEntry.focus()

        self.passphraseLabel = Label(self.login, text="Enter Passphrase", justify="center", font="Courier 18")
        self.passphraseLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.passphraseLabel.configure(bg=self.bg_blue)

        self.passphraseEntry = Entry(self.login, font="Helvetica 14")
        self.passphraseEntry.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.passphraseEntry.config(bg=self.bg_light_blue, fg=self.text_color)

        self.go = Button(self.login, text="Enter", font="Courier 18 bold", bg=self.bg_light_blue, fg=self.text_color,
                         command=lambda: self.goAhead(self.passphraseEntry.get(), self.nameEntry.get()))
        self.go.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.root.mainloop()

    def goAhead(self, passkey, name):
        self.name = name
        self.passkey = passkey
        self.login.destroy()
        self.layout()

        server_ip = "52.146.11.70"
        server_port = 9000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def closeApp(self):
        self.client_socket.close()
        self.root.destroy()

    def layout(self):

        self.root.deiconify()

        self.textCons = Text(self.root, width=1, height=1, bg=self.bg_dark_blue, fg=self.text_color, font="Courier 14",
                             padx=70, pady=10)
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
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = self.aes.encrypt(msg)
        self.cipher = self.msg.ciphertext
        self.nonce = self.msg.nonce
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode(self.FORMAT)
                if message == '123NAME123':
                    self.client_socket.send(self.name.encode(self.FORMAT))
                elif message == "123PASS123":
                    sha256_hash = hashlib.sha256()
                    sha256_hash.update(self.passkey.encode(self.FORMAT))
                    self.client_socket.send(sha256_hash.hexdigest().encode(self.FORMAT))
                elif message == "WRONG":
                    self.client_socket.close()
                    break
                else:
                    ciphernonce = re.split("\> (.*)\s(.*)", message)
                    if len(ciphernonce) > 2:
                        ciphertext = eval(ciphernonce[1])
                        nonce = eval(ciphernonce[2])
                        plaintext = self.aes.raw_decrypt(ciphertext, nonce)
                        self.textCons.config(state=NORMAL)
                        self.textCons.insert(END, message + f"\n    Decrypted to {plaintext}\n")
                        self.textCons.config(state=DISABLED)
                        self.textCons.see(END)
                    else:
                        self.textCons.config(state=NORMAL)
                        self.textCons.insert(END, message + f"\n")
                        self.textCons.config(state=DISABLED)
                        self.textCons.see(END)
            except Exception as e:
                print("An error occurred! Details: \n" + str(e))
                self.client_socket.close()
                break

    def sendMessage(self):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, f"{self.name}-> {self.aes.decrypt(self.msg)}" + f"\n  Sent as {self.cipher}\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

        self.textCons.config(state=DISABLED)

        while True:
            message = f"{self.name}-> {self.cipher} {self.msg.nonce}"
            self.client_socket.send(message.encode(self.FORMAT))
            break

    def closeApp(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    key = b'\xa4\x8dJT\x8a<\xf6\xcen\x0bvj\xf1j\x9ct'
    client = Client(key)
