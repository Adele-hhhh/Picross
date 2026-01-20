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

class CreationInterface:
    '''Interface de création de niveau avec affichage des indices en temps réel'''
    
    def __init__(self, master):
        '''Initialise l'interface de création avec une grille vierge'''
        self.master = master

        # Paramètres de la fenêtre
        master.title("Picross niveau création")  # Titre de la fenêtre
        master.geometry("850x700")  # Taille de la fenêtre
        master.resizable(False, False)  # Désactive le redimensionnage
        master.configure(bg="#FFFFFF")  # Couleur du fond
        master.attributes('-topmost', True)  # Fenêtre toujours au premier plan

        # Initialisation des variables AVANT tout
        self.cases = 10  # Nombre de cases par côté (10x10 par défaut)
        self.taille_case = 500 // self.cases  # Calcul de la taille d'une case
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]  # Grille vierge (tous à 0)
        self.etats_cases = {}  # Dictionnaire pour stocker l'état de chaque case
        self.is_dragging = False  # Indique si on est en train de glisser la souris
        self.drag_mode = None  # Mode de remplissage (1 pour remplir, 0 pour vider)
        self.labels_indices = []  # Liste pour stocker les labels des indices (pour pouvoir les supprimer)
        
        # Scale pour changer le nombre de cases par côté
        self.nb_cases_cote = tk.Scale(
            master,  # Fenêtre parente
            orient=tk.HORIZONTAL,  # Orientation du scale
            from_=5, to=10,  # Valeurs minimale et maximale
            bg="Light goldenrod",  # Couleur du scale
            command=self.changer_taille_grille)  # Fonction appelée quand on change la valeur
        self.nb_cases_cote.set(10)  # Valeur initiale (10x10)
        self.nb_cases_cote.place(x=650, y=120)  # Position du scale
        
        # Titre du scale
        self.cases_cote_label = tk.Label(
            master,  # Fenêtre parente
            text="Nombre de cases par côté",  # Texte du label
            bg="Light goldenrod",  # Couleur du label
            font=("Arial", 10))  # Police et taille de l'écriture
        self.cases_cote_label.place(x=620, y=100)  # Position du label
        
        # Création manuelle du canvas pour la grille
        self.canvas = tk.Canvas(
            master,  # Fenêtre parente
            width=500, height=500,  # Dimensions de la grille
            bg="white")  # Couleur de fond
        self.canvas.place(x=100, y=100)  # Position de la grille
        
        # Utilise la fonction dessiner_grille de Interface (réutilisation du code)
        Interface.dessiner_grille(self)
        
        # Affichage initial des indices (vides car grille vierge)
        self.actualiser_indices()
        
        # Association des événements de clic et glissement
        self.canvas.bind("<Button-1>", self.start_drag)  # Début du clic gauche
        self.canvas.bind("<B1-Motion>", self.continue_drag)  # Maintien du clic en mouvement
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)  # Relâchement du clic
        
        # Bouton Reset pour réinitialiser la grille
        self.reset_button = tk.Button(
            master,  # Fenêtre parente
            text="Reset",  # Titre du bouton
            font=("Arial", 14),  # Police et taille
            command=self.reset_grille)  # Fonction appelée au clic
        self.reset_button.place(x=620, y=320)  # Position du bouton
        
        # Bouton Sauvegarder pour enregistrer la grille dans un fichier JSON
        self.save_button = tk.Button(
            master,  # Fenêtre parente
            text="Sauvegarder la grille",  # Titre du bouton
            font=("Arial", 14),  # Police et taille
            command=self.sauvegarder_grille)  # Fonction appelée au clic
        self.save_button.place(x=620, y=380)  # Position du bouton

    def changer_taille_grille(self, value):
        '''
        Change la taille de la grille selon la valeur du scale
        Paramètre : value - nouvelle valeur du scale (nombre de cases par côté)
        '''
        # Récupération de la nouvelle taille
        self.cases = int(value)
        self.taille_case = 500 // self.cases  # Recalcul de la taille d'une case
        
        # Réinitialisation de la liste_solution avec la nouvelle taille
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        
        # Nettoyage du canvas
        self.canvas.delete("all")  # Efface tout le canvas
        self.etats_cases.clear()  # Vide le dictionnaire des états
        
        # Redessin de la grille avec la nouvelle taille
        Interface.dessiner_grille(self)
        
        # Mise à jour des indices
        self.actualiser_indices()
        
        # Réinitialisation des variables de glissement
        self.is_dragging = False
        self.drag_mode = None

    def actualiser_indices(self):
        '''Supprime et réaffiche les indices en temps réel'''
        # Suppression des anciens labels d'indices
        for label in self.labels_indices:
            label.destroy()  # Détruit chaque label
        self.labels_indices.clear()  # Vide la liste
        
        # Réaffichage des indices mis à jour
        self.afficher_nb_col_creation()  # Indices des colonnes
        self.afficher_nb_lig_creation()  # Indices des lignes

    def afficher_nb_col_creation(self):
        '''Affiche les indices des colonnes au-dessus de la grille'''
        # Calcul des indices pour chaque colonne
        nb_col = nb.nombre_colonne(self.liste_solution)
        
        # Fond coloré pour les indices des colonnes
        fond = tk.Label(
            self.master,  # Fenêtre parente
            bg="Light goldenrod",  # Couleur de fond
            height=5, width=71)  # Dimensions
        fond.place(x=100, y=20)  # Position
        self.labels_indices.append(fond)  # Ajout à la liste pour pouvoir le supprimer plus tard
        
        # Pour chaque colonne, affiche les nombres verticalement
        for i in range(len(nb_col)): 
            # Si la liste est vide (pas de cases remplies), affiche rien
            texte = "\n".join(str(nombre) for nombre in nb_col[i]) if nb_col[i] else ""
            
            # Affichage du label avec les nombres
            label = tk.Label(
                self.master,  # Fenêtre parente
                text=texte,  # Texte à afficher (nombres séparés par des retours à la ligne)
                bg="Light goldenrod",  # Couleur de fond
                font=("Arial", 9))  # Police et taille
            x = 100 + i * self.taille_case + self.taille_case // 2  # Position x (centrée sur la colonne)
            label.place(x=x, y=60, anchor="center")  # Position du label
            self.labels_indices.append(label)  # Ajout à la liste

    def afficher_nb_lig_creation(self):
        '''Affiche les indices des lignes à gauche de la grille'''
        # Calcul des indices pour chaque ligne
        nb_lig = nb.nombre_ligne(self.liste_solution)
        
        # Fond coloré pour les indices des lignes
        fond = tk.Label(
            self.master,  # Fenêtre parente
            bg="Light goldenrod",  # Couleur de fond
            height=33, width=7)  # Dimensions
        fond.place(x=46, y=100)  # Position
        self.labels_indices.append(fond)  # Ajout à la liste pour pouvoir le supprimer plus tard
        
        # Pour chaque ligne, affiche les nombres horizontalement
        for i in range(len(nb_lig)): 
            # Si la liste est vide (pas de cases remplies), affiche rien
            texte = " ".join(str(nombre) for nombre in nb_lig[i]) if nb_lig[i] else ""
            
            # Affichage du label avec les nombres
            label = tk.Label(
                self.master,  # Fenêtre parente
                text=texte,  # Texte à afficher (nombres séparés par des espaces)
                bg="Light goldenrod",  # Couleur de fond
                font=("Arial", 9))  # Police et taille
            y = 100 + i * self.taille_case + self.taille_case // 2  # Position y (centrée sur la ligne)
            label.place(x=73, y=y, anchor="center")  # Position du label
            self.labels_indices.append(label)  # Ajout à la liste

    def start_drag(self, event):
        '''
        Début du glissement : détermine le mode (remplir ou vider)
        Paramètre : event - événement contenant les coordonnées du clic
        '''
        # Calcul de la colonne et ligne cliquées
        col = event.x // self.taille_case
        lig = event.y // self.taille_case
        
        # Vérification que le clic est bien dans la grille
        if col >= self.cases or lig >= self.cases or col < 0 or lig < 0:
            return  # Sort de la fonction si hors grille
        
        self.is_dragging = True  # Active le mode glissement
        # Détermine le mode : si la case était à 0, on remplit (mode 1), sinon on vide (mode 0)
        self.drag_mode = 1 - self.liste_solution[lig][col]
        
        # Applique le changement à la première case
        self.toggle_case_to(col, lig, self.drag_mode)

    def continue_drag(self, event):
        '''
        Continue le glissement : applique le mode aux cases survolées
        Paramètre : event - événement contenant les coordonnées actuelles
        '''
        if not self.is_dragging:  # Si on n'est pas en mode glissement
            return  # Sort de la fonction
        
        # Calcul de la colonne et ligne survolées
        col = event.x // self.taille_case
        lig = event.y // self.taille_case
        
        # Vérification que la position est bien dans la grille
        if col >= self.cases or lig >= self.cases or col < 0 or lig < 0:
            return  # Sort de la fonction si hors grille
        
        # Applique le mode à la case survolée
        self.toggle_case_to(col, lig, self.drag_mode)

    def end_drag(self, event):
        '''
        Fin du glissement : réinitialise les variables
        Paramètre : event - événement contenant les coordonnées finales
        '''
        self.is_dragging = False  # Désactive le mode glissement
        self.drag_mode = None  # Réinitialise le mode

    def toggle_case_to(self, col, lig, mode):
        '''
        Change l'état d'une case vers un mode spécifique (0 ou 1)
        Paramètres :
            col - colonne de la case
            lig - ligne de la case
            mode - 0 pour vider, 1 pour remplir
        '''
        # Si la case est déjà dans le bon mode, on ne fait rien
        if self.liste_solution[lig][col] == mode:
            return  # Sort de la fonction
        
        # Change l'état de la case dans la liste_solution
        self.liste_solution[lig][col] = mode
        
        # Mise à jour visuelle de la case
        case = self.etats_cases[(col, lig)]
        if mode == 1:
            self.canvas.itemconfig(case["rect"], fill="black")  # Case remplie en noir
        else:
            self.canvas.itemconfig(case["rect"], fill="ghost white")  # Case vide en blanc
        
        # Mise à jour des indices en temps réel
        self.actualiser_indices()

    def reset_grille(self):
        '''Réinitialise complètement la grille et les indices'''
        # Réinitialisation de la liste_solution (tout à 0)
        self.liste_solution = [[0 for _ in range(self.cases)] for _ in range(self.cases)]
        
        # Nettoyage du canvas
        self.canvas.delete("all")  # Efface tout le canvas
        
        # Réinitialisation du dictionnaire des états
        self.etats_cases.clear()  # Vide le dictionnaire
        
        # Réutilise la fonction dessiner_grille de Interface
        Interface.dessiner_grille(self)
        
        # Mise à jour des indices (qui seront vides)
        self.actualiser_indices()
        
        # Réinitialisation des variables de glissement
        self.is_dragging = False
        self.drag_mode = None

    def nom_fichier(self):
        '''
        Demande à l'utilisateur de saisir un nom pour le fichier
        Retourne : le nom du fichier avec l'extension .json, ou None si annulé
        '''
        file_name = simpledialog.askstring(
            title="Nom du fichier",  # Titre de la boîte de dialogue
            prompt="Entrez le nom du fichier (sans extension) :"  # Message affiché
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
                json.dump(self.liste_solution, f)  # Sauvegarde de la liste_solution
            
            # Message de confirmation
            messagebox.showinfo("Sauvegarde", f"Grille sauvegardée dans {fichier_nom}!")
            self.master.destroy()  # Ferme la fenêtre après la sauvegarde
        else:
            # Message si l'utilisateur a annulé
            messagebox.showinfo("Annulé", "Sauvegarde annulée.")


def cree_nv():
    '''Fonction principale pour lancer l'interface de création de niveau'''
    root = tk.Tk()  # Création de la fenêtre principale
    root.attributes('-topmost', True)  # Fenêtre toujours au premier plan
    app = CreationInterface(root)  # Création de l'interface de création
    root.mainloop()  # Lance la boucle principale


# Point d'entrée si le fichier est exécuté directement
if __name__ == "__main__":
    cree_nv()
