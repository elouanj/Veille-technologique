import menu
from tkinter import *


def accueil(db, fenetre, canvas, vbar):
    vbar.forget()
    fenetre.title('accueil')
    canvas.delete('all')
    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.create_image(550, 300, image=image)

    menu.menu_header(fenetre, db, canvas, vbar)
    canvas.create_text(550, 250, text="Bienvenue dans l'application de sport à la maison", font=("times new roman", 20))
    menu.menu_footer(fenetre, canvas, db)
