from tkinter import *
import menu

def apropos(db, fenetre, canvas):
    canvas.delete('all')
    fenetre.title('a propos')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()

    canvas.create_image(550, 300, image=image)
    canvas.create_text(550, 250, text="Cette petite application a été réalisée dans le cadre d'une veille technologique par Elouan Jeannot", font=("times new roman", 20))
    menu.menu_footer(fenetre, canvas, db)
