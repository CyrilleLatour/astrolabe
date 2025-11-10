import math
import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

# Ajouter le chemin vers les modules
sys.path.append(os.path.dirname(__file__))

from parametres_cercles_almucantarats import cercle_almucantarat_personnalise

# Import du fichier avec le nom correct (avec +) et le bon chemin
import importlib.util
spec = importlib.util.spec_from_file_location("azimut_module", os.path.join(os.path.dirname(__file__), "parametres_courbe_azimut_90+270.py"))
azimut_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(azimut_module)
calculer_azimut_270 = azimut_module.calculer_azimut_270

def intersection_deux_cercles(c1, r1, c2, r2):
    x0, y0 = c1
    x1, y1 = c2
    d = math.hypot(x1 - x0, y1 - y0)
    if d > r1 + r2:
        return []  # Pas d'intersection
    if d < abs(r1 - r2):
        return []  # Cercle dans l'autre, pas d'intersection
    if d == 0 and r1 == r2:
        return []  # Cercles confondus
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h_sq = r1**2 - a**2
    if h_sq < 0:
        return []  # Pas d'intersection réelle
    h = math.sqrt(h_sq)
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d
    rx = -(y1 - y0) * (h / d)
    ry = (x1 - x0) * (h / d)
    p1 = (x2 + rx, y2 + ry)
    p2 = (x2 - rx, y2 - ry)
    if p1 == p2:
        return [p1]
    else:
        return [p1, p2]

