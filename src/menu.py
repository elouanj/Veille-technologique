from tkinter import *
import table
import apropos
import accueil
import demarrer
import seance
import ajoutexercice
import supprexercice
import modifexercice
import ajoutprogramme
import supprprogramme
import modifprogramme

def menu_header(fenetre, db, canvas, vbar):
    font = ("times new roman", 14)

    mainmenu = Menu(fenetre, background="#59C38D", font=font, activebackground="#2FB5A3", relief="flat")

    mtable = Menu(mainmenu, tearoff=0, activebackground="#2FB5A3", background="#59C38D", font=font, relief="flat")
    mtable.add_command(label="abdominaux", command=lambda choix="abdominaux": table.table(db, choix, fenetre, canvas, vbar))
    mtable.add_command(label="pectoraux", command=lambda choix="pectoraux": table.table(db, choix, fenetre, canvas, vbar))
    mtable.add_command(label="dos", command=lambda choix="dos": table.table(db, choix, fenetre, canvas, vbar))
    mtable.add_command(label="biceps", command=lambda choix="biceps": table.table(db, choix, fenetre, canvas, vbar))
    mtable.add_command(label="triceps", command=lambda choix="triceps": table.table(db, choix, fenetre, canvas, vbar))
    mtable.add_command(label="jambes", command=lambda choix="jambes": table.table(db, choix, fenetre, canvas, vbar))

    mupdateexercise = Menu(mainmenu, tearoff=0, activebackground="#2FB5A3", background="#59C38D", font=font, relief="flat")
    mupdateexercise.add_command(label="ajouter exercice", command=lambda: ajoutexercice.main(db, fenetre, canvas, vbar))
    mupdateexercise.add_command(label="supprimer exercice", command=lambda: supprexercice.main(db, fenetre, canvas, vbar))
    mupdateexercise.add_command(label="modifier exercice", command=lambda: modifexercice.main(db, fenetre, canvas, vbar))

    mupdateprogram = Menu(mainmenu, tearoff=0, activebackground="#2FB5A3", background="#59C38D", font=font, relief="flat")
    mupdateprogram.add_command(label="ajouter programme", command=lambda: ajoutprogramme.main(db, fenetre, canvas, vbar))
    mupdateprogram.add_command(label="supprimer programme", command=lambda: supprprogramme.main(db, fenetre, canvas, vbar))
    mupdateprogram.add_command(label="modifier programme", command=lambda: modifprogramme.main(db, fenetre, canvas, vbar))

    mainmenu.add_command(label="accueil", font=font, command=lambda: accueil.accueil(db, fenetre, canvas, vbar))
    mainmenu.add_cascade(label="table", font=font, menu=mtable)
    mainmenu.add_cascade(label="exercice", font=font, menu=mupdateexercise)
    mainmenu.add_cascade(label="programme", font=font, menu=mupdateprogram)

    mainmenu.add_command(label="seance", command=lambda: seance.seance(db, fenetre, canvas, vbar))

    mainmenu.add_command(label="démarrer", command=lambda: demarrer.demarrer(db, fenetre, canvas, vbar))

    fenetre.config(menu=mainmenu)


def menu_footer(fenetre, canvas, db):
    canvas.create_line(0, 540, 1100, 540)
    quitter = Button(fenetre, text="Quitter", command=lambda: [fenetre.destroy(), sys.exit(0)], font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(200, 570, window=quitter)
    propos = Button(fenetre, text="A propos", command=lambda: apropos.apropos(db, fenetre, canvas), font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(900, 570, window=propos)

    fenetre.mainloop()
