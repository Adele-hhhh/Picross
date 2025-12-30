import tkinter as tk

class FenetrePrincipale:
    def __init__(self, master):
        self.master = master
        master.title("Picross")
        master.geometry("900x900")
        master.resizable(False, False)
        master.configure(bg="#FFFFFF")

if __name__ == "__main__":
    fenetre = FenetrePrincipale(tk.Tk())
    fenetre.master.mainloop()