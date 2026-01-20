'''
Module de création de niveaux personnalisés pour Picross
Permet à l'utilisateur de créer sa propre grille et de la sauvegarder
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
from interface_base import Interface
import json
import creation_helper as ch
import creation_event as ce


class CreationInterface:
    '''Interface de création de niveau avec affichage des indices en temps réel'''
    
    def __init__(self, master):
        '''Initialise l'interface de création avec une grille vierge'''
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross niveau création")
        master.geometry("850x700")
        master.resizable(False, False)
        master.configure(bg="#FFFFFF")
        master.attributes('-topmost', True)

        # Initialisation des variables
        self.cases = 10
        self.taille_case = 500 // self.cases
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        self.etats_cases = {}
        self.is_dragging = False
        self.drag_mode = None
        self.labels_indices = []
        
        # Scale pour changer le nombre de cases par côté
        self.nb_cases_cote = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_=5, to=10,
            bg="Light goldenrod",
            command=self.changer_taille_grille)
        self.nb_cases_cote.set(10)
        self.nb_cases_cote.place(x=650, y=120)
        
        # Titre du scale
        self.cases_cote_label = tk.Label(
            master,
            text="Nombre de cases par côté",
            bg="Light goldenrod",
            font=("Arial", 10))
        self.cases_cote_label.place(x=620, y=100)
        
        # Création du canvas
        self.canvas = tk.Canvas(
            master,
            width=500, height=500,
            bg="white")
        self.canvas.place(x=100, y=100)
        
        # Utilise la fonction dessiner_grille de Interface
        Interface.dessiner_grille(self)
        
        # Affichage initial des indices (vides car grille vierge)
        ch.actualiser_indices(self)
        
        # Association des événements
        self.canvas.bind("<Button-1>", lambda e: ce.start_drag(self, e))
        self.canvas.bind("<B1-Motion>", lambda e: ce.continue_drag(self, e))
        self.canvas.bind("<ButtonRelease-1>", lambda e: ce.end_drag(self, e))
        
        # Bouton Reset
        self.reset_button = tk.Button(
            master,
            text="Reset",
            font=("Arial", 14),
            command=self.reset_grille)
        self.reset_button.place(x=620, y=320)
        
        # Bouton Sauvegarder
        self.save_button = tk.Button(
            master,
            text="Sauvegarder la grille",
            font=("Arial", 14),
            command=self.sauvegarder_grille)
        self.save_button.place(x=620, y=380)

    def changer_taille_grille(self, value):
        '''Change la taille de la grille selon la valeur du scale'''
        self.cases = int(value)
        self.taille_case = 500 // self.cases
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        
        self.canvas.delete("all")
        self.etats_cases.clear()
        
        Interface.dessiner_grille(self)
        ch.actualiser_indices(self)
        
        self.is_dragging = False
        self.drag_mode = None

    def reset_grille(self):
        '''Réinitialise complètement la grille et les indices'''
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        self.canvas.delete("all")
        self.etats_cases.clear()
        
        Interface.dessiner_grille(self)
        ch.actualiser_indices(self)
        
        self.is_dragging = False
        self.drag_mode = None

    def nom_fichier(self):
        '''Demande à l'utilisateur de saisir un nom pour le fichier'''
        file_name = simpledialog.askstring(
            title="Nom du fichier",
            prompt="Entrez le nom du fichier (sans extension) :"
        )
        if file_name:
            return file_name + ".json"
        return None
    
    def sauvegarder_grille(self):
        '''Sauvegarde la grille créée dans un fichier JSON'''
        fichier_nom = self.nom_fichier()
        
        if fichier_nom:
            with open(fichier_nom, 'w') as f:
                json.dump(self.liste_solution, f)
            
            messagebox.showinfo("Sauvegarde", f"Grille sauvegardée dans {fichier_nom}!")
            self.master.destroy()
        else:
            messagebox.showinfo("Annulé", "Sauvegarde annulée.")


def cree_nv():
    '''Fonction principale pour lancer l'interface de création de niveau'''
    root = tk.Tk()
    root.attributes('-topmost', True)
    app = CreationInterface(root)
    root.mainloop()


if __name__ == "__main__":
    cree_nv()