'''
Picross 
Auteurs : Matis Zhang et Adèle Havard
Date : jsp
Jeu dans une grille où on doit remplir ou non des cases 
en respectant un nombre prédéfini par colonne et par ligne
Entrées : les cases cochées par l'utilisateur
Résultat : indique si une erreur est faite et annonce la victoire 
'''
import tkinter as tk  # Import de tkinter
from interface_base import Interface  # Import de la classe Interface
# Import des fonctions des fichiers annexes
import création_fichier as cf
import Utillisation_fichier as uf 


class FenetrePrincipale:
    '''Classe principale gérant la fenêtre du jeu'''
    
    def __init__(self, master):
        '''Initialise la fenêtre principale et l'interface de jeu'''
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")  # Titre de la fenêtre
        master.geometry("900x800")  # Taille de la fenêtre
        master.resizable(True, True)  # Autorise le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")  # Couleur du fond

        # Création de l'interface de jeu
        self.Interface = Interface(master)
        
        # Bouton pour créer un nouveau niveau personnalisé
        # (Placé ici pour éviter l'importation circulaire)
        creation = tk.Button(
            master,  # Fenêtre parente
            text="Créer un niveau",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture
            command=cf.cree_nv)  # Fonction appelée au clic
        creation.place(x=620, y=380)  # Position du bouton

        # Bouton pour charger un niveau depuis un fichier
        # (Placé ici pour éviter l'importation circulaire)
        fichiers = tk.Button(
            master,  # Fenêtre parente
            text="Fichiers niveaux",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture
            command=uf.utilise_fichiers)  # Fonction appelée au clic
        fichiers.place(x=620, y=460)  # Position du bouton

    def run(self):
        '''Lance la boucle principale de l'interface graphique'''
        self.master.mainloop()


# Point d'entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run()