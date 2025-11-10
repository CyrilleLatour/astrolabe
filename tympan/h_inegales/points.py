import math

# ======================================================================
# 🔹 GÉNÉRATION DES ÉLÉMENTS GRAPHIQUES DU TYMPAN
# ----------------------------------------------------------------------
# Version : Points + toutes les courbes d'heures inégales
# ======================================================================

def calculer_cercle_3_points(p1, p2, p3):
    """
    Calcule le centre et le rayon du cercle passant par 3 points.
    Retourne (cx, cy, rayon) ou None si les points sont alignés.
    """
    x1, y1 = p1['x'], p1['y']
    x2, y2 = p2['x'], p2['y']
    x3, y3 = p3['x'], p3['y']
    
    # Calcul des coefficients
    A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
    
    if abs(A) < 1e-10:  # Points alignés
        return None
    
    B = (x1**2 + y1**2) * (y3 - y2) + (x2**2 + y2**2) * (y1 - y3) + (x3**2 + y3**2) * (y2 - y1)
    C = (x1**2 + y1**2) * (x2 - x3) + (x2**2 + y2**2) * (x3 - x1) + (x3**2 + y3**2) * (x1 - x2)
    
    cx = -B / (2 * A)
    cy = -C / (2 * A)
    
    rayon = math.sqrt((x1 - cx)**2 + (y1 - cy)**2)
    
    return (cx, cy, rayon)


