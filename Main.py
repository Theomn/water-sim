from View import *

root = Tk()
main = View(root)

while True:
    root.update_idletasks()
    root.update()
    main.update()
    main.render()
    root.after(1)
