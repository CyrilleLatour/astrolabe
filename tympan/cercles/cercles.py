import math

class CerclesPrincipaux:
    def __init__(self, rayon_equateur):
        self.rayon_equateur = float(rayon_equateur)
    
    def get_data(self):
        """Calcule les données pour les cercles principaux"""
        # Ratios des rayons par rapport à l'équateur
        ratio_cancer = 3.939 / 6
        ratio_capricorne = 9.141 / 6
        ratio_suppl = 10.5 / 6
    
        # Calcul des rayons
        rayon_cancer = self.rayon_equateur * ratio_cancer
        rayon_capricorne = self.rayon_equateur * ratio_capricorne
        rayon_suppl = self.rayon_equateur * ratio_suppl
    
        # Calcul de l'écliptique
        LTC = 23.44  # Obliquité de l'écliptique
        S = self.rayon_equateur / 2
        rayon_ecliptique = S * (math.tan(math.radians((90 + LTC) / 2)) + math.tan(math.radians((90 - LTC) / 2)))
        position_centre_ecliptique = rayon_ecliptique - 2 * S * math.tan(math.radians((90 - LTC) / 2))
    
        return {
            "rayon_equateur": self.rayon_equateur,
            "rayon_cancer": rayon_cancer,
            "rayon_capricorne": rayon_capricorne,
            "rayon_suppl": rayon_suppl,
            "rayon_ecliptique": rayon_ecliptique,
            "position_centre_ecliptique": position_centre_ecliptique
        }

class Almucantarats:
    def __init__(self, rayon_equateur, latitude_deg):
        self.rayon_equateur = float(rayon_equateur)
        self.latitude_deg = float(latitude_deg)

    def compute(self, z_degres):
        z_rad = math.radians(z_degres)
        phi_rad = math.radians(self.latitude_deg)

        try:
            rayon = self.rayon_equateur * math.cos(phi_rad) / math.cos(z_rad)
            centre_y = self.rayon_equateur * math.tan(z_rad) * math.sin(phi_rad)
            return {"z": z_degres, "rayon": rayon, "centre_y": centre_y}
        except Exception:
            return {"z": z_degres, "rayon": None, "centre_y": None}
