import menu
import accueil
from tkinter import *

def placement(db, nomprogramme, ligne, ordre, fenetre, canvas):
    nomprogramme = nomprogramme.get()

    cur4 = db.cursor()
    query4 = 'UPDATE programme_exercice SET ordre = ? WHERE ID = ? AND programme=(SELECT ID FROM programme WHERE nom= ?)'

    cur3 = db.cursor()
    query3 = 'SELECT ID FROM programme_exercice WHERE ordre = ? AND programme=(SELECT ID FROM programme WHERE nom= ?);'
    cur3.execute(query3, (ligne, nomprogramme))
    for row in cur3:
        id = row[0]

    cur2 = db.cursor()
    query2 = 'UPDATE programme_exercice SET ordre = ? WHERE ordre = ? AND programme=(SELECT ID FROM programme WHERE nom= ?)'

    cur = db.cursor()
    query = 'SELECT COUNT(*) FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom= ?);'
    cur.execute(query, (nomprogramme, ))
    for row in cur:
        if ligne == 1 and ordre == "avant" or ligne == row[0] and ordre == "après":
            set = ligne
            where = ligne
        elif ordre == "après":
            set = ligne
            where = ligne+1
        elif ordre == "avant":
            set = ligne
            where = ligne-1
    cur2.execute(query2, (set, where, nomprogramme))
    cur4.execute(query4, (where, id, nomprogramme))
    db.commit()

    afficherprogramme(db, nomprogramme, ligne, fenetre, canvas)



def supprimer(db, nomprogramme, ligne, fenetre, canvas):
    nomprogramme = nomprogramme.get()

    cur = db.cursor()
    query = 'DELETE FROM programme_exercice WHERE programme = (SELECT ID FROM programme WHERE nom = ?) AND ordre = ?'
    cur.execute(query, (nomprogramme, ligne))
    db.commit()

    cur2 = db.cursor()
    query2 = 'SELECT COUNT(*) FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom= ?);'
    cur2.execute(query2, (nomprogramme, ))

    cur3 = db.cursor()
    query3 = 'UPDATE programme_exercice SET ordre = ? WHERE ordre = ? AND programme=(SELECT ID FROM programme WHERE nom= ?);'

    for row in cur2:
        for i in range(ligne, row[0] + 1):
            set = i
            where = i + 1
            cur3.execute(query3, (set, where, nomprogramme))
            db.commit()
        var = row[0]+1
    print(var)
    print(ligne)
    if var == ligne:
        afficherprogramme(db, nomprogramme, ligne-1, fenetre, canvas)
    else:
        afficherprogramme(db, nomprogramme, ligne, fenetre, canvas)


def requetefinal(db, muscle, nomexercice, nomprogramme, nbreptemps, reptemps, pause, ligne, suite, canvas, fenetre):
    nbreptemps = nbreptemps.get()
    reptemps = reptemps.get()
    nomprogramme = nomprogramme.get()
    pause = pause.get()

    if reptemps == "repetition":
        nbrep = nbreptemps
        temps = "0"
    elif reptemps == "seconde":
        nbrep = "0"
        temps = nbreptemps
    else:
        canvas.itemconfigure(valider, text="Choisissez un temps ou un nombre de répetition")
        raise Exception("Choisissez un temps ou un nombre de répetition")

    cur2 = db.cursor()
    query2 = 'INSERT INTO `programme_exercice` (`programme`, `exercice`, `nombre_repetition`, `temps`, `pause`, `ordre`) VALUES ((SELECT ID FROM programme WHERE nom= ?), (SELECT ID FROM exercice WHERE nom= ? AND muscle=(SELECT ID FROM muscle WHERE nom = ?)), ?, ?, ?, ?)'
    cur3 = db.cursor()
    query3 = 'UPDATE programme_exercice SET ordre = ? WHERE ordre = ? AND programme=(SELECT ID FROM programme WHERE nom= ?)'

    cur4 = db.cursor()
    query4 = 'SELECT COUNT(*) FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom= ?);'
    cur4.execute(query4, (nomprogramme, ))

    for row in cur4:
        if suite == "suivant":
            iteration = row[0]
            parametre = (nomprogramme, nomexercice, muscle, nbrep, temps, pause, ligne + 1)
        else:
            iteration = row[0] + 1
            parametre = (nomprogramme, nomexercice, muscle, nbrep, temps, pause, ligne)
        var = row[0] + 1
        for i in range(ligne, iteration):
            set = var
            where = set - 1
            var = var - 1
            cur3.execute(query3, (set, where, nomprogramme))
            db.commit()

    cur2.execute(query2, parametre)
    db.commit()
    afficherprogramme(db, nomprogramme, ligne, fenetre, canvas)


