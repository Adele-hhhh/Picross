import tkinter as tk
from tkinter import messagebox, filedialog

import json  # Pour charger la liste depuis un fichier JSON
import main as mn  # Import du fichier principal (assumé comme main.py contenant les classes FenetrePrincipale et interface)

class Utilisation_fichier():
    def __init__(self, master, liste_solution):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")    #titre de la fenêtre
        master.geometry("900x900")    #taille de la fenêtre
        master.resizable(True, True)     #autorise ou non le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")    #couleur du fond

        super().__init__(master)
        self.liste_solution = liste_solution
        self.cases = len(self.liste_solution)
        self.taille_case = 500 // self.cases
        self.canvas.delete("all")
        self.etats_cases.clear()
        self.dessiner_grille()
        self.dessiner_solution()

def utilise_fichiers():
    """Ouvre une boîte de dialogue pour sélectionner un fichier JSON et charge la grille de solution."""
    file_name = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],
        title="Sélectionner un fichier Picross"
    )
    if file_name:  # Si l'utilisateur n'a pas annulé
        try:
            with open(file_name, 'r') as f:
                liste_solution = json.load(f)
            # Ouvre une nouvelle fenêtre avec la grille chargée
            nouvelle_fenetre = tk.Tk()
            utilisation = Utilisation_fichier(nouvelle_fenetre, liste_solution)
            nouvelle_fenetre.mainloop()
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Le fichier {file_name} n'a pas été trouvé.")
        except json.JSONDecodeError:
            messagebox.showerror("Erreur", f"Le fichier {file_name} n'est pas un fichier JSON valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    utilise_fichiers()