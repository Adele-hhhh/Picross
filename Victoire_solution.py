import random 

def creation_liste(self):
    return [[random.randint(0, 1) for _ in range(self.cases)]
        for _ in range(self.cases)]

def verifier_victoire(self):
    """Vérifie si toutes les cases correspondent à la solution"""
    for (col, lig), case in self.etats_cases.items():
        solution = self.liste_solution[lig][col]
        if case["etat"] == solution:
            continue 
        else : 
            return False
    return True 