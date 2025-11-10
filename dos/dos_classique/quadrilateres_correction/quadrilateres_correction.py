def generer_quadrilateres_gauche():
    """
    Génère les quadrilatères de remplissage correction gauche
    """
    # Coordonnées exactes reprises du code original
    coordonnees_polygones = [
        "-6.4125,-6.4125 -6.1428,-6.1428 -6.1428,-5.3871 -6.4125,-5.6236",
        "-6.4125,-4.9205 -6.1428,-4.7135 -6.1428,-4.1045 -6.4125,-4.2847",
        "-6.4125,-3.7023 -6.1428,-3.5465 -6.1428,-3.0293 -6.4125,-3.1623",
        "-6.4125,-2.6561 -6.1428,-2.5444 -6.1428,-2.0852 -6.4125,-2.1768",
        "-6.4125,-1.7182 -6.1428,-1.646 -6.1428,-1.2219 -6.4125,-1.2755",
        "-6.4125,-0.8442 -6.1428,-0.8087 -6.1428,-0.4026 -6.4125,-0.4203"
    ]
    
    polygones = []
    for points in coordonnees_polygones:
        polygone = {
            'points': points,
            'fill': 'black',
            'stroke': 'none'
        }
        polygones.append(polygone)
    
    return polygones

def generer_quadrilateres_bas():
    """
    Génère les quadrilatères de remplissage correction bas
    """
    # Coordonnées exactes reprises du code original
    coordonnees_polygones = [
        "-5.6236,-6.4125 -4.9205,-6.4125 -4.7135,-6.1428 -5.3871,-6.1428",
        "-4.2847,-6.4125 -3.7023,-6.4125 -3.5465,-6.1428 -4.1045,-6.1428",
        "-3.1623,-6.4125 -2.6561,-6.4125 -2.5444,-6.1428 -3.0293,-6.1428",
        "-2.1768,-6.4125 -1.7182,-6.4125 -1.646,-6.1428 -2.0852,-6.1428",
        "-1.2755,-6.4125 -0.8442,-6.4125 -0.8087,-6.1428 -1.2219,-6.1428",
        "-0.4203,-6.4125 0.0,-6.4125 0.0,-6.1428 -0.4026,-6.1428",
        "0.4203,-6.4125 0.8442,-6.4125 0.8087,-6.1428 0.4026,-6.1428",
        "1.2755,-6.4125 1.7182,-6.4125 1.646,-6.1428 1.2219,-6.1428",
        "2.1768,-6.4125 2.6561,-6.4125 2.5444,-6.1428 2.0852,-6.1428",
        "3.1623,-6.4125 3.7023,-6.4125 3.5465,-6.1428 3.0293,-6.1428",
        "4.2847,-6.4125 4.9205,-6.4125 4.7135,-6.1428 4.1045,-6.1428",
        "5.6236,-6.4125 6.4125,-6.4125 6.1428,-6.1428 5.3871,-6.1428"
    ]
    
    polygones = []
    for points in coordonnees_polygones:
        polygone = {
            'points': points,
            'fill': 'black',
            'stroke': 'none'
        }
        polygones.append(polygone)
    
    return polygones

def generer_quadrilateres_droite():
    """
    Génère les quadrilatères de remplissage correction droite
    """
    # Coordonnées exactes reprises du code original
    coordonnees_polygones = [
        "6.1428,-5.3871 6.4125,-5.6236 6.4125,-4.9205 6.1428,-4.7135",
        "6.1428,-4.1045 6.4125,-4.2847 6.4125,-3.7023 6.1428,-3.5465",
        "6.1428,-3.0293 6.4125,-3.1623 6.4125,-2.6561 6.1428,-2.5444",
        "6.1428,-2.0852 6.4125,-2.1768 6.4125,-1.7182 6.1428,-1.646",
        "6.1428,-1.2219 6.4125,-1.2755 6.4125,-0.8442 6.1428,-0.8087",
        "6.1428,-0.4026 6.4125,-0.4203 6.4125,0.0 6.1428,0.0"
    ]
    
    polygones = []
    for points in coordonnees_polygones:
        polygone = {
            'points': points,
            'fill': 'black',
            'stroke': 'none'
        }
        polygones.append(polygone)
    
    return polygones

def generer_tous_quadrilateres_correction():
    """
    Génère tous les quadrilatères de correction
    """
    return {
        'quadrilateres_gauche': generer_quadrilateres_gauche(),
        'quadrilateres_bas': generer_quadrilateres_bas(),
        'quadrilateres_droite': generer_quadrilateres_droite()
    }