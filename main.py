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
        master.geometry("850x700")  # Taille de la fenêtre
        master.resizable(False, False)  # Autorise le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")  # Couleur du fond
        master.attributes('-topmost', True)  # Met la fenêtre au premier plan

        # Création de l'interface de jeu
        self.Interface = Interface(master)
        
        # (Placé ici pour éviter l'importation circulaire)
        creation = tk.Button(
            master,
            text="Créer un niveau",
            font=("Arial", 14),
            command=lambda: [master.destroy(), cf.cree_nv()])  # Ferme la fenêtre avant d'ouvrir la nouvelle
        creation.place(x=620, y=400)

        # Bouton pour charger un niveau depuis un fichier
        # (Placé ici pour éviter l'importation circulaire)
        fichiers = tk.Button(
            master,  # Fenêtre parente
            text="Fichiers niveaux",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture
            command=lambda: [master.destroy(), uf.utilise_fichiers()])  # Fonction appelée au clic
        fichiers.place(x=620, y=460)  # Position du bouton
        

    def run(self):
        '''Lance la boucle principale de l'interface graphique'''
        self.master.mainloop()


# Point d'entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run()