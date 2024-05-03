from tkinter import *
import os
import ctypes
root = Tk()
icon = os.path.join(os.path.dirname(__file__), "messageicon.ico")
myappid = "CS5173.product.id"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root.iconbitmap(icon)
root.wm_title("Secure P2P Messaging")



root.mainloop()