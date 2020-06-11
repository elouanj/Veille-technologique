import menu
import accueil
from tkinter import *
from time import *
from PIL import Image
from resizeimage import resizeimage


def requete(db, temps, date, nomprogramme, fenetre, canvas):
    cur = db.cursor()
    query = 'INSERT INTO seance (programme, dateseance, temps) VALUES ((SELECT ID FROM programme WHERE nom = ?), ?, ?)'
    parametre = (nomprogramme, date, temps)
    cur.execute(query, parametre)
    db.commit()
    vbar = Scrollbar(fenetre, orient=VERTICAL)
    accueil.accueil(db, fenetre, canvas, vbar)



def terminer(datedebut, nomprogramme, db, fenetre, canvas):
    canvas.delete('all')
    fenetre.title('terminer')
    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas.pack()
    canvas.create_image(550, 300, image=image)

    datefin = time()

    tempsecoulle = int((datefin - datedebut))
    seconde = tempsecoulle
    minute = 0

    if tempsecoulle >= 60:
        seconde = (tempsecoulle % 60)
        minute = tempsecoulle // 60

    temps = str(minute)+" min "+str(seconde)+" sec"
    texttemps = "Vous avez mis " + str(minute)+" minutes et " + str(seconde) + " secondes"
    date = strftime("%A %d %B %Y %H:%M")
    textdate = "Nous sommes le " + str(date)

    canvas.create_text(550, 100, text=textdate, font=("times new roman", 18))
    canvas.create_text(550, 200, text=texttemps, font=("times new roman", 18))

    button = Button(fenetre, text="Terminer", command=lambda: requete(db, temps, date, nomprogramme, fenetre, canvas), font=("times new roman", 20), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 500, window=button)

    menu.menu_footer(fenetre, canvas, db)

    fenetre.mainloop()


def updatepause(pause, timer, canvas, fenetre, db, ordre, nomprogramme, datedebut):
    var = "il vous reste \n"+str(pause)+"\n secondes de pause"
    canvas.itemconfigure(timer, text=var)
    if pause >= 1:
        fenetre.after(1000, lambda: updatepause(pause-1, timer, canvas, fenetre, db, ordre, nomprogramme, datedebut))
    else:
        afficher(nomprogramme, db, fenetre, canvas, ordre+1, datedebut)

def afficherpause(pause, db, fenetre, canvas, ordre, nomprogramme, datedebut):
    if pause > 0:
        canvas.delete('all')
        fenetre.title('pause')
        image = PhotoImage(file='image/fond.gif', master=fenetre)
        canvas.pack()
        canvas.create_image(550, 300, image=image)

        timer = canvas.create_text(550, 300, text="", font=("times new roman", 26), justify=CENTER)
        updatepause(pause, timer, canvas, fenetre, db, ordre, nomprogramme, datedebut)

        menu.menu_footer(fenetre, canvas, db)
    else:
        afficher(nomprogramme, db, fenetre, canvas, ordre + 1, datedebut)


def updatetime(db, temps, timer, canvas, fenetre, pause, ordre, nomprogramme, datedebut):
    var = "il vous reste \n"+str(temps)+"\n secondes"
    canvas.itemconfigure(timer, text=var)
    if temps >= 1:
        fenetre.after(1000, lambda: updatetime(db, temps-1, timer, canvas, fenetre, pause, ordre, nomprogramme, datedebut))
    else:
        afficherpause(pause, db, fenetre, canvas, ordre, nomprogramme, datedebut)


def afficher(nomprogramme, db, fenetre, canvas, ordre, datedebut):
    cur = db.cursor()
    query = 'SELECT exercice.nom, exercice.description, exercice.image, muscle.nom, programme_exercice.nombre_repetition, programme_exercice.temps, programme_exercice.pause FROM programme_exercice JOIN exercice ON programme_exercice.exercice = exercice.ID JOIN muscle ON exercice.muscle = muscle.ID WHERE programme = (SELECT ID FROM programme WHERE nom = ?) AND ordre= ?'
    try:
        cur.execute(query, (nomprogramme, ordre))
        for var in cur:
            row = var
        canvas.delete('all')
        fenetre.title('lire programme')
        image = PhotoImage(file='image/fond.gif', master=fenetre)
        canvas.pack()
        canvas.create_image(550, 300, image=image)

        canvas.create_text(550, 50, text=row[0], font=("times new roman", 18))
        canvas.create_text(550, 100, text=row[1], font=("times new roman", 14))

        cheminimage = "image/" + str(row[2]) + ".gif"
        try:
            im = Image.open(cheminimage)
        except:
            im = Image.open("image/default.gif")

        if im.size[1] >= 235:
            cover = resizeimage.resize_height(im, 235)
            cover.save(cheminimage, im.format)
        imageexercice = PhotoImage(file=cheminimage, master=fenetre)
        canvas.create_image(550, 235, image=imageexercice)

        if row[5] != 0:
            timer = canvas.create_text(550, 450, text="", font=("times new roman", 18), justify=CENTER)
            updatetime(db, row[5], timer, canvas, fenetre, row[6], ordre, nomprogramme, datedebut)
            menu.menu_footer(fenetre, canvas, db)

        elif row[4] != 0:
            repetition = "Vous devez faire \n " + str(row[4]) + " \n repetitions pour terminer l'exercice"
            canvas.create_text(550, 400, text=repetition, font=("times new roman", 18), justify=CENTER)

            button = Button(fenetre, text="Passer à l'exercice suivant",
                            command=lambda: afficherpause(row[6], db, fenetre, canvas, ordre, nomprogramme, datedebut),
                            font=("times new roman", 20), background="#59C38D", borderwidth=0,
                            activebackground="#2FB5A3")
            canvas.create_window(550, 500, window=button)
            menu.menu_footer(fenetre, canvas, db)

        else:
            afficherpause(row[6], db, fenetre, canvas, ordre, nomprogramme, datedebut)
            menu.menu_footer(fenetre, canvas, db)
    except:
        terminer(datedebut, nomprogramme, db, fenetre, canvas)


def main(db, nomprogramme, fenetre, canvas):
    datedebut = time()
    afficher(nomprogramme, db, fenetre, canvas, 1, datedebut)
