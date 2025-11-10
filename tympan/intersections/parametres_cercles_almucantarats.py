import math
import pandas as pd

def cercle_almucantarat_personnalise(Z_deg, L_deg, S):
    A_B = math.radians((180 - L_deg - Z_deg) / 2)
    A_C = math.radians((Z_deg - L_deg) / 2)
    B = 2 * S * math.tan(A_B)
    C = 2 * S * math.tan(A_C)
    
    R = (B - C) / 2
    y_centre = B - R
    
    cx = 0
    return cx, y_centre, R

def calculer_cercles_almucantarats(latitude_deg, S=3, Z_min=0, Z_max=90, pas=1):
    resultats = []
    for Z in range(Z_min, Z_max + 1, pas):
        cx, cy, r = cercle_almucantarat_personnalise(Z, latitude_deg, S)
        resultats.append({"Z": Z, "cx": cx, "cy": cy, "rayon": r})
    return pd.DataFrame(resultats)

if __name__ == "__main__":
    print("=== CALCUL DES ALMUCANTARATS ===")
    ma_latitude = float(input("Quelle latitude voulez-vous (en degrés) ? "))
    
    print(f"\nCalcul pour latitude = {ma_latitude}°")
    df_cercles = calculer_cercles_almucantarats(latitude_deg=ma_latitude)
    pd.set_option('display.float_format', '{:.15f}'.format)
    print(df_cercles)
    
    print(f"\nVérification:")
    print(f"Z=0° (horizon): rayon = {df_cercles[df_cercles['Z']==0]['rayon'].iloc[0]:.6f}")
    print(f"Z=90° (zénith): rayon = {df_cercles[df_cercles['Z']==90]['rayon'].iloc[0]:.6f}")