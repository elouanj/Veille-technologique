from tkinter import *
import accueil
from pysqlcipher3 import dbapi2 as sqlcipher


def connexion(db, fenetre, canvas, password):
    password = password.get()
    query = "pragma key=\""+str(password)+"\""
    db.execute(query)
    cur = db.cursor()
    query2 = 'SELECT * FROM exercice;'
    try:
        cur.execute(query2)
        vbar = Scrollbar(fenetre, orient=VERTICAL)
        accueil.accueil(db, fenetre, canvas, vbar)
    except:
        canvas.itemconfigure(valider, text="Le mot de passe ne correspond pas")


def app_connexion():
    global valider

    db = sqlcipher.connect('DB/musculation.db')

    fenetre = Tk()
    fenetre.resizable(0, 0)
    fenetre.title('connexion')
    image = PhotoImage(file='image/fond.gif', master=fenetre)
    canvas = Canvas(fenetre, width=1100, height=600)
    canvas.pack()

    canvas.create_image(550, 300, image=image)


    canvas.create_text(550, 240, text="mot de passe :", font=("times new roman", 16))
    var_password = StringVar()
    entry_password = Entry(fenetre, show="*", exportselection=0, textvariable=var_password, width=30, font=("times new roman", 14), borderwidth=0)
    canvas.create_window(550, 270, window=entry_password)

    button = Button(fenetre, text="valider", command=lambda: connexion(db, fenetre, canvas, var_password), width=10, font=("times new roman", 14), background="#59C38D", borderwidth=0, activebackground="#2FB5A3")
    canvas.create_window(550, 350, window=button)

    valider = canvas.create_text(550, 400, text="", font=("times new roman", 16), fill="red")

    fenetre.mainloop()
