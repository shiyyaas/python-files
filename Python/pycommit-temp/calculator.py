from tkinter import *

window = Tk() 
window.geometry("1080x500")
def number():
    print(2)
button = Button(text="Hello", width=10, height=5, command=number)
label = Label(text="Enter the text")
button.pack()
label.pack()
window.mainloop()