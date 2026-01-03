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
        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.place(x=200, y=100)

        # Valeur par défaut
        self.cases = 10
        self.taille_case = 500 // self.cases

        #dict pour stocker l'état des cases
        self.etats_cases = {} 

        # Dessin initial
        self.dessiner_grille()

        # Lie le clic gauche à la fonction
        self.canvas.bind("<Button-1>", self.clic_case)

    # --- FONCTION CLÉ ---
    def set_cases(self, nb_cases):
        """
        Cette fonction sera appelée par un bouton
        pour changer le nombre de cases.
        """
        self.cases = nb_cases
        self.taille_case = 500 // self.cases

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

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="grey", fill="white"
                )
                self.etats_cases[(col, lig)] = rect 

    #Inverse la couleur de la case cliquée
    def clic_case(self, event): 
        #coordonnées de la case cliquée
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case

        if 0 <= col < self.cases and 0 <= lig < self.cases: #vérifie qu'on clique pas en dehors de la grille
            rect = self.etats_cases[(col, lig)]
            couleur_actuelle = self.canvas.itemcget(rect, "fill")
            nouvelle_couleur = "black" if couleur_actuelle == "white" else "white"
            self.canvas.itemconfig(rect, fill=nouvelle_couleur)




# Point d’entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run()
