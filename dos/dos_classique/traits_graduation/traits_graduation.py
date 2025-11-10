import math

def generer_traits_1_degre():
    """
    Génère les traits noirs tous les 1° de rayon 11.95 à 11.7
    """
    traits = []
    for i in range(360):
        angle_deg = i
        angle_rad = (angle_deg - 90) * math.pi / 180
        x1 = 11.95 * math.cos(angle_rad)
        y1 = 11.95 * math.sin(angle_rad)
        x2 = 11.7 * math.cos(angle_rad)
        y2 = 11.7 * math.sin(angle_rad)
        
        trait = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        traits.append(trait)
    
    return traits

def generer_traits_5_degres():
    """
    Génère les traits noirs tous les 5° de rayon 12.35 à 11.3
    """
    traits = []
    for i in range(0, 360, 5):
        angle_rad = (i - 90) * math.pi / 180
        x1 = 12.35 * math.cos(angle_rad)
        y1 = 12.35 * math.sin(angle_rad)
        x2 = 11.3 * math.cos(angle_rad)
        y2 = 11.3 * math.sin(angle_rad)
        
        trait = {
            'x1': round(x1, 3),
            'y1': round(y1, 3),
            'x2': round(x2, 3),
            'y2': round(y2, 3),
            'stroke': 'black',
            'stroke_width': 0.03
        }
        traits.append(trait)
    
    return traits

def generer_traits_30_degres():
    """
    Génère les traits rouges tous les 30° de rayon 12.35 à 10.55
    """
    # Coordonnées exactes reprises du code original
    coordonnees_traits = [
        (0.000, -12.35, 0.000, -10.55),
        (6.175, -10.706, 5.279, -9.094),
        (10.706, -6.175, 9.094, -5.279),
        (12.35, 0.000, 10.55, 0.000),
        (10.706, 6.175, 9.094, 5.279),
        (6.175, 10.706, 5.279, 9.094),
        (0.000, 12.35, 0.000, 10.55),
        (-6.175, 10.706, -5.279, 9.094),
        (-10.706, 6.175, -9.094, 5.279),
        (-12.35, 0.000, -10.55, 0.000),
        (-10.706, -6.175, -9.094, -5.279),
        (-6.175, -10.706, -5.279, -9.094)
    ]
    
    traits = []
    for x1, y1, x2, y2 in coordonnees_traits:
        trait = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'red',
            'stroke_width': 0.05
        }
        traits.append(trait)
    
    return traits

def generer_tous_traits_graduation():
    """
    Génère tous les traits de graduation
    """
    return {
        'traits_1_degre': generer_traits_1_degre(),
        'traits_5_degres': generer_traits_5_degres(),
        'traits_30_degres': generer_traits_30_degres()
    }