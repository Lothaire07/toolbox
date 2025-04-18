import tkinter as tk
from tkinter import messagebox
import time
import threading
import subprocess

# Variable de contrôle pour arrêter la recherche
stop_recherche = False
thread_en_cours = None

def ouvrir_en_arriere_plan(url):
    script = f'''
tell application "Safari"
        open location "{url}"
end tell
        '''
    subprocess.run(["osascript", "-e", script])

def lancer_recherches():
    global stop_recherche, thread_en_cours
    stop_recherche = False

    mots_liste = entree_liste.get("1.0", tk.END).strip().splitlines()
    chaine_fixe = entree_fixe.get().strip()

    if not mots_liste or not chaine_fixe:
        messagebox.showwarning("Champs manquants", "Veuillez remplir les deux champs.")
        return

    bouton_rechercher.config(state="disabled")
    bouton_arreter.config(state="normal")

    thread_en_cours = threading.Thread(target=effectuer_recherches, args=(mots_liste, chaine_fixe))
    thread_en_cours.start()

def effectuer_recherches(mots_liste, chaine_fixe):
    global stop_recherche
    delai = 0.1  # en secondes

    for mot in mots_liste:
        if stop_recherche:
            break
        requete = f"{mot} {chaine_fixe}"
        url = f"https://www.google.com/search?q={requete.replace(' ', '+')}"
        ouvrir_en_arriere_plan(url)
        time.sleep(delai)

    bouton_rechercher.config(state="normal")
    bouton_arreter.config(state="disabled")

def arreter_recherches():
    global stop_recherche
    stop_recherche = True

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Recherche Internet Automatisée")

label_liste = tk.Label(fenetre, text="Liste de mots (un par ligne) :")
label_liste.pack()

entree_liste = tk.Text(fenetre, height=10, width=50)
entree_liste.pack()

label_fixe = tk.Label(fenetre, text="Chaîne fixe :")
label_fixe.pack()

entree_fixe = tk.Entry(fenetre, width=50)
entree_fixe.pack()

bouton_rechercher = tk.Button(fenetre, text="Lancer les recherches", command=lancer_recherches)
bouton_rechercher.pack(pady=5)

bouton_arreter = tk.Button(fenetre, text="Arrêter", command=arreter_recherches, state="disabled")
bouton_arreter.pack(pady=5)

fenetre.mainloop()