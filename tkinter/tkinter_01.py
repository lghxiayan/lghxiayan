from tkinter import *

root = Tk()
lb = Label(root, text='我是第一个标签', \
           bg='#d3fbfb', \
           fg='red', \
           font=('华文新魏', 32), \
           width=20, \
           height=2, \
           relief=SUNKEN)
lb.pack()
root.mainloop()
