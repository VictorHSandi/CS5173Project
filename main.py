from tkinter import *
import os

root = Tk()
img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "messageicon.png"))
root.iconphoto(True, img)
root.wm_title("Secure P2P Messaging")



root.mainloop()