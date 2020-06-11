import menu
import lireprogramme
from tkinter import *


def programme(db, fenetre, canvas):
    listeOptions = []

    canvas.create_text(550, 250, text="choisissez le programme a modifier :", font=("times new roman", 16))

    cur = db.cursor()
    query = 'SELECT nom FROM programme'
    cur.execute(query)

    var_nom = StringVar()
    var_nom.set("programme")
    for row in cur:
        listeOptions.append(row[0])

    liste_ex = OptionMenu(fenetre, var_nom, *listeOptions)
    liste_ex.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 300, window=liste_ex)

    button1 = Button(fenetre, text="valider", command=lambda: lireprogramme.main(db, var_nom.get(), fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button1)



def demarrer(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('demarrer')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    programme(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
