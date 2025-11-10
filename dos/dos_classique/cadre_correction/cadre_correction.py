def generer_cadre_gauche_correction():
    """
    Génère les lignes du cadre gauche de correction
    """
    # Coordonnées exactes reprises du code original
    coordonnees_lignes = [
        (-6.68216, 0, -6.68216, -6.68216),
        (-6.4125, 0, -6.4125, -6.4125),
        (-6.1425, 0, -6.1425, -6.1425),
        (-5.8731, 0, -5.8731, -5.8731)
    ]
    
    lignes = []
    for x1, y1, x2, y2 in coordonnees_lignes:
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_cadre_bas_correction():
    """
    Génère les lignes du cadre bas de correction
    """
    # Coordonnées exactes reprises du code original
    coordonnees_lignes = [
        (-6.68216, -6.68216, 6.68216, -6.68216),
        (-6.4125, -6.4125, 6.4125, -6.4125),
        (-6.1428, -6.1428, 6.1428, -6.1428),
        (-5.8731, -5.8731, 5.8731, -5.8731)
    ]
    
    lignes = []
    for x1, y1, x2, y2 in coordonnees_lignes:
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_cadre_droit_correction():
    """
    Génère les lignes du cadre droit de correction
    """
    # Coordonnées exactes reprises du code original
    coordonnees_lignes = [
        (6.68216, -6.68216, 6.68216, 0),
        (6.4125, -6.4125, 6.4125, 0),
        (6.1428, -6.1428, 6.1428, 0),
        (5.8731, -5.8731, 5.8731, 0)
    ]
    
    lignes = []
    for x1, y1, x2, y2 in coordonnees_lignes:
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_tous_cadres_correction():
    """
    Génère tous les cadres de correction
    """
    return {
        'cadre_gauche': generer_cadre_gauche_correction(),
        'cadre_bas': generer_cadre_bas_correction(),
        'cadre_droit': generer_cadre_droit_correction()
    }