def generer_points_cercles(cx, cy, facteur, rayon_cancer, rayon_equateur, rayon_capricorne, angle_max_deg, horizon_data):
    """
    Génère les points sur Cancer, Équateur et Capricorne + toutes les courbes
    """

    points_cancer_gauche = []
    points_cancer_droite = []
    points_equateur_gauche = []
    points_equateur_droite = []
    points_capricorne_gauche = []
    points_capricorne_droite = []
    courbes_gauche = []
    courbes_droite = []

    # === CALCUL DE L'ANGLE DE L'HORIZON ===
    if horizon_data and horizon_data.get('type') != 'ligne_horizontale':
        rayon_horizon = horizon_data['rayon']
        cy_horizon = horizon_data['cy']
    else:
        return {
            "points_cancer_gauche": [],
            "points_cancer_droite": [],
            "points_equateur_gauche": [],
            "points_equateur_droite": [],
            "points_capricorne_gauche": [],
            "points_capricorne_droite": [],
            "courbes_gauche": [],
            "courbes_droite": []
        }
    
    # === POINTS SUR LE CERCLE DU CANCER ===
    r1 = rayon_cancer
    r2 = rayon_horizon
    d = cy_horizon
    
    y_inter_cancer = (r1**2 - r2**2 + d**2) / (2 * d)
    x_inter_sq_cancer = r1**2 - y_inter_cancer**2
    
    if x_inter_sq_cancer >= 0:
        x_inter_cancer = -math.sqrt(x_inter_sq_cancer)
        angle_horizon_cancer = math.atan2(y_inter_cancer, x_inter_cancer)
    else:
        angle_horizon_cancer = None
    
    if angle_horizon_cancer is not None:
        y_vert_cancer = -rayon_cancer
        angle_verticale_cancer = math.atan2(y_vert_cancer, 0)
        
        angle_total_cancer = angle_verticale_cancer - angle_horizon_cancer
        pas_cancer = angle_total_cancer / 6
        
        for i in range(1, 6):
            angle = angle_horizon_cancer + i * pas_cancer
            
            x_point = rayon_cancer * math.cos(angle)
            y_point = rayon_cancer * math.sin(angle)
            
            x_point_svg = cx + x_point * facteur
            y_point_svg = cy - y_point * facteur
            
            points_cancer_gauche.append({"x": x_point_svg, "y": y_point_svg})
            
            x_point_droite_svg = cx - (x_point_svg - cx)
            points_cancer_droite.append({"x": x_point_droite_svg, "y": y_point_svg})
    
    # === POINTS SUR LE CERCLE DE L'ÉQUATEUR ===
    r1 = rayon_equateur
    
    y_inter_equateur = (r1**2 - r2**2 + d**2) / (2 * d)
    x_inter_sq_equateur = r1**2 - y_inter_equateur**2
    
    if x_inter_sq_equateur >= 0:
        x_inter_equateur = -math.sqrt(x_inter_sq_equateur)
        angle_horizon_equateur = math.atan2(y_inter_equateur, x_inter_equateur)
    else:
        angle_horizon_equateur = None
    
    if angle_horizon_equateur is not None:
        y_vert_equateur = -rayon_equateur
        angle_verticale_equateur = math.atan2(y_vert_equateur, 0)
        
        # Si angle_verticale < angle_horizon, on doit passer par -180° (en bas)
        if angle_verticale_equateur < angle_horizon_equateur:
            angle_verticale_equateur_ajuste = angle_verticale_equateur + 2 * math.pi
            angle_total_equateur = angle_verticale_equateur_ajuste - angle_horizon_equateur
        else:
            angle_total_equateur = angle_verticale_equateur - angle_horizon_equateur
        
        pas_equateur = angle_total_equateur / 6
        
        for i in range(1, 6):
            angle = angle_horizon_equateur + i * pas_equateur
            
            x_point = rayon_equateur * math.cos(angle)
            y_point = rayon_equateur * math.sin(angle)
            
            x_point_svg = cx + x_point * facteur
            y_point_svg = cy - y_point * facteur
            
            points_equateur_gauche.append({"x": x_point_svg, "y": y_point_svg})
            
            x_point_droite_svg = cx - (x_point_svg - cx)
            points_equateur_droite.append({"x": x_point_droite_svg, "y": y_point_svg})
    
    # === POINTS SUR LE CERCLE DU CAPRICORNE ===
    r1 = rayon_capricorne
    
    # Intersection avec l'horizon
    y_inter_capricorne = (r1**2 - r2**2 + d**2) / (2 * d)
    x_inter_sq_capricorne = r1**2 - y_inter_capricorne**2
    
    if x_inter_sq_capricorne >= 0:
        x_inter_capricorne = -math.sqrt(x_inter_sq_capricorne)
        angle_horizon_capricorne = math.atan2(y_inter_capricorne, x_inter_capricorne)
        
        # Intersection avec la verticale
        y_vert_capricorne = -rayon_capricorne
        angle_verticale_capricorne = math.atan2(y_vert_capricorne, 0)
        
        # Si angle_verticale < angle_horizon, on doit passer par -180° (en bas)
        if angle_verticale_capricorne < angle_horizon_capricorne:
            angle_verticale_capricorne_ajuste = angle_verticale_capricorne + 2 * math.pi
            angle_total_capricorne = angle_verticale_capricorne_ajuste - angle_horizon_capricorne
        else:
            angle_total_capricorne = angle_verticale_capricorne - angle_horizon_capricorne
        
        pas_capricorne = angle_total_capricorne / 6
        
        for i in range(1, 6):
            angle = angle_horizon_capricorne + i * pas_capricorne
            
            x_point = rayon_capricorne * math.cos(angle)
            y_point = rayon_capricorne * math.sin(angle)
            
            x_point_svg = cx + x_point * facteur
            y_point_svg = cy - y_point * facteur
            
            points_capricorne_gauche.append({"x": x_point_svg, "y": y_point_svg})
            
            x_point_droite_svg = cx - (x_point_svg - cx)
            points_capricorne_droite.append({"x": x_point_droite_svg, "y": y_point_svg})
    
    # === COURBES D'HEURES INÉGALES ===
    # Courbes à gauche
    for i in range(5):
        if i < len(points_cancer_gauche) and i < len(points_equateur_gauche) and i < len(points_capricorne_gauche):
            p1 = points_cancer_gauche[i]
            p2 = points_equateur_gauche[i]
            p3 = points_capricorne_gauche[i]
            
            resultat = calculer_cercle_3_points(p1, p2, p3)
            
            if resultat:
                cx_arc, cy_arc, rayon_arc = resultat
                
                courbes_gauche.append({
                    "p1": p1,
                    "p3": p3,
                    "rayon": rayon_arc,
                    "large_arc": 0,
                    "sweep": 1
                })
    
    # Courbes à droite
    for i in range(5):
        if i < len(points_cancer_droite) and i < len(points_equateur_droite) and i < len(points_capricorne_droite):
            p1 = points_cancer_droite[i]
            p2 = points_equateur_droite[i]
            p3 = points_capricorne_droite[i]
            
            resultat = calculer_cercle_3_points(p1, p2, p3)
            
            if resultat:
                cx_arc, cy_arc, rayon_arc = resultat
                
                courbes_droite.append({
                    "p1": p1,
                    "p3": p3,
                    "rayon": rayon_arc,
                    "large_arc": 0,
                    "sweep": 0  # Inversé pour le bon sens à droite
                })

    return {
        "points_cancer_gauche": points_cancer_gauche,
        "points_cancer_droite": points_cancer_droite,
        "points_equateur_gauche": points_equateur_gauche,
        "points_equateur_droite": points_equateur_droite,
        "points_capricorne_gauche": points_capricorne_gauche,
        "points_capricorne_droite": points_capricorne_droite,
        "courbes_gauche": courbes_gauche,
        "courbes_droite": courbes_droite
    }