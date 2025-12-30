import tkinter as tk

class FenetrePrincipale:
    # Initialisation de la fenêtre principale
    def __init__(self, master):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")
        master.geometry("900x900")
        master.resizable(False, False)
        master.configure(bg="#FFFFFF")

        # Forcer la fenêtre au premier plan
        master.attributes('-topmost', True)
        master.after(100, lambda: master.attributes('-topmost', True))

        # Création de la grille de jeu
        self.grille = Grille_de_jeux(master)

    # Lancement de la boucle principale
    def run(self):
        self.master.mainloop()


class Grille_de_jeux:
    def __init__(self, master):
        self.master = master

        # Canvas
        self.canvas = tk.Canvas(master, width=650, height=650, bg="black")
        self.canvas.place(x=125, y=180)

        # Valeur par défaut
        self.cases = 10
        self.taille_case = 650 // self.cases

        # Dessin initial
        self.dessiner_grille()

    # --- FONCTION CLÉ ---
    def set_cases(self, nb_cases):
        """
        Cette fonction sera appelée par un bouton
        pour changer le nombre de cases.
        """
        self.cases = nb_cases
        self.taille_case = 650 // self.cases

        # Nettoyage du canvas
        self.canvas.delete("all")

        # Redessin
        self.dessiner_grille()

    def dessiner_grille(self):
        for col in range(self.cases):
            for lig in range(self.cases):
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="gray"
                )
class Grille_de_jeux:
    def __init__(self, master):
        self.master = master

        # Canvas
        self.canvas = tk.Canvas(master, width=600, height=600, bg="black")
        self.canvas.place(x=250, y=250)

        # Valeur par défaut
        self.cases = 5
        self.taille_case = 600 // self.cases

        # Dessin initial
        self.dessiner_grille()

    # --- FONCTION CLÉ ---
    def set_cases(self, nb_cases):
        """
        Cette fonction sera appelée par un bouton
        pour changer le nombre de cases.
        """
        self.cases = nb_cases
        self.taille_case = 650 // self.cases

        # Nettoyage du canvas
        self.canvas.delete("all")

        # Redessin
        self.dessiner_grille()

    def dessiner_grille(self):
        for col in range(self.cases):
            for lig in range(self.cases):
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="gray"
                )

# Point d’entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run()
