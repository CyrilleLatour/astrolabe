import math

def generer_subdivisions_internes_gauche_1_degre():
    """
    Génère les subdivisions internes gauches tous les 1° (91° à 179°)
    Rayon 8.55 → 8.8
    """
    lignes = []
    for angle in range(91, 180):  # 91° à 179°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 8.8 * math.cos(angle_rad)
        y2 = 8.8 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_gauche_15_degres():
    """
    Génère les 5 traits spéciaux gauche (105°, 120°, 135°, 150°, 165°)
    Rayon 8.55 → 9.725
    """
    angles_speciaux = [105, 120, 135, 150, 165]
    lignes = []
    
    for angle in angles_speciaux:
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.725 * math.cos(angle_rad)
        y2 = 9.725 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_gauche_5_degres():
    """
    Génère les subdivisions internes gauches tous les 5° (95° à 175°)
    Rayon 8.55 → 9.05
    """
    lignes = []
    for angle in range(95, 180, 5):  # 95° à 175° par pas de 5°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.05 * math.cos(angle_rad)
        y2 = 9.05 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.025
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_gauche_10_degres():
    """
    Génère les subdivisions internes gauches tous les 10° (100° à 170°)
    Rayon 8.55 → 9.45
    """
    lignes = []
    for angle in range(100, 180, 10):  # 100° à 170° par pas de 10°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.45 * math.cos(angle_rad)
        y2 = 9.45 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.035
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_droite_1_degre():
    """
    Génère les subdivisions internes droite tous les 1° (1° à 89°)
    Rayon 8.55 → 8.8
    """
    lignes = []
    for angle in range(1, 90):  # 1° à 89°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 8.8 * math.cos(angle_rad)
        y2 = 8.8 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_droite_5_degres():
    """
    Génère les subdivisions internes droite tous les 5° (5° à 85°)
    Rayon 8.55 → 9.05
    """
    lignes = []
    for angle in range(5, 90, 5):  # 5° à 85° par pas de 5°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.05 * math.cos(angle_rad)
        y2 = 9.05 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.025
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_droite_10_degres():
    """
    Génère les subdivisions internes droite tous les 10° (10° à 80°)
    Rayon 8.55 → 9.45
    """
    lignes = []
    for angle in range(10, 90, 10):  # 10° à 80° par pas de 10°
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.45 * math.cos(angle_rad)
        y2 = 9.45 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.035
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_internes_droite_15_degres():
    """
    Génère les 5 traits spéciaux droite (15°, 30°, 45°, 60°, 75°)
    Rayon 8.55 → 9.725
    """
    angles_speciaux = [15, 30, 45, 60, 75]
    lignes = []
    
    for angle in angles_speciaux:
        angle_rad = angle * math.pi / 180
        x1 = 8.55 * math.cos(angle_rad)
        y1 = 8.55 * math.sin(angle_rad)
        x2 = 9.725 * math.cos(angle_rad)
        y2 = 9.725 * math.sin(angle_rad)
        
        ligne = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_toutes_subdivisions_internes():
    """
    Génère toutes les subdivisions internes
    """
    return {
        'subdivisions_gauche_1_degre': generer_subdivisions_internes_gauche_1_degre(),
        'subdivisions_gauche_15_degres': generer_subdivisions_internes_gauche_15_degres(),
        'subdivisions_gauche_5_degres': generer_subdivisions_internes_gauche_5_degres(),
        'subdivisions_gauche_10_degres': generer_subdivisions_internes_gauche_10_degres(),
        'subdivisions_droite_1_degre': generer_subdivisions_internes_droite_1_degre(),
        'subdivisions_droite_5_degres': generer_subdivisions_internes_droite_5_degres(),
        'subdivisions_droite_10_degres': generer_subdivisions_internes_droite_10_degres(),
        'subdivisions_droite_15_degres': generer_subdivisions_internes_droite_15_degres()
    }