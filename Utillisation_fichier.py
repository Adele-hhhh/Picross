'''
Module d'utilisation de fichiers de niveaux pour Picross
Permet de charger et jouer des niveaux sauvegardés au format JSON
'''
import tkinter as tk
from tkinter import messagebox, filedialog
from interface_base import Interface  # Import de la classe de base Interface
import json  # Pour charger la grille depuis un fichier JSON
import NOMBRES as nb  # Pour afficher les indices
import CLICS as cl  # Pour gérer les clics


class Utilisation_fichier(Interface):
    '''Interface pour charger et jouer un niveau depuis un fichier'''
    
    def __init__(self, master, liste_solution):
        '''
        Initialise l'interface avec une grille chargée depuis un fichier
        Paramètres :
            master : fenêtre parente
            liste_solution : grille chargée depuis le fichier JSON
        '''
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross Fichier")  # Titre de la fenêtre
        master.geometry("850x700")  # Taille de la fenêtre
        master.resizable(True, True)  # Autorise le redimensionnage
        master.configure(bg="#FFFFFF")  # Couleur du fond
        master.attributes('-topmost', True)  # Fenêtre toujours au premier plan
        # Bouton pour charger un niveau depuis un fichier
        fichiers = tk.Button(
        master,  # Fenêtre parente
        text="Fichiers niveaux",  # Titre du bouton
        font=("Arial", 14),  # Police et taille de l'écriture
        command=lambda: [master.destroy(), utilise_fichiers()])  # Fonction appelée au clic
        fichiers.place(x=620, y=440)  # Position du bouton

        # Configuration AVANT l'appel à super().__init__
        # On définit la liste_solution et les dimensions avant d'initialiser l'interface
        self.liste_solution = liste_solution
        self.cases = len(self.liste_solution)  # Taille de la grille chargée
        
        # Appel du constructeur de la classe parente Interface
        super().__init__(master)
        
        # Reconfiguration avec la bonne liste solution
        self.liste_solution = liste_solution
        self.cases = len(self.liste_solution)
        self.taille_case = 500 // self.cases  # Recalcul de la taille des cases
        
        # Réinitialisation de la grille
        self.canvas.delete("all")  # Efface tout le canvas
        self.etats_cases.clear()  # Vide le dictionnaire des états
        
        # Redessin de la grille avec les nouvelles dimensions
        self.dessiner_grille()
        
        # Affichage des indices basés sur la liste_solution chargée
        nb.afficher_nb_col(self)
        nb.afficher_nb_lig(self)
        
        # Réassociation des clics (car on a recréé le canvas)
        self.canvas.bind("<Button-1>", lambda event: cl.clic_case_gauche(event, self))
        self.canvas.bind("<Button-3>", lambda event: cl.clic_case_droit(event, self))


def utilise_fichiers():
    '''
    Ouvre une boîte de dialogue pour sélectionner un fichier JSON
    et charge la grille de solution correspondante
    '''
    # Ouverture de la boîte de dialogue de sélection de fichier
    file_name = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],
        title="Sélectionner un fichier Picross"
    )
    
    if file_name:  # Si l'utilisateur a sélectionné un fichier
        try:
            # Lecture du fichier JSON
            with open(file_name, 'r') as f:
                liste_solution = json.load(f)
            
            # Création d'une nouvelle fenêtre pour afficher le niveau
            nouvelle_fenetre = tk.Tk()  # CHANGÉ de Toplevel() à Tk()
            nouvelle_fenetre.attributes('-topmost', True)  # Fenêtre toujours au premier plan
            utilisation = Utilisation_fichier(nouvelle_fenetre, liste_solution)
            nouvelle_fenetre.mainloop()
            
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Le fichier {file_name} n'a pas été trouvé.")
        except json.JSONDecodeError:
            messagebox.showerror("Erreur", f"Le fichier {file_name} n'est pas un fichier JSON valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


# Point d'entrée si le fichier est exécuté directement
if __name__ == "__main__":
    utilise_fichiers()