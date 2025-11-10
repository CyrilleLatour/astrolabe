import math

def generer_diagonales_gauche_25():
    """
    Génère les 25 diagonales gauche (x1=-6.68216, x2=-6.4125, angles 225°-180°)
    """
    x1 = -6.68216
    x2 = -6.4125
    angle_depart = 225
    angle_arrivee = 180
    
    lignes = []
    for i in range(25):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 24
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.03
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_gauche_13():
    """
    Génère les 13 diagonales gauche (x1=-6.4125, x2=-6.1428, angles 225°-180°)
    """
    x1 = -6.4125
    x2 = -6.1428
    angle_depart = 225
    angle_arrivee = 180
    
    lignes = []
    for i in range(13):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 12
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_gauche_5():
    """
    Génère les 5 diagonales gauche (x1=-6.1428, x2=-5.8731, angles 225°-180°)
    """
    x1 = -6.1428
    x2 = -5.8731
    angle_depart = 225
    angle_arrivee = 180
    
    lignes = []
    for i in range(5):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 4
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_bas_49():
    """
    Génère les 49 diagonales bas (y1=-6.6822, y2=-6.4125, angles 225°-315°)
    """
    y_bas = -6.6822
    y_haut = -6.4125
    total = 49
    angle_depart = 225
    angle_fin = 315
    pas = (angle_fin - angle_depart) / (total - 1)
    
    lignes = []
    for i in range(total):
        angle_deg = angle_depart + i * pas
        angle_rad = angle_deg * math.pi / 180
        tan_theta = math.tan(angle_rad)
        
        if abs(tan_theta) < 1e-6:
            continue
        
        x1 = y_bas / tan_theta
        y1 = y_bas
        x2 = y_haut / tan_theta
        y2 = y_haut
        
        ligne = {
            'x1': round(x1, 5),
            'y1': round(y1, 5),
            'x2': round(x2, 5),
            'y2': round(y2, 5),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_bas_25():
    """
    Génère les 25 diagonales bas (y1=-6.4125, y2=-6.1428, angles 225°-315°)
    """
    y_bas = -6.4125
    y_haut = -6.1428
    total = 25
    angle_depart = 225
    angle_fin = 315
    pas = (angle_fin - angle_depart) / (total - 1)
    
    lignes = []
    for i in range(total):
        angle_deg = angle_depart + i * pas
        angle_rad = angle_deg * math.pi / 180
        tan_theta = math.tan(angle_rad)
        
        if abs(tan_theta) < 1e-6:
            continue
        
        x1 = y_bas / tan_theta
        y1 = y_bas
        x2 = y_haut / tan_theta
        y2 = y_haut
        
        ligne = {
            'x1': round(x1, 5),
            'y1': round(y1, 5),
            'x2': round(x2, 5),
            'y2': round(y2, 5),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_bas_9():
    """
    Génère les 9 diagonales bas (y1=-6.1428, y2=-5.8731, angles 225°-315°)
    """
    y_bas = -6.1428
    y_haut = -5.8731
    total = 9
    angle_depart = 225
    angle_fin = 315
    pas = (angle_fin - angle_depart) / (total - 1)
    
    lignes = []
    for i in range(total):
        angle_deg = angle_depart + i * pas
        angle_rad = angle_deg * math.pi / 180
        tan_theta = math.tan(angle_rad)
        
        if abs(tan_theta) < 1e-6:
            continue
        
        x1 = y_bas / tan_theta
        y1 = y_bas
        x2 = y_haut / tan_theta
        y2 = y_haut
        
        ligne = {
            'x1': round(x1, 5),
            'y1': round(y1, 5),
            'x2': round(x2, 5),
            'y2': round(y2, 5),
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_droite_25():
    """
    Génère les 25 diagonales droite (x1=6.68216, x2=6.4125, angles 315°-360°)
    """
    x1 = 6.68216
    x2 = 6.4125
    angle_depart = 315
    angle_arrivee = 360
    
    lignes = []
    for i in range(25):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 24
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.03
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_droite_13():
    """
    Génère les 13 diagonales droite (x1=6.4125, x2=6.1428, angles 315°-360°)
    """
    x1 = 6.4125
    x2 = 6.1428
    angle_depart = 315
    angle_arrivee = 360
    
    lignes = []
    for i in range(13):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 12
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_diagonales_droite_5():
    """
    Génère les 5 diagonales droite (x1=6.1428, x2=5.8731, angles 315°-360°)
    """
    x1 = 6.1428
    x2 = 5.8731
    angle_depart = 315
    angle_arrivee = 360
    
    lignes = []
    for i in range(5):
        angle = angle_depart + (angle_arrivee - angle_depart) * i / 4
        angle_rad = angle * math.pi / 180
        y1 = x1 * math.tan(angle_rad)
        y2 = x2 * math.tan(angle_rad)
        
        ligne = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stroke': 'black',
            'stroke_width': 0.02
        }
        lignes.append(ligne)
    
    return lignes

def generer_toutes_diagonales_correction():
    """
    Génère toutes les diagonales de correction
    """
    return {
        'diagonales_gauche_25': generer_diagonales_gauche_25(),
        'diagonales_gauche_13': generer_diagonales_gauche_13(),
        'diagonales_gauche_5': generer_diagonales_gauche_5(),
        'diagonales_bas_49': generer_diagonales_bas_49(),
        'diagonales_bas_25': generer_diagonales_bas_25(),
        'diagonales_bas_9': generer_diagonales_bas_9(),
        'diagonales_droite_25': generer_diagonales_droite_25(),
        'diagonales_droite_13': generer_diagonales_droite_13(),
        'diagonales_droite_5': generer_diagonales_droite_5()
    }