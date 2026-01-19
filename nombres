'''
à partir de la liste de solutions, donne le nombre de cases à remplir par colonne et par ligne
'''
import tkinter as tk

#par colonne 
def nombre_colonne(liste_solution) :
    liste = []
    for i in range (len(liste_solution)):
        l = []
        k = 0
        for j in range (len(liste_solution)) :
            if liste_solution[j][i] == 1 : 
                k += 1
            elif k > 0: 
                l.append(k)
                k = 0
        if k > 0 : 
            l.append(k)
        liste.append(l)
    return liste 

#par ligne
def nombre_ligne(liste_solution) :
    liste = []
    for i in liste_solution: 
        l = []
        k = 0
        for j in range (len(i)):
            if i[j] == 1 :
                k += 1 
            elif k != 0: 
                l.append(k)
                k = 0
            
            if j == len(i) - 1 and i[j] != 0 : 
                    l.append(k)
                    k = 0 
        liste.append(l)
    return liste


def afficher_nb_col(self):
    nb_col = nombre_colonne(self.liste_solution)
    fond = tk.Label(self.master, bg="Light goldenrod",height = 1, width=71)
    fond.place(x=100, y=49)
    for i in range(len(nb_col)): 
        texte = ""
        for nombre in nombre_colonne(self.liste_solution)[i]:
            if texte == "":
                texte = str(nombre)
            else:
                texte = texte + " " + str(nombre)
        label = tk.Label(
                self.master, 
                text = texte,
                bg="Light goldenrod", 
                font=("Arial", 9))
        x = 100 + i * self.taille_case 
        label.place(x=x, y=49)

def afficher_nb_lig(self):
    nb_lig = nombre_ligne(self.liste_solution)
    fond = tk.Label(self.master, bg="Light goldenrod",height = 33, width=7)
    fond.place(x=46, y=70)
    for i in range(len(nb_lig)): 
        texte = ""
        for nombre in nombre_ligne(self.liste_solution)[i]:
            if texte == "":
                texte = str(nombre)
            else:
                texte = texte + " " + str(nombre)
        label = tk.Label(
                self.master, 
                text = texte,                    
                bg="Light goldenrod", 
                font=("Arial", 9))
        y = 70 + i * self.taille_case + int(self.taille_case//2.8)
        label.place(x=46, y=y)
