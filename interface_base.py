'''
Classe de base Interface pour le jeu Picross
Contient la grille de jeu, les contrôles et l'affichage des indices
'''
import tkinter as tk
from tkinter import messagebox
import NOMBRES as nb 
import CLICS as cl 
import Niveaux as niv
class Interface:
    def __init__(self, master):
        '''Initialise l'interface de jeu avec tous ses éléments'''
        self.master = master

        self.nb_vies = 3  # Nombre de vies initial

        # Affichage du nombre de vies
        self.label_vies = tk.Label(
            master,  # Fenêtre parente
            text=f"Vies : {self.nb_vies}",  # Texte du label (avec nombre de vies)
            bg="Violet red",  # Couleur du label
            font=("Arial", 15))  # Police et taille de l'écriture
        self.label_vies.place(x=650, y=30)  # Position du label 

        # Scale pour changer le nombre de cases par côté
        self.nb_cases_cote = tk.Scale(
            master,  # Fenêtre parente
            orient=tk.HORIZONTAL,  # Orientation du scale 
            from_=5, to=10,  # Valeurs minimale et maximale
            bg="Light goldenrod")  # Couleur du scale
        self.nb_cases_cote.set(10)  # Valeur initiale 
        self.nb_cases_cote.place(x=650, y=120)  # Position du scale
        
        # Titre du scale
        self.cases_cote = tk.Label(
            master,  # Fenêtre parente
            text="Nombre de cases par côté",  # Texte du label
            bg="Light goldenrod",  # Couleur du label
            font=("Arial", 10))  # Police et taille de l'écriture 
        self.cases_cote.place(x=620, y=100)  # Position du label
    
        # Bouton pour créer un nouveau niveau
        self.nv_niv = tk.Button(  
            master,  # Fenêtre parente
            text="Nouveau niveau",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture 
            command=lambda: niv.nouveau_niveau(self))  # Fonction appelée au clic
        self.nv_niv.place(x=620, y=200)  # Position du bouton  

        # Bouton pour rejouer à la partie précédente
        self.rejouer_btn = tk.Button(  
            master,  # Fenêtre parente
            text="Rejouer",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture 
            command=lambda: niv.rejouer(self))  # Fonction appelée au clic
        self.rejouer_btn.place(x=620, y=250)  # Position du bouton  

        # Note : les boutons "Créer un niveau" et "Fichiers niveaux" 
        # sont ajoutés dans main.py pour éviter l'importation circulaire

        # Création du canvas pour la grille de jeu
        self.canvas = tk.Canvas(
            master,  # Fenêtre parente
            width=500, height=500,  # Dimensions de la grille
            bg="white")  # Couleur de fond
        self.canvas.place(x=100, y=100)  # Position de la grille
        
        # Valeurs par défaut
        self.cases = 10  # Nombre de cases par côté (valeur initiale)
        self.taille_case = 500 // self.cases  # Calcul de la taille d'une case

        # Dictionnaire pour stocker l'état de chaque case
        self.etats_cases = {} 

        # Liste pour stocker les labels d'indices (ajouté pour fixer le bug)
        self.labels_indices = []

        # Génération de la solution de la partie
        self.liste_solution = niv.creation_liste(self)
        
        # Dessin initial de la grille et des indices
        self.dessiner_grille() 
        nb.afficher_nb_col(self)  # Affiche les indices des colonnes
        nb.afficher_nb_lig(self)  # Affiche les indices des lignes

        # Association des clics aux fonctions correspondantes
        self.canvas.bind("<Button-1>", lambda event: cl.clic_case_gauche(event, self))  # Clic gauche
        self.canvas.bind("<Button-3>", lambda event: cl.clic_case_droit(event, self))  # Clic droit

    def dessiner_grille(self):
        '''Dessine la grille de jeu avec toutes les cases'''
        for col in range(self.cases):
            for lig in range(self.cases):
                # Calcul des coordonnées de chaque case
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                # Création du rectangle représentant la case
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="grey",  # Couleur de la bordure
                    fill="ghost white"  # Couleur de remplissage
                )
                
                # Stockage de l'ID et de l'état de la case (0 = vide au début)
                self.etats_cases[(col, lig)] = {
                    "rect": rect,
                    "etat": 0}