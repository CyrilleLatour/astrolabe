# 📁 Ajout du chemin vers le projet Flask
import sys
import os
chemin_projet = r"C:\Users\admin\Dropbox\00e-NET\0PROJETS\0ASTROLABE\00pythonAstrolabe2"
sys.path.append(chemin_projet)

# 📦 Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from tympan.almucantarats.almucantarats import Almucantarats

# 📥 Demande de la latitude
latitude_input = input("Entrez la latitude en degrés décimaux (ex: 46.2) : ")
try:
    latitude = float(latitude_input)
except ValueError:
    print("Latitude invalide.")
    latitude = None

# 🧾 Paramètres identiques à views.py
rayon_equateur = 6

if latitude is not None:
    alm = Almucantarats(rayon_equateur, latitude)
    resultats = []
    
    # ✅ Données réelles (Z = 0 à 65)
    Z_reels = list(range(0, 66 + 1, 5))
    for Z in Z_reels:
        cercle = alm.calculer_almucantarat(Z)
        if cercle:
            y_cartesien = cercle["cy"] - cercle["rayon"]
            resultats.append({
                "Z": Z,
                "y_cartesien": y_cartesien,
                "extrapole": False
            })
    
    # 📈 Régression polynomiale - Trouver le degré qui donne R² = 1
    df_reel = pd.DataFrame(resultats)
    X = df_reel[["Z"]]
    y = df_reel["y_cartesien"]
    
    meilleur_modele = None
    degre_optimal = None
    
    for degree in range(1, 15):  # Tester jusqu'à degré 14
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        
        if abs(r2 - 1.0) < 1e-10:  # R² = 1 avec tolérance
            meilleur_modele = model
            degre_optimal = degree
            break
    
    if meilleur_modele is None:
        print("Aucun modèle avec R² = 1 trouvé.")
        exit()
    
    # Coefficients et formule
    coeffs = meilleur_modele.named_steps['linearregression'].coef_
    intercept = meilleur_modele.named_steps['linearregression'].intercept_
    
    formule_parts = [f"{intercept:.6f}"]
    for i in range(1, len(coeffs)):
        if coeffs[i] >= 0:
            formule_parts.append(f"+ {coeffs[i]:.6f}·Z^{i}")
        else:
            formule_parts.append(f"- {abs(coeffs[i]):.6f}·Z^{i}")
    
    formule = "y = " + " ".join(formule_parts)
    
    # 🔮 Extrapolation pour Z = -6, -12, -18
    Z_extrapoles = [-6, -12, -18]
    for Z in Z_extrapoles:
        y_ext = meilleur_modele.predict(pd.DataFrame({"Z": [Z]}))[0]
        resultats.append({
            "Z": Z,
            "y_cartesien": y_ext,
            "extrapole": True
        })
    
    # 📋 Tableau final
    df_all = pd.DataFrame(resultats).sort_values(by="Z", ascending=True)
    print(df_all[["Z", "y_cartesien"]])
    
    # 📊 Affichage graphique
    plt.figure(figsize=(12, 8))
    for _, row in df_all.iterrows():
        color = 'red' if row["extrapole"] else 'blue'
        marker = 'o' if not row["extrapole"] else 's'  # Carré pour extrapolés
        plt.scatter(row["Z"], row["y_cartesien"], color=color, marker=marker, s=50)
   
    # Courbe de régression
    Z_plot = pd.DataFrame({"Z": np.linspace(-20, 70, 200)})
    y_plot = meilleur_modele.predict(Z_plot)
    plt.plot(Z_plot["Z"], y_plot, color='green', linewidth=2, label=f'Régression polynomiale (degré {degre_optimal})')
    
    plt.title("Coordonnées Y cartésiennes des intersections avec extrapolation")
    plt.xlabel("Z (hauteur en °)")
    plt.ylabel("y cartésien")
    plt.grid(True)
    plt.legend()
    
    # ➕ Formule + R² dans le coin haut gauche
    plt.text(0.02, 0.98, formule, fontsize=8, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    plt.text(0.02, 0.88, f"R² = 1.000000 (degré {degre_optimal})", fontsize=10, 
             transform=plt.gca().transAxes, verticalalignment='top', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n✅ Modèle trouvé avec R² = 1 au degré {degre_optimal}")
    print(f"📐 Formule: {formule}")
    
else:
    print("❌ Latitude invalide. Aucun calcul effectué.")