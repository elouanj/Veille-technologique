import menu
from tkinter import *

def replacer(db, nom):
    cur = db.cursor()
    query = 'SELECT DISTINCT nom FROM programme JOIN programme_exercice ON programme.ID = programme_exercice.programme WHERE programme_exercice.exercice = (SELECT ID FROM exercice WHERE nom = ?);'
    cur.execute(query, (nom, ))

    for row in cur:
        cur4 = db.cursor()
        query4 = 'SELECT ordre FROM programme_exercice WHERE exercice=(SELECT ID FROM exercice WHERE nom = ?) AND programme=(SELECT ID FROM programme WHERE nom= ?)'
        cur4.execute(query4, (nom, row[0]))
        for row2 in cur4:
            ligne = row2[0]

            cur5 = db.cursor()
            query5 = 'DELETE FROM programme_exercice WHERE programme = (SELECT ID FROM programme WHERE nom = ?) AND ordre = ?'
            cur5.execute(query5, (row[0], ligne))

            cur2 = db.cursor()
            query2 = 'SELECT COUNT(*) FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom= ?);'
            cur2.execute(query2, (row[0], ))

            cur3 = db.cursor()
            query3 = 'UPDATE programme_exercice SET ordre = ? WHERE ordre = ? AND programme=(SELECT ID FROM programme WHERE nom= ?);'

            for row1 in cur2:
                for i in range(ligne, row1[0] + 1):
                    set = i
                    where = i + 1
                    cur3.execute(query3, (set, where, row[0]))
            cur4.execute(query4, (nom, row[0]))

def requete(db, choix, nom, canvas):
    nom = nom.get()

    cur2 = db.cursor()
    query2 = 'DELETE FROM exercice WHERE nom= ? AND muscle=(SELECT ID FROM muscle where nom = ?);'
    parametre2 = (nom, choix)
    if nom == "exercice":
        canvas.itemconfigure(valider, text="Veuillez choisir un exercice")
    else:
        try:
            replacer(db, nom)
            cur2.execute(query2, parametre2)
            db.commit()
            canvas.itemconfigure(valider, text="Vous avez supprimé un exercice")
        except:
            canvas.itemconfigure(valider, text="L'exercice n'a pas été supprimé")


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
        listeOptions.append(row[0])

    liste_ex = OptionMenu(fenetre, var_nom, *listeOptions)
    liste_ex.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 300, window=liste_ex)

    button1 = Button(fenetre, text="valider", command=lambda: requete(db, choix, var_nom, canvas),  font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button1)

    valider = canvas.create_text(550, 400, text="", font=("times new roman", 16), fill="red")


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
    fenetre.title('supprimer exercice')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    muscle(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