def paramexercice(db, fenetre, muscle, nomexercice, nomprogramme, ligne, suite, canvas):
    nomexercice = nomexercice.get()
    global valider


    if nomexercice == "exercice":
        raise Exception("Choisissez un exercice")

    canvas.delete(canvas_button1)
    canvas.move(canvas_exo, -250, -200)
    canvas.move(canvas_liste_ex, -250, -200)
    canvas.move(canvas_muscle, 250, -100)
    canvas.move(canvas_om, 250, -100)

    canvas.create_text(300, 250, text="choisissez le nombre de répetition ou le temps :", font=("times new roman", 16))
    value_reptemps = IntVar()
    reptemps = Scale(fenetre, orient='horizontal', variable=value_reptemps, length=350, font=("times new roman", 14), background="#2FB5A3", activebackground="#59C38D", borderwidth=0, troughcolor="white")
    canvas.create_window(300, 300, window=reptemps)

    var_reptemps = StringVar()
    temps = Radiobutton(fenetre, text="durée de l'exercice", variable=var_reptemps, value="seconde", font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=17)
    rep = Radiobutton(fenetre, text="nombre de repetition", variable=var_reptemps, value="repetition", font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=17)
    canvas.create_window(300, 350, window=temps)
    canvas.create_window(300, 380, window=rep)

    canvas.create_text(800, 250, text="choisissez le temps de pause après l'exercice :", font=("times new roman", 16))
    var_pause = IntVar()
    pause = Scale(fenetre, orient='horizontal', variable=var_pause, length=350, font=("times new roman", 14), background="#2FB5A3", activebackground="#59C38D", borderwidth=0, troughcolor="white")
    canvas.create_window(800, 300, window=pause)

    button2 = Button(fenetre, text="valider", command=lambda: requetefinal(db, muscle, nomexercice, nomprogramme, value_reptemps, var_reptemps, var_pause, ligne, suite, canvas, fenetre), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 450, window=button2)

    valider = canvas.create_text(550, 500, text="", font=("times new roman", 16), fill="red")


