import math
import pandas as pd

def calcul_intersections(latitude_deg):
    """
    Calcule les intersections des almucantarats avec l'azimut 180°
    
    Args:
        latitude_deg (float): Latitude en degrés
    
    Returns:
        pd.DataFrame: Tableau des intersections avec colonnes Z (°) et y (intersection)
    """
    latitude_rad = math.radians(latitude_deg)
    azimut_deg = 180
    azimut_rad = math.radians(azimut_deg)

    resultats = []

    for z in range(0, 67, 6):  # Z = 0°, 6°, ..., 66°
        z_rad = math.radians(z)
        # Formule simplifiée pour l'intersection avec azimut 180° :
        # x = tan(z) * cos(latitude)
        # y = tan(z) * sin(latitude)
        if z == 0:
            x = 0
            y = 0
        else:
            tan_z = math.tan(z_rad)
            x = tan_z * math.cos(latitude_rad)
            y = tan_z * math.sin(latitude_rad)
        resultats.append({"Z (°)": z, "y (intersection)": round(y, 4)})

    return pd.DataFrame(resultats)

def main():
    """Fonction principale pour exécuter le calcul interactivement"""
    try:
        latitude = float(input("Entrez la latitude en degrés : "))
        tableau = calcul_intersections(latitude)
        print("\nTableau des intersections (azimut 180°) :\n")
        print(tableau.to_string(index=False))
    except ValueError:
        print("Erreur : veuillez entrer un nombre valide pour la latitude.")

if __name__ == "__main__":
    main()