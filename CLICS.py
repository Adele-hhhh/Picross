from tkinter import messagebox 

def verifier_victoire(self):
    """Vérifie si toutes les cases correspondent à la solution"""
    for (col, lig), case in self.etats_cases.items():
        solution = self.liste_solution[lig][col]
        if case["etat"] == solution:
            continue 
        else : 
            return False
    return True 

#clic gauche : remplir une case
def clic_case_gauche(event, self): 
    #coordonnées de la case cliquée
    col = event.x // self.taille_case 
    lig = event.y // self.taille_case

    case = self.etats_cases[(col, lig)] 
    if verifier_victoire(self) == False:
        if case["etat"] == 0:   #si la case est vide 
            if self.liste_solution[lig][col] == 1 and self.nb_vies > 0:#si c'est la bonne réponse et qu'on a encore des vies
                self.canvas.itemconfig(case["rect"], fill="black") #on remplit la case
                case["etat"] = 1 # on met à jour l'état de la case
                if verifier_victoire(self):
                    messagebox.showinfo(None, "Vous avez gagnééé !")
                    return
            else : 
                if self.nb_vies >= 1: #si on a encore des vies on en enlève une
                    self.nb_vies -= 1 
                    self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                    if self.nb_vies == 0:  # si on a plus de vies on perd
                        messagebox.showinfo(None, "Vous avez perdu")


def clic_case_droit(event, self):
    col = event.x // self.taille_case 
    lig = event.y // self.taille_case

    case = self.etats_cases[(col, lig)]
    if verifier_victoire(self) == False:
        if case["etat"] == 0:  # Si la case est déja remplie on met rien
            if self.liste_solution[lig][col] == 0 and self.nb_vies > 0 :#si c'est la bonne réponse et qu'on a encore des vies
                #on dessine une croix dans la case :
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
            
                # deux lignes en diagonale
                l1 = self.canvas.create_line(x1+3, y1+3, x2-3, y2-3, fill="Violet red", width=2)
                l2 = self.canvas.create_line(x1+3, y2-3, x2-3, y1+3, fill="Violet red", width=2)
                case["etat"] = 0
                if verifier_victoire(self):
                    messagebox.showinfo(None, "Vous avez gagnééé !")
                    return
            else : 
                if self.nb_vies >= 1 : #si on a encore des vies on en enlève une
                    self.nb_vies -= 1 
                    self.label_vies.config(text=f"Vies : {self.nb_vies}") #on change le nombre affiché
                    if self.nb_vies == 0 :  #si on a plus de vies on perd
                        messagebox.showinfo(None, "Vous avez perdu")