def exercice(db, choix, fenetre, nomprogramme, ligne, suite, canvas):
    global canvas_button1
    global canvas_exo
    global canvas_liste_ex
    choix = choix.get()

    if choix == "muscle":
        raise Exception("Choisissez un muscle")

    listeOptions = []

    canvas.delete(canvas_button)

    canvas_exo = canvas.create_text(550, 300, text="choisissez l'exercice a ajouter au programme :", font=("times new roman", 16))

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
    canvas_liste_ex = canvas.create_window(550, 350, window=liste_ex)

    button1 = Button(fenetre, text="valider", command=lambda: paramexercice(db, fenetre, choix, var_nom, nomprogramme, ligne, suite, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_button1 = canvas.create_window(550, 400, window=button1)


def ajout(db, nomprogramme, ligne, suite, fenetre, canvas):
    global canvas_button
    global canvas_om
    global canvas_muscle

    canvas.delete('all')
    fenetre.title('ajouter exercice programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    canvas_muscle = canvas.create_text(550, 200, text="choisissez le groupe musculaire de l'exercice a ajouter :", font=("times new roman", 16))
    var_om = StringVar()
    var_om.set("muscle")
    listeOptions = ('abdominaux', 'biceps', 'dos', 'jambes', 'pectoraux', 'triceps')
    om = OptionMenu(fenetre, var_om, *listeOptions)
    om.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_om = canvas.create_window(550, 250, window=om)

    button = Button(fenetre, text="valider", command=lambda: exercice(db, var_om, fenetre, nomprogramme, ligne, suite, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    button.pack()
    canvas_button = canvas.create_window(550, 300, window=button)

    menu.menu_footer(fenetre, canvas, db)

def requete(db, nnomprogramme, nomprogramme, nomex, nbreptemps, reptemps, pause, ligne, suite, fenetre, canvas):
    nnomprogramme = nnomprogramme.get()
    nomex = nomex.get()
    nbreptemps = nbreptemps.get()
    reptemps = reptemps.get()
    pause = pause.get()

    if reptemps == "repetition":
        nbrep = nbreptemps
        temps = "0"
    elif reptemps == "seconde":
        nbrep = "0"
        temps = nbreptemps

    cur = db.cursor()
    query = 'UPDATE programme SET nom= ? WHERE nom= ?;'
    query2 = 'UPDATE programme_exercice SET exercice=(SELECT ID FROM exercice WHERE nom= ?), nombre_repetition= ?, temps= ?, pause= ? WHERE ordre= ? AND programme=(SELECT ID FROM programme WHERE nom = ?);'
    parametre2 = (nomex, nbrep, temps, pause, ligne, nnomprogramme)
    cur.execute(query, (nnomprogramme, nomprogramme))
    cur.execute(query2, parametre2)
    db.commit()

    if suite == "precedent":
        if ligne == 1:
            afficherprogramme(db, nnomprogramme, 1, fenetre, canvas)
        else:
            afficherprogramme(db, nnomprogramme, ligne-1, fenetre, canvas)
    elif suite == "suivant":
        cur = db.cursor()
        query = 'SELECT COUNT(*) FROM programme_exercice WHERE programme=(SELECT ID FROM programme WHERE nom= ?);'
        cur.execute(query, (nnomprogramme, ))
        for row in cur:
            test = row[0]
        if ligne == test:
            afficherprogramme(db, nnomprogramme, test, fenetre, canvas)
        else:
            afficherprogramme(db, nnomprogramme, ligne+1, fenetre, canvas)
    elif suite == "accueil":
        vbar = Scrollbar(fenetre, orient=VERTICAL)
        accueil.accueil(db, fenetre, canvas, vbar)


def afficherprogramme(db, nomprogramme, ligne, fenetre, canvas):
    if nomprogramme == "programme":
        main(db)
        raise Exception("Veuillez choisir un programme")

    var = ""
    canvas.delete('all')
    fenetre.title('modifier programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    canvas.create_text(550, 50, text="changez le nom du programme :", font=("times new roman", 16))
    var_nomprogramme = StringVar()
    entry_nomprogramme = Entry(fenetre, exportselection=0, textvariable=var_nomprogramme, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(550, 80, window=entry_nomprogramme)
    var_nomprogramme.set(nomprogramme)

    cur = db.cursor()
    query = 'SELECT nom, nombre_repetition, temps, pause, muscle FROM programme_exercice JOIN exercice ON programme_exercice.exercice = exercice.ID WHERE programme_exercice.programme=(SELECT ID FROM programme WHERE nom = ?) AND ordre = ?'
    cur.execute(query, (nomprogramme, ligne))

    for row in cur:
        var = row
    if var == "":
        aucunexercice = Button(fenetre, text="ajouter le premier exercice", command=lambda: ajout(db, var_nomprogramme, 0, "suivant"), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(550, 300, window=aucunexercice)
    else:
        cur.execute(query, (nomprogramme, ligne))
        for row in cur:
            listeOptions = []

            cur = db.cursor()
            query = 'SELECT nom FROM exercice WHERE muscle = ?'
            cur.execute(query, (row[4], ))
            for row1 in cur:
                listeOptions.append(row1[0])

            canvas.create_text(300, 150, text="changez le nom de l'exercice :", font=("times new roman", 16))
            var_nomex = StringVar()
            liste_ex = OptionMenu(fenetre, var_nomex, *listeOptions)
            liste_ex.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
            canvas.create_window(300, 200, window=liste_ex)
            var_nomex.set(row[0])

            canvas.create_text(800, 150, text="choisissez le nombre de répetition ou le temps :", font=("times new roman", 16))
            value_reptemps = IntVar()
            reptemps = Scale(fenetre, orient='horizontal', variable=value_reptemps, length=350, font=("times new roman", 14), background="#2FB5A3", activebackground="#59C38D", borderwidth=0, troughcolor="white")

            var_reptemps = StringVar()
            temps = Radiobutton(fenetre, text="durée de l'exercice", variable=var_reptemps, value="seconde", font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=17)
            rep = Radiobutton(fenetre, text="nombre de repetition", variable=var_reptemps, value="repetition", font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=17)

            if row[1] == 0:
                var_reptemps.set("seconde")
                value_reptemps.set(row[2])
            else:
                var_reptemps.set("repetition")
                value_reptemps.set(row[1])

            canvas.create_window(800, 200, window=reptemps)
            canvas.create_window(800, 250, window=temps)
            canvas.create_window(800, 280, window=rep)

            var_pause = IntVar()
            canvas.create_text(300, 250, text="choisissez le temps de pause après l'exercice :", font=("times new roman", 16))
            pause = Scale(fenetre, orient='horizontal', variable=var_pause, length=350, font=("times new roman", 14), background="#2FB5A3", activebackground="#59C38D", borderwidth=0, troughcolor="white")
            var_pause.set(row[3])
            canvas.create_window(300, 300, window=pause)

        buttonprecedent = Button(fenetre, text="Precedent", command=lambda: requete(db, var_nomprogramme, nomprogramme, var_nomex, value_reptemps, var_reptemps, var_pause, ligne, "precedent", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=10)
        canvas.create_window(200, 50, window=buttonprecedent)

        buttonsuivant = Button(fenetre, text="Suivant", command=lambda: requete(db, var_nomprogramme, nomprogramme, var_nomex, value_reptemps, var_reptemps, var_pause, ligne, "suivant", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=10)
        canvas.create_window(900, 50, window=buttonsuivant)

        buttonajoutprecedent = Button(fenetre, text="ajouter un exercice avant celui-ci", command=lambda: ajout(db, var_nomprogramme, ligne, "precedent", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(300, 450, window=buttonajoutprecedent)

        buttonajoutsuivant = Button(fenetre, text="ajouter un exercice après celui-ci", command=lambda: ajout(db, var_nomprogramme, ligne, "suivant", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(800, 450, window=buttonajoutsuivant)

        buttonsuppr = Button(fenetre, text="supprimer cet exercice du programme", command=lambda: supprimer(db, var_nomprogramme, ligne, fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(550, 400, window=buttonsuppr)

        buttonplaceprecedent = Button(fenetre, text="placer cet exercice avant", command=lambda: placement(db, var_nomprogramme, ligne, "avant", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(300, 500, window=buttonplaceprecedent)

        buttonplacesuivant = Button(fenetre, text="placer cet exercice après", command=lambda: placement(db, var_nomprogramme, ligne, "après", fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3", width=30)
        canvas.create_window(800, 500, window=buttonplacesuivant)

        buttonhome = Button(fenetre, text="Terminer", command=lambda: [requete(db, var_nomprogramme, nomprogramme, var_nomex, value_reptemps, var_reptemps, var_pause, ligne, "accueil", fenetre, canvas)], font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
        canvas.create_window(550, 475, window=buttonhome)

    menu.menu_footer(fenetre, canvas, db)


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

    button1 = Button(fenetre, text="valider", command=lambda: afficherprogramme(db, var_nom.get(), 1, fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button1)


def main(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('modifier programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    programme(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
