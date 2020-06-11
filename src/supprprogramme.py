import menu
from tkinter import *


def requete(db, nom, canvas):
    nom = nom.get()

    cur = db.cursor()
    query = 'DELETE FROM seance WHERE programme=(SELECT ID FROM programme WHERE nom = ?);'
    query2 = 'DELETE FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom = ?);'
    query3 = 'DELETE FROM programme WHERE nom= ?;'
    if nom == "programme":
        canvas.itemconfigure(valider, text="Veuillez choisir un programme")
    else:
        cur.execute(query, (nom, ))
        cur.execute(query2, (nom, ))
        cur.execute(query3, (nom, ))
        db.commit()
        canvas.itemconfigure(valider, text="Vous avez supprimé un programme")



def programme(db, fenetre, canvas):
    global valider
    listeOptions = []

    canvas.create_text(550, 250, text="choisissez le programme a supprimer :", font=("times new roman", 16))

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

    button = Button(fenetre, text="valider", command=lambda: requete(db, var_nom, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button)

    valider = canvas.create_text(550, 400, text="", font=("times new roman", 16), fill="red")


def main(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('supprimer programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    programme(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
