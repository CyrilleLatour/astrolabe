import os
import shutil

racine = os.path.abspath(".")  # Dossier courant
nb = 0

print(f"🧹 Suppression des dossiers '.ipynb_checkpoints' dans : {racine}\n")

for dossier, sous_dossiers, _ in os.walk(racine):
    for sous_dossier in sous_dossiers:
        if sous_dossier == ".ipynb_checkpoints":
            chemin = os.path.join(dossier, sous_dossier)
            try:
                shutil.rmtree(chemin)
                print(f"✅ Supprimé : {chemin}")
                nb += 1
            except Exception as e:
                print(f"❌ Échec sur {chemin} : {e}")

print(f"\n✔️ {nb} dossier(s) supprimé(s).")
