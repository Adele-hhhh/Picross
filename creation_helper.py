'''
Fonctions auxiliaires pour la création de niveaux Picross
Ces fonctions servent à afficher et mettre à jour les indices
(lignes et colonnes) lors de la création d’un niveau.
'''

import tkinter as tk
import NOMBRES as nb


def actualiser_indices(self):
    '''
    Supprime puis réaffiche les indices des lignes et colonnes
    en fonction de la grille actuelle.
    '''
    # Suppression de tous les anciens labels d’indices
    for label in self.labels_indices:
        label.destroy()
    
    # Vide la liste qui stocke les labels d’indices
    self.labels_indices.clear()
    
    # Réaffiche les indices mis à jour
    afficher_nb_col_creation(self)
    afficher_nb_lig_creation(self)


def afficher_nb_col_creation(self):
    '''
    Affiche les indices des colonnes au-dessus de la grille lors de la création d’un niveau, 
    même fonction que dans le fichier nombres mais remise pour simplifier
    '''
    # Calcul des indices de colonnes à partir de la solution
    nb_col = nb.nombre_colonne(self.liste_solution)
    
    # Création d’un fond coloré pour les indices des colonnes
    fond = tk.Label(
        self.master,
        bg="Light goldenrod",
        height=5,
        width=71
    )
    fond.place(x=100, y=20)
    
    # Stocke le fond pour pouvoir le supprimer plus tard
    self.labels_indices.append(fond)
    
    # Parcourt chaque colonne
    for i in range(len(nb_col)):
        # Transforme la liste d’indices en texte vertical
        texte = "\n".join(str(nombre) for nombre in nb_col[i]) if nb_col[i] else ""
        
        # Création du label pour les indices de la colonne
        label = tk.Label(
            self.master,
            text=texte,
            bg="Light goldenrod",
            font=("Arial", 9)
        )
        
        # Calcul de la position horizontale du label
        x = 100 + i * self.taille_case + self.taille_case // 2
        
        # Placement du label au-dessus de la colonne
        label.place(x=x, y=60, anchor="center")
        
        # Stocke le label pour une future suppression
        self.labels_indices.append(label)


def afficher_nb_lig_creation(self):
    '''
    Affiche les indices des lignes à gauche de la grille lors de la création d’un niveau, 
    même fonction que dans le fichier nombres mais remise pour simplifier
    '''
    # Calcul des indices de lignes à partir de la solution
    nb_lig = nb.nombre_ligne(self.liste_solution)
    
    # Création d’un fond coloré pour les indices des lignes
    fond = tk.Label(
        self.master,
        bg="Light goldenrod",
        height=33,
        width=7
    )
    fond.place(x=46, y=100)
    
    # Stocke le fond pour pouvoir le supprimer plus tard
    self.labels_indices.append(fond)
    
    # Parcourt chaque ligne
    for i in range(len(nb_lig)):
        # Transforme la liste d’indices en texte horizontal
        texte = " ".join(str(nombre) for nombre in nb_lig[i]) if nb_lig[i] else ""
        
        # Création du label pour les indices de la ligne
        label = tk.Label(
            self.master,
            text=texte,
            bg="Light goldenrod",
            font=("Arial", 9)
        )
        
        # Calcul de la position verticale du label
        y = 100 + i * self.taille_case + self.taille_case // 2
        
        # Placement du label à gauche de la ligne
        label.place(x=73, y=y, anchor="center")
        
        # Stocke le label pour une future suppression
        self.labels_indices.append(label)
