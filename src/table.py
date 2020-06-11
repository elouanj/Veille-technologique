from tkinter import *

def table(db, choix, fenetre, canvas, vbar):
    canvas.delete('all')
    fenetre.title('table')
    scrool = 0
    limite = 600
    hauteur = 300
    i=2

    cur2 = db.cursor()
    query2 = 'SELECT count(*) FROM exercice WHERE muscle=(SELECT ID FROM muscle WHERE nom=?);'
    cur2.execute(query2, (choix,))

    for row in cur2:
        scrool=row[0]*50+50

    image = PhotoImage(file='image/fond.gif', master=fenetre)

    canvas.config(scrollregion=(0, 0, scrool, scrool))
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)
    canvas.create_image(550, hauteur, image=image)

    while scrool > limite:
        hauteur = hauteur + 600
        canvas.create_image(550, hauteur, image=image)
        i = i + 1
        limite = limite + 600

    cur = db.cursor()
    query = 'SELECT `nom`, `description`, `image` FROM exercice WHERE muscle=(SELECT ID FROM muscle WHERE nom=?);'
    cur.execute(query, (choix,))

    colonne = 1100*(1/3)

    canvas.create_text(colonne/2, 25, text="Nom de l'exercice", font=("times new roman", 16))
    canvas.create_line(colonne, 0, colonne, 50)
    canvas.create_text(colonne + colonne/2, 25, text="Description", font=("times new roman", 16))
    canvas.create_line(colonne*2, 0, colonne*2, 50)
    canvas.create_text(colonne*2 + colonne/2, 25, text="Image", font=("times new roman", 16))
    canvas.create_line(0, 50, 1100, 50)

    hauteur = 50
    for row in cur:
        hauteur = hauteur + 50
        largeur = 1100*(1/3)/2
        colonne = 1100*(1/3)
        canvas.create_line(0, hauteur, 1100, hauteur)
        for i in row:
            canvas.create_text(largeur, hauteur-25, text=i, font=("times new roman", 16))
            canvas.create_line(colonne, hauteur-50, colonne, hauteur)
            colonne = colonne * 2
            largeur = largeur + 1100*(1/3)

    fenetre.mainloop()
    vbar.forget()
