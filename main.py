'''
Picross 
Auteurs : Matis Zhang et Adèle Havard
Date : jsp
Jeu dans une grille où on doit remplir ou non des cases 
en respectant un nombre prédéfini par colonne et par ligne
Entrées : les cases cochées par l'utilisateur
Réslutat : indique si une erreur est faite et annonce la victoire 
'''
import tkinter as tk
from tkinter import messagebox 
import random

class FenetrePrincipale:    # Initialisation de la fenêtre principale
    def __init__(self, master):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")    #titre de la fenêtre
        master.geometry("900x900")    #taille de la fenêtre
        master.resizable(True, True)     #autorise ou non le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")    #couleur du fond

        # Création de la grille de jeu
        self.grille = Grille_de_jeux(master)

    # Lancement de la boucle principale
    def run(self):
        self.master.mainloop()


class Grille_de_jeux:
    def __init__(self, master):
        self.master = master

        self.label_vies = tk.Label(master, text =f"Vies : {self.nb_vies}", bg="White", font=("Arial", 15)) #affiche le nombre de vies
        self.label_vies.grid (row=0, column=0, padx=800, pady=50) #position du label

        # Canvas
        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")    #taille et couleur de la grille
        self.canvas.place(x=200, y=100)    #écart entre le haut et le côté gauche de la fenêtre avec la grille

        # Valeur par défaut
        self.cases = 10    #nombre de cases par côté
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        #dict pour stocker l'état des cases
        self.etats_cases = {} 

        # Dessin initial
        self.dessiner_grille()
        self.liste_solution = self.creation_liste(self.cases)
        #self.afficher_liste()

        # Lie le clic gauche et le clic droit à leur fonction
        self.canvas.bind("<Button-1>", self.clic_case_gauche)
        self.canvas.bind("<Button-3>", self.clic_case_droit)
        
    # --- FONCTION CLÉ ---
    def set_cases(self, nb_cases):
        """
        Cette fonction sera appelée par un bouton
        pour changer le nombre de cases.
        """
        self.cases = nb_cases    #nombre de cases par côté
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        # Nettoyage du canvas
        self.canvas.delete("all") #enlève la grille qu'il y avait avant

        # Redessin
        self.dessiner_grille()    #remet une grille avec le nombre de cases demandé

    def dessiner_grille(self):
        for col in range(self.cases):
            for lig in range(self.cases):
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="grey", fill="white"
                )
                #on stocke l'ID de la case (vide et sans croix)
                self.etats_cases[(col, lig)] = {
                    "rect": rect,
                    "etat": 0   }

    nb_vies = 3 #nombre de vies initial

    #Inverse la couleur de la case cliquée
    def clic_case_gauche(self, event): 
        #coordonnées de la case cliquée
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case

        case = self.etats_cases[(col, lig)] 

        if case["etat"] == 0:   #si la case est vide 
            if self.liste_solution[col][lig] == 1 and self.nb_vies > 0:#si c'est la bonne réponse et qu'on a encore des vies
                self.canvas.itemconfig(case["rect"], fill="black") #on remplit la case
                case["etat"] = 1 # on met à jour l'état de la case
            else : 
                if self.nb_vies >= 1 : #si on a encore des vies on en enlève une
                    self.nb_vies -= 1 
                    self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                    if self.nb_vies == 0 :  # si on a plus de vies on perd
                        messagebox.showinfo(None, "Vous avez perdu")
                        messagebox.OK = 'ok'
                    

    # Clic droit : mettre / enlever une croix
    def clic_case_droit(self, event):
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case

        case = self.etats_cases[(col, lig)]

        if case["etat"] == 0:  # Si la case est déja remplie on met rien
            if self.liste_solution[col][lig] == 0 and self.nb_vies > 0 :#si c'est la bonne réponse et qu'on a encore des vies
                #on dessine une croix dans la case :
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
            
                # deux lignes en diagonale
                l1 = self.canvas.create_line(x1+3, y1+3, x2-3, y2-3, fill="red", width=2)
                l2 = self.canvas.create_line(x1+3, y2-3, x2-3, y1+3, fill="red", width=2)
                case["etat"] = 1
            else : 
                if self.nb_vies >= 1 : #si on a encore des vies on en enlève une
                    self.nb_vies -= 1 
                    self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                    if self.nb_vies == 0 :  #si on a plus de vies on perd
                        messagebox.showinfo(None, "Vous avez perdu")
                        messagebox.OK = 'ok'

    def creation_liste(self, nb_cases):
        return [[random.randint(0, 1) for _ in range(nb_cases)]
                for _ in range(nb_cases)]

# Point d’entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run() 
