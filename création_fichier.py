import tkinter as tk
from tkinter import messagebox, simpledialog

import json  # Pour sauvegarder la liste dans un fichier JSON
import main as mn  # Import du fichier principal (assumé comme main.py contenant les classes FenetrePrincipale et interface)

class CreationInterface(mn.interface):
    def __init__(self, master):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross niveau création")    #titre de la fenêtre
        master.geometry("900x900")    #taille de la fenêtre
        master.resizable(True, True)     #autorise ou non le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")    #couleur du fond

        super().__init__(master)
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]  # Grille vide initiale
        self.dessiner_grille()  # Dessine la grille vide
        self.canvas.bind("<Button-1>", self.toggle_case)  # Clic gauche pour toggle (remplir/vider)
        
        # Bouton pour sauvegarder
        self.save_button = tk.Button(
            master,
            text="Sauvegarder la grille",
            font=("Arial", 14),
            command=self.sauvegarder_grille
        )
        self.save_button.place(x=720, y=300)

    def toggle_case(self, event):
        """Toggle l'état d'une case (0 -> 1 ou 1 -> 0)"""
        col = event.x // self.taille_case
        lig = (event.y - self.clue_height) // self.taille_case if hasattr(self, 'clue_height') else event.y // self.taille_case
        
        if col >= self.cases or lig >= self.cases or col < 0 or lig < 0:
            return  # Hors grille

        # Toggle dans la liste_solution (ici on édite directement la solution)
        self.liste_solution[lig][col] = 1 - self.liste_solution[lig][col]
        
        case = self.etats_cases[(col, lig)]
        if self.liste_solution[lig][col] == 1:
            self.canvas.itemconfig(case["rect"], fill="black")  # Remplir
        else:
            self.canvas.itemconfig(case["rect"], fill="white")  # Vider

    def nom_fichier(self):
        """
        Crée une boîte de dialogue (message box) pour entrer le nom du fichier.
        Retourne le nom saisi par l'utilisateur.
        """
        file_name = simpledialog.askstring(
            title="Nom du fichier",
            prompt="Entrez le nom du fichier (sans extension) :"
        )
        if file_name:  # Si l'utilisateur n'a pas annulé
            return file_name + ".json"  # Ajoute l'extension JSON par défaut
        return None  # Si annulé, retourne None
    
    def sauvegarder_grille(self):
        """Sauvegarde la liste_solution dans un fichier JSON avec nom saisi via message box"""
        fichier_nom = self.nom_fichier()  # Appel à la fonction nom_fichier()
        if fichier_nom:  # Si un nom a été saisi
            with open(fichier_nom, 'w') as f:
                json.dump(self.liste_solution, f)
            messagebox.showinfo("Sauvegarde", f"Grille sauvegardée dans {fichier_nom}!")
            self.master.destroy()  # Ferme la fenêtre après la sauvegarde réussie
        else:
            messagebox.showinfo("Annulé", "Sauvegarde annulée.")

def cree_nv():
    """Fonction principale pour créer un nouveau niveau"""
    root = tk.Tk()
    app = CreationInterface(root)
    root.mainloop()

if __name__ == "__main__":
    cree_nv()