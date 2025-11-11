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

    # === CAS SPÉCIAL : LATITUDE 0°0'0'' (ÉQUATEUR) ===
    if horizon_data and horizon_data.get('type') == 'ligne_horizontale':
        print("=" * 60)
        print("DÉTECTION LATITUDE 0°0'0'' - GÉNÉRATION LIGNES RAYONNANTES")
        print(f"horizon_data type: {horizon_data.get('type')}")
        print("=" * 60)
        
        # À l'équateur, les heures inégales sont des lignes droites qui rayonnent du centre
        # Il faut 11 lignes (heures 1 à 11) + la ligne verticale de la 6ème heure
        
        # On génère 5 lignes à gauche (heures 7, 8, 9, 10, 11) 
        # et 5 à droite (heures 1, 2, 3, 4, 5)
        # + la 6ème heure (midi) sur l'axe vertical
        
        # Angles : chaque heure = 15° (360° / 24h)
        # À partir de l'Est (0°) dans le sens antihoraire
        # MAIS en coordonnées SVG où Y est inversé
        
        for i in range(1, 6):  # 5 lignes à gauche (heures 7, 8, 9, 10, 11)
            # Heure = 6 + i (donc 7, 8, 9, 10, 11)
            # Angle depuis l'Est : (6+i) * 15° = 105°, 120°, 135°, 150°, 165°
            angle_deg = (6 + i) * 15
            angle_rad = math.radians(angle_deg)
            
            # Point sur le cercle du Cancer (rayon = rayon_cancer)
            x_cancer = rayon_cancer * math.cos(angle_rad)
            y_cancer = rayon_cancer * math.sin(angle_rad)
            x_cancer_svg = cx + x_cancer * facteur
            y_cancer_svg = cy + y_cancer * facteur  # PAS d'inversion - on veut en BAS
            
            # Point sur le cercle du Capricorne (rayon = rayon_capricorne)
            x_capricorne = rayon_capricorne * math.cos(angle_rad)
            y_capricorne = rayon_capricorne * math.sin(angle_rad)
            x_capricorne_svg = cx + x_capricorne * facteur
            y_capricorne_svg = cy + y_capricorne * facteur  # PAS d'inversion - on veut en BAS
            
            p_cancer = {"x": x_cancer_svg, "y": y_cancer_svg}
            p_capricorne = {"x": x_capricorne_svg, "y": y_capricorne_svg}
            
            points_cancer_gauche.append(p_cancer)
            points_capricorne_gauche.append(p_capricorne)
            
            # Ligne droite du Cancer au Capricorne
            courbes_gauche.append({
                "p1": p_cancer,
                "p3": p_capricorne,
                "rayon": 999999,
                "large_arc": 0,
                "sweep": 1,
                "type": "ligne_verticale"
            })
        
        print(f"Nombre de courbes à gauche générées: {len(courbes_gauche)}")
        
        for i in range(1, 6):  # 5 lignes à droite (heures 1, 2, 3, 4, 5)
            # Angle depuis l'Est : i * 15° = 15°, 30°, 45°, 60°, 75°
            angle_deg = i * 15
            angle_rad = math.radians(angle_deg)
            
            # Point sur le cercle du Cancer (rayon = rayon_cancer)
            x_cancer = rayon_cancer * math.cos(angle_rad)
            y_cancer = rayon_cancer * math.sin(angle_rad)
            x_cancer_svg = cx + x_cancer * facteur
            y_cancer_svg = cy + y_cancer * facteur  # PAS d'inversion - on veut en BAS
            
            # Point sur le cercle du Capricorne (rayon = rayon_capricorne)
            x_capricorne = rayon_capricorne * math.cos(angle_rad)
            y_capricorne = rayon_capricorne * math.sin(angle_rad)
            x_capricorne_svg = cx + x_capricorne * facteur
            y_capricorne_svg = cy + y_capricorne * facteur  # PAS d'inversion - on veut en BAS
            
            p_cancer = {"x": x_cancer_svg, "y": y_cancer_svg}
            p_capricorne = {"x": x_capricorne_svg, "y": y_capricorne_svg}
            
            points_cancer_droite.append(p_cancer)
            points_capricorne_droite.append(p_capricorne)
            
            # Ligne droite du Cancer au Capricorne
            courbes_droite.append({
                "p1": p_cancer,
                "p3": p_capricorne,
                "rayon": 999999,
                "large_arc": 0,
                "sweep": 0,
                "type": "ligne_verticale"
            })
        
        # AJOUTER LA 6ÈME HEURE (LIGNE VERTICALE - MIDI)
        # Angle = 90° (vers le haut en coordonnées mathématiques, vers le bas en SVG)
        angle_6h = math.radians(90)
        
        x_6h_cancer = rayon_cancer * math.cos(angle_6h)  # = 0
        y_6h_cancer = rayon_cancer * math.sin(angle_6h)  # = rayon_cancer
        x_6h_cancer_svg = cx + x_6h_cancer * facteur
        y_6h_cancer_svg = cy + y_6h_cancer * facteur
        
        x_6h_capricorne = rayon_capricorne * math.cos(angle_6h)  # = 0
        y_6h_capricorne = rayon_capricorne * math.sin(angle_6h)  # = rayon_capricorne
        x_6h_capricorne_svg = cx + x_6h_capricorne * facteur
        y_6h_capricorne_svg = cy + y_6h_capricorne * facteur
        
        # On l'ajoute aux courbes de droite
        courbes_droite.append({
            "p1": {"x": x_6h_cancer_svg, "y": y_6h_cancer_svg},
            "p3": {"x": x_6h_capricorne_svg, "y": y_6h_capricorne_svg},
            "rayon": 999999,
            "large_arc": 0,
            "sweep": 0,
            "type": "ligne_verticale"
        })
        
        print(f"Nombre de courbes à droite générées: {len(courbes_droite)}")
        print(f"RETOUR: {len(courbes_gauche)} courbes gauche, {len(courbes_droite)} courbes droite")
        print("=" * 60)
        
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

    # === CAS NORMAL : AUTRES LATITUDES ===
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