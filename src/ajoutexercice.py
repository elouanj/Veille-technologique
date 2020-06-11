import menu
from tkinter import *


def requete(db, choix, nom, description, image, canvas):
    choix = choix.get()
    nom = nom.get()
    description = description.get()
    image = image.get()
    cur = db.cursor()
    query = 'INSERT INTO exercice (nom, description, image, muscle) VALUES (?, ?, ?, (SELECT ID FROM muscle where nom = ?)) ;'
    parametre = (nom, description, image, choix)
    query2 = 'SELECT COUNT(*) FROM exercice WHERE nom = ?'
    cur.execute(query2, (nom,))
    for row in cur:
        var = row[0]
    if var != 0:
        canvas.itemconfigure(valider, text="Le nom de l'exercice est déjà pris")
    elif choix == "muscle":
        canvas.itemconfigure(valider, text="Veuillez choisir un muscle")
    else:
        try:
            cur.execute(query, parametre)
            db.commit()
            canvas.itemconfigure(valider, text="Vous avez ajouté un exercice")
        except:
            canvas.itemconfigure(valider, text="ERROR: l'exercice n'a pas été ajouté")


def ajouter(db, fenetre, canvas):
    global valider

    canvas.create_text(300, 100, text="choisissez le groupe musculaire :", font=("times new roman", 16))
    var_om = StringVar()
    var_om.set("muscle")
    listeOptions = ('abdominaux', 'biceps', 'dos', 'jambes', 'pectoraux', 'triceps')
    om = OptionMenu(fenetre, var_om, *listeOptions)
    om.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(300, 150, window=om)

    canvas.create_text(800, 100, text="choisissez le nom de l'exercice :", font=("times new roman", 16))
    var_nom = StringVar()
    entry_nom = Entry(fenetre, exportselection=0, textvariable=var_nom, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(800, 150, window=entry_nom)

    canvas.create_text(300, 300, text="faites une courte description de l'exercice :", font=("times new roman", 16))
    var_description = StringVar()
    entry_description = Entry(fenetre, exportselection=0, textvariable=var_description, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(300, 350, window=entry_description)

    canvas.create_text(800, 300, text="ajoutez le nom de image de l'exercice :", font=("times new roman", 16))
    var_image = StringVar()
    entry_image = Entry(fenetre, exportselection=0, textvariable=var_image, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(800, 350, window=entry_image)
    canvas.create_text(800, 375, text="L'image doit etre en .gif et doit etre dans le dossier image", font=("times new roman", 12))

    button = Button(fenetre, text="valider", command=lambda: requete(db, var_om, var_nom, var_description, var_image, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 450, window=button)

    valider = canvas.create_text(550, 500, text="", font=("times new roman", 16), fill="red")


def main(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('ajouter exercice')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    ajouter(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