def calculer_regressions_xy(df):
    """
    Calcule les régressions polynomiales pour x et y en fonction de Z
    jusqu'à obtenir R² ≈ 1
    """
    if df.empty:
        print("DataFrame vide, impossible de calculer les régressions")
        return None, None
    
    Z = df[['Z']]
    x_vals = df['x']
    y_vals = df['y']
    
    print(f"\nNombre de points pour la régression : {len(df)}")
    
    # Régression pour X
    print("\n=== RÉGRESSION POUR X ===")
    modele_x = None
    degre_x = None
    meilleur_r2_x = 0
    
    for degree in range(1, min(len(df), 15)):
        try:
            model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
            model.fit(Z, x_vals)
            x_pred = model.predict(Z)
            r2 = r2_score(x_vals, x_pred)
            
            print(f"Degré {degree}: R² = {r2:.10f}")
            
            # Garder le meilleur modèle
            if r2 > meilleur_r2_x:
                meilleur_r2_x = r2
                modele_x = model
                degre_x = degree
            
            # Tolérance plus large pour accepter R² ≈ 1
            if abs(r2 - 1.0) < 1e-6 or r2 > 0.999999:
                modele_x = model
                degre_x = degree
                print(f"✅ R² ≈ 1 atteint au degré {degree}")
                break
                
        except Exception as e:
            print(f"Erreur au degré {degree}: {e}")
    
    # Régression pour Y
    print("\n=== RÉGRESSION POUR Y ===")
    modele_y = None
    degre_y = None
    meilleur_r2_y = 0
    
    for degree in range(1, min(len(df), 15)):
        try:
            model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
            model.fit(Z, y_vals)
            y_pred = model.predict(Z)
            r2 = r2_score(y_vals, y_pred)
            
            print(f"Degré {degree}: R² = {r2:.10f}")
            
            # Garder le meilleur modèle
            if r2 > meilleur_r2_y:
                meilleur_r2_y = r2
                modele_y = model
                degre_y = degree
            
            # Tolérance plus large pour accepter R² ≈ 1
            if abs(r2 - 1.0) < 1e-6 or r2 > 0.999999:
                modele_y = model
                degre_y = degree
                print(f"✅ R² ≈ 1 atteint au degré {degree}")
                break
                
        except Exception as e:
            print(f"Erreur au degré {degree}: {e}")
    
    # Si aucun modèle n'atteint la tolérance, prendre le meilleur
    if modele_x is None and meilleur_r2_x > 0:
        print(f"⚠️ Aucun modèle X n'atteint R² ≈ 1, utilisation du meilleur (R² = {meilleur_r2_x:.10f})")
    
    if modele_y is None and meilleur_r2_y > 0:
        print(f"⚠️ Aucun modèle Y n'atteint R² ≈ 1, utilisation du meilleur (R² = {meilleur_r2_y:.10f})")
    
    # Afficher les formules
    formule_x = ""
    formule_y = ""
    r2_final_x = 0
    r2_final_y = 0
    
    if modele_x:
        coeffs_x = modele_x.named_steps['linearregression'].coef_
        intercept_x = modele_x.named_steps['linearregression'].intercept_
        
        # Calculer R² final
        x_pred_final = modele_x.predict(Z)
        r2_final_x = r2_score(x_vals, x_pred_final)
        
        formule_x_parts = [f"{intercept_x:.6f}"]
        for i in range(1, len(coeffs_x)):
            if coeffs_x[i] >= 0:
                formule_x_parts.append(f"+ {coeffs_x[i]:.6f}·Z^{i}")
            else:
                formule_x_parts.append(f"- {abs(coeffs_x[i]):.6f}·Z^{i}")
        
        formule_x = "x = " + " ".join(formule_x_parts)
        print(f"\n📐 FORMULE X (degré {degre_x}): {formule_x}")
        print(f"📊 R² = {r2_final_x:.10f}")
    
    if modele_y:
        coeffs_y = modele_y.named_steps['linearregression'].coef_
        intercept_y = modele_y.named_steps['linearregression'].intercept_
        
        # Calculer R² final
        y_pred_final = modele_y.predict(Z)
        r2_final_y = r2_score(y_vals, y_pred_final)
        
        formule_y_parts = [f"{intercept_y:.6f}"]
        for i in range(1, len(coeffs_y)):
            if coeffs_y[i] >= 0:
                formule_y_parts.append(f"+ {coeffs_y[i]:.6f}·Z^{i}")
            else:
                formule_y_parts.append(f"- {abs(coeffs_y[i]):.6f}·Z^{i}")
        
        formule_y = "y = " + " ".join(formule_y_parts)
        print(f"\n📐 FORMULE Y (degré {degre_y}): {formule_y}")
        print(f"📊 R² = {r2_final_y:.10f}")
    
    # === GRAPHIQUES ===
    if modele_x and modele_y:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Graphique X
        ax1.scatter(df['Z'], df['x'], color='blue', s=50, alpha=0.7, label='Points calculés')
        
        # Courbe de régression X (prolongée jusqu'à -18°)
        Z_plot = np.linspace(-18, df['Z'].max() + 5, 200)
        Z_plot_df = pd.DataFrame({'Z': Z_plot})
        x_plot = modele_x.predict(Z_plot_df)
        ax1.plot(Z_plot, x_plot, color='green', linewidth=2, label=f'Régression (degré {degre_x})')
        
        # Points extrapolés X (en rouge, même taille)
        Z_extrapoles = [-6, -12, -18]
        for Z_ext in Z_extrapoles:
            x_ext = modele_x.predict(pd.DataFrame({'Z': [Z_ext]}))[0]
            ax1.scatter(Z_ext, x_ext, color='red', s=50, alpha=0.7, label='Extrapolé' if Z_ext == -6 else "")
        
        ax1.set_xlabel('Z (hauteur en °)')
        ax1.set_ylabel('x')
        ax1.set_title('Coordonnées X vs Z')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Ajouter formule et R² sur le graphique X
        ax1.text(0.02, 0.98, formule_x, fontsize=8, transform=ax1.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        ax1.text(0.02, 0.88, f"R² = {r2_final_x:.6f}", fontsize=10, 
                transform=ax1.transAxes, verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
        
        # Graphique Y
        ax2.scatter(df['Z'], df['y'], color='blue', s=50, alpha=0.7, label='Points calculés')
        
        # Courbe de régression Y (prolongée jusqu'à -18°)
        y_plot = modele_y.predict(Z_plot_df)
        ax2.plot(Z_plot, y_plot, color='green', linewidth=2, label=f'Régression (degré {degre_y})')
        
        # Points extrapolés Y (en rouge, même taille)
        for Z_ext in Z_extrapoles:
            y_ext = modele_y.predict(pd.DataFrame({'Z': [Z_ext]}))[0]
            ax2.scatter(Z_ext, y_ext, color='red', s=50, alpha=0.7, label='Extrapolé' if Z_ext == -6 else "")
        
        ax2.set_xlabel('Z (hauteur en °)')
        ax2.set_ylabel('y')
        ax2.set_title('Coordonnées Y vs Z')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Ajouter formule et R² sur le graphique Y
        ax2.text(0.02, 0.98, formule_y, fontsize=8, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        ax2.text(0.02, 0.88, f"R² = {r2_final_y:.6f}", fontsize=10, 
                transform=ax2.transAxes, verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    return modele_x, modele_y

def calculer_intersections(latitude_deg, tol=1e-9):
    # Utiliser les fonctions des autres fichiers
    S = 3  # Paramètre utilisé dans parametres_cercles_almucantarats.py
    
    # Cercle d'azimut 270° avec rayon_equateur = 6
    cx_az, cy_az, r_az = calculer_azimut_270(latitude_deg, rayon_equateur=6)
    
    intersections = []
    
    # De 70 à 0 inclus
    for Z in range(70, -1, -1):
        try:
            # Utiliser la fonction du fichier parametres_cercles_almucantarats.py
            cx_al, cy_al, r_al = cercle_almucantarat_personnalise(Z, latitude_deg, S)
            
            points = intersection_deux_cercles((cx_az, cy_az), r_az, (cx_al, cy_al), r_al)
            print(f"Z={Z}: {len(points)} intersections trouvées, points = {points}")
            
            for (x, y) in points:
                if x <= tol:  # tolérance au lieu de strict <= 0
                    intersections.append({"Z": Z, "x": x, "y": y})
                else:
                    print(f"Point exclu par filtre x>tol : x={x:.6f}, y={y:.6f}")
        except Exception as e:
            print(f"Erreur pour Z={Z}: {e}")
            continue
    
    return pd.DataFrame(intersections)

if __name__ == "__main__":
    lat_str = input("Entrez la latitude en degrés décimaux (ex: 46.2) : ")
    try:
        lat_val = float(lat_str)
        if not (0 <= lat_val <= 90):
            print("Latitude doit être entre 0 et 90.")
            exit(1)
    except ValueError:
        print("Entrée invalide.")
        exit(1)
    
    df = calculer_intersections(lat_val)
    if df.empty:
        print("Aucune intersection retenue à gauche (x <= tol).")
    else:
        print("\n--- Intersections filtrées à gauche (x <= tol) ---")
        # Configurer pandas pour afficher en notation décimale
        pd.set_option('display.float_format', '{:.6f}'.format)
        print(df)
        
        # Calculer et afficher les formules de régression avec graphiques
        modele_x, modele_y = calculer_regressions_xy(df)
        
        # AJOUTER LES POINTS EXTRAPOLÉS AU DATAFRAME ET LES AFFICHER
        if modele_x and modele_y:
            print("\n=== POINTS EXTRAPOLÉS ===")
            Z_extrapoles = [-6, -12, -18]
            points_extrapoles = []
            
            for Z_ext in Z_extrapoles:
                try:
                    x_ext = modele_x.predict(pd.DataFrame({'Z': [Z_ext]}))[0]
                    y_ext = modele_y.predict(pd.DataFrame({'Z': [Z_ext]}))[0]
                    points_extrapoles.append({"Z": Z_ext, "x": x_ext, "y": y_ext})
                    print(f"Z={Z_ext}°: x={x_ext:.6f}, y={y_ext:.6f}")
                except Exception as e:
                    print(f"Erreur extrapolation Z={Z_ext}: {e}")
            
            # Ajouter les points extrapolés au DataFrame principal
            if points_extrapoles:
                df_extrapoles = pd.DataFrame(points_extrapoles)
                df_complet = pd.concat([df, df_extrapoles], ignore_index=True).sort_values('Z', ascending=False)
                
                print("\n--- DATAFRAME COMPLET (calculés + extrapolés) ---")
                print(df_complet)