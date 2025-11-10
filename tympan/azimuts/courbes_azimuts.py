import math
import numpy as np

class CourbesAzimut:
    def __init__(self, rayon_equateur, latitude):
        self.S = rayon_equateur / 2
        self.latitude_deg = latitude
        self.latitude_rad = math.radians(latitude)
        self.resultats = []

    def calculer_courbes(self):
        L = self.latitude_rad
        S = self.S
        NP = 2 * S * math.tan(math.radians((90 - math.degrees(L)) / 2))
        NK = 2 * S / math.cos(L)
        ycentre = NP - NK
        
        # Azimut 0° (droite verticale passant par x=0, allant vers le haut)
        self.resultats.append({
            'azimut': 0,
            'type': 'ligne_verticale',
            'x': 0,
            'color': 'black'
        })
        
        # Azimuts de 5° à 175° (cercles)
        for azimut_deg in range(5, 180, 5):
            alpha_rad = math.radians(azimut_deg)
            try:
                xcentre = 2 * S / (math.cos(L) * math.tan(alpha_rad))
                rayon = 2 * S / (math.cos(L) * math.sin(alpha_rad))
            except ZeroDivisionError:
                continue
            points = []
            for theta in range(0, 361):
                theta_rad = math.radians(theta)
                x = xcentre + rayon * math.cos(theta_rad)
                y = ycentre + rayon * math.sin(theta_rad)
                points.append((x, y))
            color = "black" if azimut_deg % 10 == 0 else "gray"
            self.resultats.append({
                'azimut': azimut_deg,
                'points': points,
                'color': color
            })
        
        # Azimut 180° (droite verticale passant par x=0, allant vers le bas)
        self.resultats.append({
            'azimut': 180,
            'type': 'ligne_verticale',
            'x': 0,
            'color': 'black'
        })
        
        return self.resultats

    def calculer_azimut_specifique(self, azimut_deg):
        L = self.latitude_rad
        S = self.S
        NP = 2 * S * math.tan(math.radians((90 - math.degrees(L)) / 2))
        NK = 2 * S / math.cos(L)
        ycentre = NP - NK
        alpha_rad = math.radians(azimut_deg)
        try:
            xcentre = 2 * S / (math.cos(L) * math.tan(alpha_rad))
            rayon = 2 * S / (math.cos(L) * math.sin(alpha_rad))
            return {
                'centre_x': xcentre,
                'centre_y': ycentre,
                'rayon': rayon
            }
        except ZeroDivisionError:
            return None

    def get_data(self):
        return self.calculer_courbes()

    def generer_courbe_par_point(self, x, y):
        angle = np.degrees(np.arctan2(y, x)) % 360
        return self.generer_courbe(angle)

    def generer_courbe(self, angle):
        L = self.latitude_rad
        S = self.S
        NP = 2 * S * math.tan(math.radians((90 - math.degrees(L)) / 2))
        NK = 2 * S / math.cos(L)
        ycentre = NP - NK
        alpha_rad = math.radians(angle)
        try:
            xcentre = 2 * S / (math.cos(L) * math.tan(alpha_rad))
            rayon = 2 * S / (math.cos(L) * math.sin(alpha_rad))
        except ZeroDivisionError:
            return None
        points = []
        for theta in range(0, 361):
            theta_rad = math.radians(theta)
            x = xcentre + rayon * math.cos(theta_rad)
            y = ycentre + rayon * math.sin(theta_rad)
            points.append((x, y))
        color = "black" if angle % 10 == 0 else "gray"
        return {
            "points": points,
            "color": color,
            "azimut": angle
        }

    def generer_courbe_par_point_svg(self, x_svg, y_svg, facteur):
        """
        Génère une courbe d'azimut exacte qui passe par un point donné en pixels SVG.

        Args:
            x_svg (float): Coordonnée X du point dans le SVG (en pixels)
            y_svg (float): Coordonnée Y du point dans le SVG (en pixels)
            facteur (float): Facteur d'échelle utilisé dans le SVG

        Returns:
            dict: Dictionnaire contenant les points de la courbe, sa couleur, son azimut
        """
        S = self.S
        L_rad = self.latitude_rad

        x_reel = (x_svg - 300) / facteur
        y_reel = (250 - y_svg) / facteur

        azimut = math.degrees(math.atan2(y_reel, x_reel)) % 360
        alpha_rad = math.radians(azimut)

        NP = 2 * S * math.tan((math.pi / 2 - L_rad) / 2)
        NK = 2 * S / math.cos(L_rad)
        ycentre = NP - NK

        try:
            xcentre = 2 * S / (math.cos(L_rad) * math.tan(alpha_rad))
            rayon = 2 * S / (math.cos(L_rad) * math.sin(alpha_rad))
        except ZeroDivisionError:
            return None

        points = []
        for theta in range(361):
            theta_rad = math.radians(theta)
            x = xcentre + rayon * math.cos(theta_rad)
            y = ycentre + rayon * math.sin(theta_rad)
            points.append((x, y))

        return {
            'azimut': azimut,
            'points': points,
            'color': 'gray',
            'stroke_width': 2.5
        }

def generer_courbe_par_trois_points(self, points):
    """
    Génère un chemin SVG (<path>) représentant le cercle passant par trois points donnés.
    Args:
        points (list of tuple): Trois points [(x1, y1), (x2, y2), (x3, y3)]
    Returns:
        str: Une chaîne SVG 'd' pour la balise <path>
    """
    (x1, y1), (x2, y2), (x3, y3) = points

    # Calcul des déterminants pour trouver le centre du cercle
    temp = x2**2 + y2**2
    bc = (x1**2 + y1**2 - temp) / 2
    cd = (temp - x3**2 - y3**2) / 2
    det = (x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2)

    if abs(det) < 1e-6:
        return ""  # Les points sont alignés, pas de cercle

    # Coordonnées du centre
    cx = (bc * (y2 - y3) - cd * (y1 - y2)) / det
    cy = ((x1 - x2) * cd - (x2 - x3) * bc) / det

    # Rayon
    r = math.sqrt((cx - x1)**2 + (cy - y1)**2)

    # Angles de départ et de fin
    angle1 = math.atan2(y1 - cy, x1 - cx)
    angle2 = math.atan2(y2 - cy, x2 - cx)

    # Déterminer le sens du tracé
    large_arc = 0
    sweep_flag = 1

    # SVG path: A rx ry x-axis-rotation large-arc-flag sweep-flag x y
    path = (
        f"M {x1:.2f},{y1:.2f} "
        f"A {r:.2f},{r:.2f} 0 {large_arc} {sweep_flag} {x2:.2f},{y2:.2f}"
    )

    return path