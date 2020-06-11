import menu
from tkinter import *


def requete(db, nom, muscle, nnom, description, image, nmuscle, canvas):
    nnom = nnom.get()
    description = description.get()
    image = image.get()
    nmuscle = nmuscle.get()

    cur = db.cursor()
    query = 'UPDATE exercice SET nom= ?, description= ?, image= ?, muscle=(SELECT ID FROM muscle where nom = ?) WHERE nom= ? AND muscle=(SELECT ID FROM muscle where nom = ?);'
    parametre = (nnom, description, image, nmuscle, nom, muscle)
    if nnom == "":
        canvas.itemconfigure(valider, text="Le nom de l'exercice ne peut pas être vide")
    else:
        try:
            cur.execute(query, parametre)
            db.commit()
            canvas.itemconfigure(valider, text="Vous avez modifié un exercice")
        except:
            canvas.itemconfigure(valider, text="ERROR: l'exercice n'a pas été modifié")

def modifier(db, muscle, nom, fenetre, canvas):

    if nom.get() == "exercice":
        raise Exception("Choisissez un exercice")

    global valider
    canvas.delete('all')
    fenetre.title('modifier exercice')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    canvas.create_text(300, 100, text="changez le nom de l'exercice :", font=("times new roman", 16))
    var_nom = StringVar()
    entry_nom = Entry(fenetre, exportselection=0, textvariable=var_nom, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(300, 150, window=entry_nom)

    canvas.create_text(800, 100, text="changez la description de l'exercice :", font=("times new roman", 16))
    var_description = StringVar()
    entry_description = Entry(fenetre, exportselection=0, textvariable=var_description, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(800, 150, window=entry_description)

    canvas.create_text(300, 300, text="changez l'image de l'exercice :", font=("times new roman", 16))
    var_image = StringVar()
    entry_image = Entry(fenetre, exportselection=0, textvariable=var_image, width=40, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(300, 350, window=entry_image)

    canvas.create_text(800, 300, text="changez le muscle de l'exercice :", font=("times new roman", 16))
    var_om = StringVar()
    listeOptions = ('abdominaux', 'biceps', 'dos', 'jambes', 'pectoraux', 'triceps')
    om = OptionMenu(fenetre, var_om, *listeOptions)
    om.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(800, 350, window=om)

    nom = nom.get()
    cur = db.cursor()
    query = 'SELECT exercice.nom, description, image, muscle.nom FROM exercice JOIN muscle ON exercice.muscle = muscle.ID WHERE exercice.nom= ? AND exercice.muscle=(SELECT ID FROM muscle where nom = ?)'
    parametre = (nom, muscle)
    cur.execute(query, parametre)
    for row in cur:
        var_nom.set(row[0])
        var_description.set(row[1])
        var_image.set(row[2])
        var_om.set(row[3])

    button = Button(fenetre, text="valider", command=lambda: requete(db, nom, muscle, var_nom, var_description, var_image, var_om, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 450, window=button)

    valider = canvas.create_text(550, 500, text="", font=("times new roman", 16), fill="red")

    menu.menu_footer(fenetre, canvas, db)


def exercice(db, choix, fenetre, canvas):
    global valider
    listeOptions = []
    choix = choix.get()

    if choix == "muscle":
        raise Exception("Choisissez un muscle")

    canvas.delete(can_but)

    canvas.create_text(550, 250, text="choisissez l'exercice a supprimer :", font=("times new roman", 16))

    cur = db.cursor()
    query = 'SELECT `nom` FROM exercice WHERE muscle=(SELECT ID FROM muscle WHERE nom= ?);'
    cur.execute(query, (choix, ))

    var_nom = StringVar()
    var_nom.set("exercice")
    for row in cur:
        str = ''.join(row)
        str.strip("(',)")
        listeOptions.append(str)

    liste_ex = OptionMenu(fenetre, var_nom, *listeOptions)
    liste_ex.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 300, window=liste_ex)

    button1 = Button(fenetre, text="valider", command=lambda: modifier(db, choix, var_nom, fenetre, canvas),  font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button1)


def muscle(db, fenetre, canvas):
    global can_but
    canvas.create_text(550, 150, text="choisissez le groupe musculaire :", font=("times new roman", 16))
    var_om = StringVar()
    var_om.set("muscle")
    listeOptions = ('abdominaux', 'biceps', 'dos', 'jambes', 'pectoraux', 'triceps')
    om = OptionMenu(fenetre, var_om, *listeOptions)
    om.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 200, window=om)

    button = Button(fenetre, text="valider", command=lambda: exercice(db, var_om, fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    can_but = canvas.create_window(550, 250, window=button)



def main(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('modifier exercice')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    muscle(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)