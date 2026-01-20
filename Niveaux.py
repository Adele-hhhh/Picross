import random 
import NOMBRES as nb 
import création_fichier as cf

#crée une liste de 0 et 1 aléatoire, les 1 représenteront les cases remplies et les 0 les cases vides
def creation_liste(self):
    return [[random.randint(0, 1) for _ in range(self.cases)]
        for _ in range(self.cases)]

#permet de recommencer la partie en cours (ou perdue)
def rejouer(self): 
    
    #nouvelles vies
    self.nb_vies = 3
    self.label_vies.config(text=f"Vies : {self.nb_vies}")#actualise l'affichage du nombre de vies

    #--on enlève les cases qui ont été coloriées--

    self.cases = self.nb_cases_cote.get() #on récupère le nombre de cases par côté dans le scale
    self.taille_case = 500 // self.cases #calcule la taille d'une case

    # Nettoyage du canvas
    self.canvas.delete("all") #enlève la grille qu'il y avait avant
    self.etats_cases.clear() #toutes les cases sont remises à 0
    
    # Redessin
    self.dessiner_grille()    #remet une grille avec le nombre de cases demandé
    # Réaffichage des indices
    nb.afficher_nb_col(self)
    nb.afficher_nb_lig(self)

#Crée un nouveau niveau avec le nombre de cases demandé dans le Scale
def nouveau_niveau(self):
    self.cases = self.nb_cases_cote.get()#on récupère le nombre de cases par côté dans le scale
    self.taille_case = 500 // self.cases    #calcule la taille d'une case

    #nouvelle solution 
    self.liste_solution = creation_liste(self) #on crée une nouvelle solution

    #nouvelles vies
    self.nb_vies = 3
    self.label_vies.config(text=f"Vies : {self.nb_vies}")#actualise l'affichage du nombre de vies
        
    # Nettoyage du canvas
    self.canvas.delete("all") #enlève la grille qu'il y avait avant
    self.etats_cases.clear() #toutes les cases sont remises à 0

    cf.actualiser_indices(self) #enlève les anciens indices et met les nouveaux  
    
    # Redessin
    self.dessiner_grille()    #remet une grille avec le nombre de cases demandé



