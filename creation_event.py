'''
Fonctions pour les événements de souris dans la création de niveau Picross.
Gère le drag pour remplir ou vider les cases.
'''
import creation_helper as ch  # Pour actualiser_indices


def toggle_case(self, col, lig, new_etat):
    '''Change l'état d'une case et met à jour l'affichage'''
    if 0 <= col < self.cases and 0 <= lig < self.cases:
        key = (col, lig)
        if key in self.etats_cases:
            case = self.etats_cases[key]
            self.liste_solution[lig][col] = new_etat
            color = "black" if new_etat == 1 else "ghost white"
            self.canvas.itemconfig(case["rect"], fill=color)
            case["etat"] = new_etat


def start_drag(self, event):
    '''Démarre le drag : détermine le mode (remplir ou vider)'''
    col = event.x // self.taille_case
    lig = event.y // self.taille_case
    if 0 <= col < self.cases and 0 <= lig < self.cases:
        current = self.liste_solution[lig][col]
        self.drag_mode = 1 if current == 0 else 0
        toggle_case(self, col, lig, self.drag_mode)
        self.is_dragging = True


def continue_drag(self, event):
    '''Continue le drag : applique le mode sur les cases survolées'''
    if self.is_dragging:
        col = event.x // self.taille_case
        lig = event.y // self.taille_case
        if 0 <= col < self.cases and 0 <= lig < self.cases:
            current = self.liste_solution[lig][col]
            if current != self.drag_mode:
                toggle_case(self, col, lig, self.drag_mode)


def end_drag(self, event):
    '''Termine le drag et met à jour les indices'''
    self.is_dragging = False
    ch.actualiser_indices(self)