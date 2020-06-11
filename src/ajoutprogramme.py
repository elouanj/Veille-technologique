import menu
import accueil
from tkinter import *


def requetefinal(db, muscle, nomexercice, nomprogramme, nbreptemps, reptemps, pause, canvas, fenetre):
    nbreptemps = nbreptemps.get()
    reptemps = reptemps.get()
    pause = pause.get()

    if reptemps == "repetition":
        nbrep = nbreptemps
        temps = "0"
    elif reptemps == "seconde":
        nbrep = "0"
        temps = nbreptemps
    else:
        canvas.itemconfigure(valider2, text="Choisissez un temps ou un nombre de répetition")
        raise Exception("Choisissez un temps ou un nombre de répetition")

    cur = db.cursor()
    query ='SELECT MAX(ordre) FROM programme_exercice WHERE programme = (SELECT ID FROM programme WHERE nom= ?)'
    cur.execute(query, (nomprogramme, ))
    for row in cur:
        if row[0] == None:
            ordre = 1
        else:
            ordre=row[0]+1

    cur2 = db.cursor()
    query2 = 'INSERT INTO `programme_exercice` (`programme`, `exercice`, `nombre_repetition`, `temps`, `pause`, `ordre`) VALUES ((SELECT ID FROM programme WHERE nom= ?), (SELECT ID FROM exercice WHERE nom= ? AND muscle=(SELECT ID FROM muscle WHERE nom = ?)), ?, ?, ?, ?)'
    parametre = (nomprogramme, nomexercice, muscle, nbrep, temps, pause, ordre)
    try:
        cur2.execute(query2, parametre)
        db.commit()
        textvalider = "Vous avez ajouté un exercice au programme"
    except:
        textvalider = "ERROR: l'exercice n'a pas été ajouté au programme"
    choixmuscle(db, nomprogramme, textvalider, fenetre, canvas)


def paramexercice(db, fenetre, muscle, nomexercice, nomprogramme, canvas):
    global valider2

    if nomexercice.get() == "exercice":
        raise Exception("Choisissez un exercice")

    nomexercice = nomexercice.get()
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

    button2 = Button(fenetre, text="valider", command=lambda: requetefinal(db, muscle, nomexercice, nomprogramme, value_reptemps, var_reptemps, var_pause, canvas, fenetre), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 450, window=button2)

    valider2 = canvas.create_text(550, 500, text="", font=("times new roman", 16), fill="red")

def exercice(db, choix, fenetre, nomprogramme, canvas):
    global canvas_button1
    global canvas_exo
    global canvas_liste_ex
    listeOptions = []
    choix = choix.get()

    if choix == "muscle":
        choixmuscle(db, nomprogramme, "Veuillez choisir un muscle", fenetre, canvas)

    canvas.delete(canvas_button)
    canvas.delete(canvas_valider)

    canvas_exo = canvas.create_text(550, 300, text="choisissez l'exercice a ajouter au programme :", font=("times new roman", 16))

    cur = db.cursor()
    query = 'SELECT `nom` FROM exercice WHERE muscle=(SELECT ID FROM muscle WHERE nom= ?);'
    cur.execute(query, (choix, ))

    var_nom = StringVar()
    var_nom.set("exercice")
    for row in cur:
        listeOptions.append(row[0])

    liste_ex = OptionMenu(fenetre, var_nom, *listeOptions)
    liste_ex.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_liste_ex = canvas.create_window(550, 350, window=liste_ex)

    button1 = Button(fenetre, text="valider", command=lambda: paramexercice(db, fenetre, choix, var_nom, nomprogramme, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_button1 = canvas.create_window(550, 400, window=button1)



def choixmuscle(db, nomprogramme, textvalider, fenetre, canvas):
    global canvas_button
    global canvas_valider
    global canvas_om
    global canvas_muscle

    canvas.delete('all')
    fenetre.title('ajouter exercice au programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    vbar = Scrollbar(fenetre, orient=VERTICAL)
    button_accueil = Button(fenetre, text="Ne pas ajouter de nouvel exercice", command=lambda: accueil.accueil(db, fenetre, canvas, vbar), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 50, window=button_accueil)

    canvas_muscle = canvas.create_text(550, 200, text="choisissez le groupe musculaire de l'exercice a ajouter :", font=("times new roman", 16))
    var_om = StringVar()
    var_om.set("muscle")
    listeOptions = ('abdominaux', 'biceps', 'dos', 'jambes', 'pectoraux', 'triceps')
    om = OptionMenu(fenetre, var_om, *listeOptions)
    om.config(font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_om = canvas.create_window(550, 250, window=om)

    button = Button(fenetre, text="valider", command=lambda: exercice(db, var_om, fenetre, nomprogramme, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas_button = canvas.create_window(550, 300, window=button)

    canvas_valider = canvas.create_text(550, 350, text=textvalider, font=("times new roman", 16), fill="red")

    menu.menu_footer(fenetre, canvas, db)


def requeteprogramme(db, nom, canvas):
    var = ""
    nom = nom.get()
    cur = db.cursor()
    query = 'SELECT nom FROM programme WHERE nom= ?'
    cur.execute(query, (nom,))
    for row in cur:
        var = row[0]
    if var != "":
        canvas.itemconfigure(valider, text="Le programme existe déjà")
        raise Exception("Le programme existe déjà")
    else:
        cur2 = db.cursor()
        query = 'INSERT INTO programme (nom) VALUES (?)'
        cur2.execute(query, (nom, ))
        db.commit()


def ajouter(db, fenetre, canvas):
    global valider
    canvas.create_text(550, 200, text="choisissez le nom du programme :", font=("times new roman", 16))
    var_nom = StringVar()
    entry_nom = Entry(fenetre, exportselection=0, textvariable=var_nom, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(550, 250, window=entry_nom)

    button = Button(fenetre, text="valider", command=lambda: [requeteprogramme(db, var_nom, canvas), choixmuscle(db, var_nom.get(), "", fenetre, canvas)], font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 300, window=button)

    valider = canvas.create_text(550, 350, text="", font=("times new roman", 16), fill="red")


def main(db, fenetre, canvas, vbar):
    vbar.forget()
    canvas.delete('all')
    fenetre.title('ajouter programme')

    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    ajouter(db, fenetre, canvas)

    menu.menu_footer(fenetre, canvas, db)
