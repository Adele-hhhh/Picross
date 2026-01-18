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
import NOMBRES as nb 
import création_fichier as cf  # Import du fichier de création de fichier
import Utillisation_fichier as uf

class FenetrePrincipale:    # Initialisation de la fenêtre principale
    def __init__(self, master):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")    #titre de la fenêtre
        master.geometry("800x900")    #taille de la fenêtre
        master.resizable(True, True)     #autorise ou non le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")    #couleur du fond

        # Création de la grille de jeu
        self.interface = interface(master)

    # Lancement de la boucle principale
    def run(self):
        self.master.mainloop()

class interface :
    def __init__(self, master):
        self.master = master

        self.nb_vies = 3 #nombre de vies initial

        #affichage du nombre de vies
        self.label_vies = tk.Label(
            master, 
            text =f"Vies : {self.nb_vies}", 
            bg="Violet red", 
            font=("Arial", 15))
        self.label_vies.place(x=650, y=30) #position du label 

        #titre du scale
        self.cases_cote = tk.Label (
            master, 
            text="Nombre de cases par côté", 
            bg="Light goldenrod", 
            font=("Arial",10))
        self.cases_cote.place(x=620, y=100) 

        #pour changer le nombre de cases par côté
        self.nb_cases_cote = tk.Scale(
            master, 
            orient=tk.HORIZONTAL, 
            from_=5, to=10, 
            bg="Light goldenrod")
        self.nb_cases_cote.set(10) 
        self.nb_cases_cote.place(x=650, y=120)
    
        nv_niv = tk.Button(
            master,
            text="Nouveau niveau", 
            font=("Arial", 14), 
            command=self.nouveau_niveau)
        nv_niv.place(x=620, y=200)

        creation = tk.Button(
            master,
            text="Créer un niveau", 
            font=("Arial", 14),
            command=cf.cree_nv,
            )
        creation.place(x=620, y=300)

        fichiers = tk.Button(
            master,
            text="Fichiers niveaux", 
            font=("Arial", 14),
            command=uf.utilise_fichiers
            )
        fichiers.place(x=620, y=400)

        # Grille
        self.canvas = tk.Canvas(
            master, 
            width=500, height=500, #taille de la grille
            bg="white")    #couleur de la grille
        self.canvas.place(x=100, y=70)    #écart entre le haut et le côté gauche de la fenêtre avec la grille
        
        # Valeur par défaut
        self.cases = 10    #nombre de cases par côté
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        #dict pour stocker l'état des cases
        self.etats_cases = {} 

        #solution
        self.liste_solution = self.creation_liste(self.cases)
        
        # Dessin initial
        self.dessiner_grille()
        nb.afficher_nb_col(self) 
        nb.afficher_nb_lig(self)
        self.liste_solution = self.creation_liste(self.cases)



        # Lie le clic gauche et le clic droit à leur fonction
        self.canvas.bind("<Button-1>", self.clic_case_gauche)
        self.canvas.bind("<Button-3>", self.clic_case_droit)
        
    def verifier_victoire(self):
        """Vérifie si toutes les cases correspondent à la solution"""
        for (col, lig), case in self.etats_cases.items():
            solution = self.liste_solution[lig][col]
            if case["etat"] == solution:
                continue 
            else : 
                return False
        return True

    
    def creation_liste(self, nb_cases):
            return [[random.randint(0, 1) for _ in range(nb_cases)]
                for _ in range(nb_cases)]
    def nouveau_niveau(self):
        """
        Crée un nouveau niveau avec le nombre de cases demandé dans le Scale
        """
        self.cases = self.nb_cases_cote.get()
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        #nouvelle solution 
        self.liste_solution = self.creation_liste(self.cases)

        #nouvelles vies
        self.nb_vies = 3
        self.label_vies.config(text=f"Vies : {self.nb_vies}")
        
        # Nettoyage du canvas
        self.canvas.delete("all") #enlève la grille qu'il y avait avant
        self.etats_cases.clear() #toutes les cases sont remises à 0
        
        # Redessin
        self.dessiner_grille()    #remet une grille avec le nombre de cases demandé
        nb.afficher_nb_col(self) 
        nb.afficher_nb_lig(self)

    def dessiner_grille(self):
        for col in range(self.cases):
            for lig in range(self.cases):
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="grey", fill="ghost white"
                )
                #on stocke l'ID de la case (vide au début)
                self.etats_cases[(col, lig)] = {
                    "rect": rect,
                    "etat": 0   }

    #clic gauche : remplir une case
    def clic_case_gauche(self, event): 
        #coordonnées de la case cliquée
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case
        
        case = self.etats_cases[(col, lig)] 
        if self.verifier_victoire() == False:
            if case["etat"] == 0:   #si la case est vide 
                if self.liste_solution[lig][col] == 1 and self.nb_vies > 0:#si c'est la bonne réponse et qu'on a encore des vies
                    self.canvas.itemconfig(case["rect"], fill="black") #on remplit la case
                    case["etat"] = 1 # on met à jour l'état de la case
                    if self.verifier_victoire():
                        messagebox.showinfo(None, "Vous avez gagnééé !")
                        return
                else : 
                    if self.nb_vies >= 1: #si on a encore des vies on en enlève une
                        self.nb_vies -= 1 
                        self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                        if self.nb_vies == 0:  # si on a plus de vies on perd
                            messagebox.showinfo(None, "Vous avez perdu")


    # Clic droit : mettre / enlever une croix
    def clic_case_droit(self, event):
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case

        case = self.etats_cases[(col, lig)]
        
        if self.verifier_victoire() == False:
            if case["etat"] == 0:  # Si la case est déja remplie on met rien
                if self.liste_solution[lig][col] == 0 and self.nb_vies > 0 :#si c'est la bonne réponse et qu'on a encore des vies
                    #on dessine une croix dans la case :
                    x1 = col * self.taille_case
                    y1 = lig * self.taille_case
                    x2 = x1 + self.taille_case
                    y2 = y1 + self.taille_case
                
                    # deux lignes en diagonale
                    l1 = self.canvas.create_line(x1+3, y1+3, x2-3, y2-3, fill="Violet red", width=2)
                    l2 = self.canvas.create_line(x1+3, y2-3, x2-3, y1+3, fill="Violet red", width=2)
                    case["etat"] = 0
                    if self.verifier_victoire():
                        messagebox.showinfo(None, "Vous avez gagnééé !")
                        return
                else : 
                    if self.nb_vies >= 1 : #si on a encore des vies on en enlève une
                        self.nb_vies -= 1 
                        self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                        if self.nb_vies == 0 :  #si on a plus de vies on perd
                            messagebox.showinfo(None, "Vous avez perdu")

# Point d’entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run() 
