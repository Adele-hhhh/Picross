''''
Picross 
Auteurs : Matis Zheng et Adèle Havard
Date : jsp
Jeu dans une grille où on doit remplir ou non des cases 
en respectant un nombre prédéfini par colonne et par ligne
Entrées : les cases cochées par l'utilisateur
Réslutat : indique si une errur est faite et annonce la victoire
''''
import tkinter as tk

class FenetrePrincipale:    # Initialisation de la fenêtre principale
    def __init__(self, master):
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross")    #titre de la fenêtre
        master.geometry("900x900")    #taille de la fenêtre
        master.resizable(True, True)     #autorise ou non le redimensionnage de la fenêtre
        master.configure(bg="#FFFFFF")    #couleur du fond

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
        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")    #taille et couleur de la grille
        self.canvas.place(x=200, y=100)    #écart entre le haut et le côté gauche de la fenêtre avec la grille

        # Valeur par défaut
        self.cases = 10    #nombre de cases par côté
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        #dict pour stocker l'état des cases
        self.etats_cases = {} 

        # Dessin initial
        self.dessiner_grille()

        # Lie le clic gauche et le clic droit à leur fonction
        self.canvas.bind("<Button-1>", self.clic_case_gauche)
        self.canvas.bind("<Button-3>", self.clic_case_droit)
        
    # --- FONCTION CLÉ ---
    def set_cases(self, nb_cases):
        """
        Cette fonction sera appelée par un bouton
        pour changer le nombre de cases.
        """
        self.cases = nb_cases    #nombre de cases par côté
        self.taille_case = 500 // self.cases    #calcule la taille d'une case

        # Nettoyage du canvas
        self.canvas.delete("all") #enlève la grille qu'il y avait avant

        # Redessin
        self.dessiner_grille()    #remet une grille avec le nombre de cases demandé

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
                #on stocke l'ID de la case (vide et sans croix)
                self.etats_cases[(col, lig)] = {
                    "rect": rect,
                    "croix": None, 
                    "etat": "vide"
                }

    #Inverse la couleur de la case cliquée
    def clic_case_gauche(self, event): 
        #coordonnées de la case cliquée
        col = event.x // self.taille_case 
        lig = event.y // self.taille_case

        if 0 <= col < self.cases and 0 <= lig < self.cases: #vérifie qu'on clique pas en dehors de la grille
            case = self.etats_cases[(col, lig)]
            rect = case["rect"]
            couleur_actuelle = self.canvas.itemcget(rect, "fill")
            nouvelle_couleur = "black" if couleur_actuelle == "white" else "white"
            self.canvas.itemconfig(rect, fill=nouvelle_couleur)

            # on met à jour l'état de la case
            case["etat"] = "remplie" if nouvelle_couleur == "black" else "vide"

            #si on remplit, on enlève une éventuelle croix
            if case["croix"] is not None:
                for ligne_id in case["croix"]:
                    self.canvas.delete(ligne_id)
                case["croix"] = None

    # Clic droit : mettre / enlever une croix
    def clic_case_droit(self, event):
        col = event.x // self.taille_case
        lig = event.y // self.taille_case

        if 0 <= col < self.cases and 0 <= lig < self.cases:
            case = self.etats_cases[(col, lig)]

            # Si une croix existe déjà, on l’enlève
            if case["croix"] is not None or case["etat"] is "remplie":
                for ligne_id in case["croix"]:
                    self.canvas.delete(ligne_id)
                return

            # Sinon, on dessine une croix dans la case
            x1 = col * self.taille_case
            y1 = lig * self.taille_case
            x2 = x1 + self.taille_case
            y2 = y1 + self.taille_case

            # deux lignes en diagonale
            l1 = self.canvas.create_line(x1+3, y1+3, x2-3, y2-3, fill="red", width=2)
            l2 = self.canvas.create_line(x1+3, y2-3, x2-3, y1+3, fill="red", width=2)

            case["croix"] = [l1, l2]
            case["etat"] = "croix"



# Point d’entrée du programme
if __name__ == "__main__":
    app = FenetrePrincipale(tk.Tk())
    app.run()
