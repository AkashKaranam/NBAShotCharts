from tkinter import *
root = Tk()

a = StringVar()
a.set("default")

oc = StringVar(root)
oc.set("Select")

def function(x):

  if x == "yes":
      a.set("hello")
      print(a.get())

  else:
      a.set("bye")
      print(a.get())

o = OptionMenu(root, oc, "yes", "no", command=function)
o.pack()


z = a.get()
print(z)

root.mainloop()