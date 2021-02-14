from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Dropdown Menu For NBA Shot Chart")
root.geometry("400x400")

clicked = StringVar()
clicked.set("Monday")

clicked1 = StringVar()
clicked1.set("March")


drop = OptionMenu(root, clicked,"Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
drop.pack()

drop1 = OptionMenu(root, clicked1, "January", "February", "March", "April")
drop1.pack()

# T = Text(root, height=2, width=30)
# T.pack()
# T.insert(END, "Choose Player's First Name")
# listaEquipos = ['Equipos']
# menuEquipoText = StringVar(root)
# menuEquipoText.set(listaEquipos[0])
# menuEquipo = OptionMenu(root, menuEquipoText, *'Hello')
# menuEquipo.pack()
#
# T1 = Text(root, height=2, width=30)
# T1.pack()
# T1.insert(END, "Choose Player's Last Name")





root.mainloop()


# print("CLICKED")
# day = clicked.get()
# print(day)

