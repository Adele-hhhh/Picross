'''
Module de création de niveaux personnalisés pour Picross
Permet à l'utilisateur de créer sa propre grille et de la sauvegarder
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
from interface_base import Interface  # Import de la classe de base Interface
import json  # Pour sauvegarder la grille dans un fichier JSON
import NOMBRES as nb  # Pour afficher les indices en temps réel
import Niveaux as niv  # Pour la fonction de rejouer

class CreationInterface(Interface):
    '''Interface de création de niveau, hérite de la classe Interface de base'''
    
    def __init__(self, master):
        '''Initialise l'interface de création avec une grille vierge'''
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross niveau création")  # Titre de la fenêtre
        master.geometry("850x700")  # Taille de la fenêtre
        master.resizable(False, False)  # Désactive le redimensionnage
        master.configure(bg="#FFFFFF")  # Couleur du fond

        # Appel du constructeur de la classe parente Interface
        super().__init__(master)
        
        # Initialisation d'une grille vide (remplie de 0)
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        
        # Nettoyage du canvas pour enlever la grille par défaut
        self.canvas.delete("all")
        self.etats_cases.clear()
        
        # Liste pour stocker les labels des indices (pour pouvoir les supprimer)
        self.labels_indices = []
        
        # Variables pour gérer le maintien du clic
        self.is_dragging = False  # Indique si on est en train de glisser
        self.drag_mode = None  # Mode de remplissage (1 pour remplir, 0 pour vider)
        
        # Dessin de la grille vierge
        self.dessiner_grille()
        
        # Association des événements de clic et glissement
        self.canvas.bind("<Button-1>", self.start_drag)  # Début du clic
        self.canvas.bind("<B1-Motion>", self.continue_drag)  # Maintien du clic en mouvement
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)  # Relâchement du clic
        
        # Bouton pour sauvegarder la grille créée
        self.save_button = tk.Button(
            master,  # Fenêtre parente
            text="Sauvegarder la grille",  # Titre du bouton
            font=("Arial", 14),  # Police et taille
            command=self.sauvegarder_grille)  # Fonction de sauvegarde
        self.save_button.place(x=620, y=300)  # Position du bouton
                # Bouton pour rejouer à la partie précédente
        
        self.rejouer_btn = tk.Button(  
            master,  # Fenêtre parente
            text="Reinitialiser",  # Titre du bouton
            font=("Arial", 14),  # Police et taille de l'écriture 
            command=lambda: niv.rejouer(self))  # Fonction appelée au clic
        self.rejouer_btn.place(x=620, y=250)  # Position du bouton

    def actualiser_indices(self):
        '''Supprime et réaffiche les indices en temps réel'''
        # Suppression des anciens labels d'indices
        for label in self.labels_indices:
            label.destroy()
        self.labels_indices.clear()
        
        # Réaffichage des indices mis à jour
        nb.afficher_nb_col(self) 
        nb.afficher_nb_lig(self)

    def start_drag(self, event):
        '''
        Début du glissement : détermine le mode (remplir ou vider)
        Paramètre : event contient les coordonnées du clic
        '''
        col = event.x // self.taille_case
        lig = event.y // self.taille_case
        
        # Vérification que le clic est bien dans la grille
        if col >= self.cases or lig >= self.cases or col < 0 or lig < 0:
            return
        
        self.is_dragging = True
        # Détermine le mode : si la case était à 0, on remplit (mode 1), sinon on vide (mode 0)
        self.drag_mode = 1 - self.liste_solution[lig][col]
        
        # Applique le changement à la première case
        self.toggle_case_to(col, lig, self.drag_mode)

    def continue_drag(self, event):
        '''
        Continue le glissement : applique le mode aux cases survolées
        Paramètre : event contient les coordonnées actuelles
        '''
        if not self.is_dragging:
            return
        
        col = event.x // self.taille_case
        lig = event.y // self.taille_case
        
        # Vérification que le clic est bien dans la grille
        if col >= self.cases or lig >= self.cases or col < 0 or lig < 0:
            return
        
        # Applique le mode à la case survolée
        self.toggle_case_to(col, lig, self.drag_mode)

    def end_drag(self, event):
        '''
        Fin du glissement : réinitialise les variables
        Paramètre : event contient les coordonnées finales
        '''
        self.is_dragging = False
        self.drag_mode = None

    def toggle_case_to(self, col, lig, mode):
        '''
        Change l'état d'une case vers un mode spécifique (0 ou 1)
        Paramètres :
            col : colonne de la case
            lig : ligne de la case
            mode : 0 pour vider, 1 pour remplir
        '''
        # Si la case est déjà dans le bon mode, on ne fait rien
        if self.liste_solution[lig][col] == mode:
            return
        
        # Change l'état de la case
        self.liste_solution[lig][col] = mode
        
        # Mise à jour visuelle de la case
        case = self.etats_cases[(col, lig)]
        if mode == 1:
            self.canvas.itemconfig(case["rect"], fill="black")  # Case remplie
        else:
            self.canvas.itemconfig(case["rect"], fill="ghost white")  # Case vide
        
        # Mise à jour des indices en temps réel
        self.actualiser_indices()

    def nom_fichier(self):
        '''
        Demande à l'utilisateur de saisir un nom pour le fichier
        Retourne : le nom du fichier avec l'extension .json, ou None si annulé
        '''
        file_name = simpledialog.askstring(
            title="Nom du fichier",
            prompt="Entrez le nom du fichier (sans extension) :"
        )
        if file_name:  # Si l'utilisateur a saisi un nom
            return file_name + ".json"  # Ajout de l'extension JSON
        return None  # Retourne None si l'utilisateur a annulé
    
    def sauvegarder_grille(self):
        '''Sauvegarde la grille créée dans un fichier JSON'''
        fichier_nom = self.nom_fichier()  # Demande le nom du fichier
        
        if fichier_nom:  # Si un nom a été saisi
            # Écriture de la grille dans le fichier JSON
            with open(fichier_nom, 'w') as f:
                json.dump(self.liste_solution, f)
            
            # Message de confirmation
            messagebox.showinfo("Sauvegarde", f"Grille sauvegardée dans {fichier_nom}!")
            self.master.destroy()  # Ferme la fenêtre après la sauvegarde
        else:
            # Message si l'utilisateur a annulé
            messagebox.showinfo("Annulé", "Sauvegarde annulée.")


def cree_nv():
    '''Fonction principale pour lancer l'interface de création de niveau'''
    root = tk.Tk()
    root.attributes('-topmost', True)
    app = CreationInterface(root)
    root.mainloop()


# Point d'entrée si le fichier est exécuté directement
if __name__ == "__main__":
    cree_nv()
