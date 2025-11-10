import math

def calculer_azimut_270(latitude_deg, rayon_equateur=6):
    S = rayon_equateur / 2
    L_rad = math.radians(latitude_deg)
    
    NP = 2 * S * math.tan(math.radians((90 - latitude_deg) / 2))
    NK = 2 * S / math.cos(L_rad)
    ycentre = NP - NK
    
    xcentre = 0
    rayon = abs(2 * S / (math.cos(L_rad) * math.sin(math.radians(270))))
    
    return xcentre, ycentre, rayon

if __name__ == "__main__":
    latitude = float(input("Entrez une latitude (en degrés) : "))
    x_centre, y_centre, rayon = calculer_azimut_270(latitude)
    
    print(f"Pour latitude = {latitude}°:")
    print(f"Paramètres du cercle d'azimut 270°:")
    print(f"x_centre = {x_centre:.3f}")
    print(f"y_centre = {y_centre:.3f}")
    print(f"rayon = {rayon:.3f}")