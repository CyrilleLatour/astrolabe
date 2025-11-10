import math

def generer_subdivisions_jours():
    """
    Génère les subdivisions des jours de l'année (365 traits)
    """
    angle_jour = 360 / 365
    lignes = []
    
    for i in range(365):
        angle_deg = i * angle_jour
        angle_rad = (angle_deg - 90) * math.pi / 180
        x1 = 10.55 * math.cos(angle_rad)
        y1 = 10.55 * math.sin(angle_rad)
        x2 = 10.35 * math.cos(angle_rad)
        y2 = 10.35 * math.sin(angle_rad)
        
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

def generer_subdivisions_mois():
    """
    Génère les subdivisions des mois (12 traits rouges)
    """
    angle_jour_mois = 360 / 365
    jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    jour_cumule = 9
    lignes = []
    
    for mois in range(12):
        jour_cumule += jours_mois[mois]
        angle_deg_mois = jour_cumule * angle_jour_mois
        angle_rad_mois = (angle_deg_mois - 90) * math.pi / 180
        x1_mois = 10.55 * math.cos(angle_rad_mois)
        y1_mois = 10.55 * math.sin(angle_rad_mois)
        x2_mois = 9.45 * math.cos(angle_rad_mois)
        y2_mois = 9.45 * math.sin(angle_rad_mois)
        
        ligne = {
            'x1': round(x1_mois, 3),
            'y1': round(y1_mois, 3),
            'x2': round(x2_mois, 3),
            'y2': round(y2_mois, 3),
            'stroke': 'red',
            'stroke_width': 0.05
        }
        lignes.append(ligne)
    
    return lignes

def generer_subdivisions_5_jours():
    """
    Génère les subdivisions tous les 5 jours
    """
    angle_jour = 360 / 365
    jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    subdivisions_par_mois = [6, 5, 6, 5, 6, 5, 6, 6, 5, 6, 5, 6]  # Jan, Fév, Mar, Avr, Mai, Jun, Jul, Aoû, Sep, Oct, Nov, Déc
    jour_cumule = 9
    lignes = []
    
    for mois in range(12):
        # Position du trait rouge (début du mois)
        debut_mois = jour_cumule
        
        # Ajouter TOUTES les subdivisions pour ce mois
        for subdiv in range(1, subdivisions_par_mois[mois] + 1):
            jour_subdivision = debut_mois + (subdiv * 5)  # 5, 10, 15, 20, 25, 30 jours après le trait rouge
            angle_deg = jour_subdivision * angle_jour
            angle_rad = (angle_deg - 90) * math.pi / 180
            
            x1 = 10 * math.cos(angle_rad)
            y1 = 10 * math.sin(angle_rad)
            x2 = 10.55 * math.cos(angle_rad)
            y2 = 10.55 * math.sin(angle_rad)
            
            ligne = {
                'x1': round(x1, 3),
                'y1': round(y1, 3),
                'x2': round(x2, 3),
                'y2': round(y2, 3),
                'stroke': 'black',
                'stroke_width': 0.02
            }
            lignes.append(ligne)
        
        # Passer au mois suivant
        jour_cumule += jours_mois[mois]
    
    return lignes

def generer_toutes_subdivisions_annee():
    """
    Génère toutes les subdivisions de l'année
    """
    return {
        'subdivisions_jours': generer_subdivisions_jours(),
        'subdivisions_mois': generer_subdivisions_mois(),
        'subdivisions_5_jours': generer_subdivisions_5_jours()
    }




def generer_points_10_jours():
    """
    Points tous les 10 jours à partir du début de chaque mois,
    sur le cercle de centre (0,0) et de rayon r = 10.
    Conventions identiques à tes subdivisions: angle_rad = (angle_deg - 90) * pi/180.
    Retourne une liste de dicts {'x','y','r'} avec r = 0.3 (unités).
    """
    angle_jour = 360 / 365
    jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    subs_10_par_mois = [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]  # 10, 20, (30) jours
    r_cercle = 10
    jour_cumule = 9  # début de mois (trait rouge) comme dans ton code

    points = []
    for m in range(12):
        debut_mois = jour_cumule
        for k in range(1, subs_10_par_mois[m] + 1):
            jour_sub = debut_mois + 10 * k
            angle_deg = jour_sub * angle_jour
            angle_rad = (angle_deg - 90) * math.pi / 180.0
            x = r_cercle * math.cos(angle_rad)
            y = r_cercle * math.sin(angle_rad)
            points.append({'x': x, 'y': y, 'r': 0.3})
        jour_cumule += jours_mois[m]
    return points

def _svg_points_10_jours(points, r_cercle=10, margin=3):
    vb_min = -(r_cercle + margin)
    vb_size = 2 * (r_cercle + margin)
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_min} {vb_min} {vb_size} {vb_size}" width="800" height="800">')
    out.append(f'  <rect x="{vb_min}" y="{vb_min}" width="{vb_size}" height="{vb_size}" fill="white"/>')
    out.append('  <g transform="scale(1,-1)">')  # cartésien: Y vers le haut
    out.append(f'    <circle cx="0" cy="0" r="{r_cercle}" fill="none" stroke="lightgray" stroke-width="0.05"/>')
    for p in points:
        out.append(f'    <circle cx="{p["x"]}" cy="{p["y"]}" r="{p["r"]}" fill="black"/>')
    out.append('  </g>')
    out.append('</svg>')
    return "\n".join(out)

def exporter_points_10_jours_svg(fichier="subdivisions_annee.svg"):
    svg = _svg_points_10_jours(generer_points_10_jours())
    Path(fichier).write_text(svg, encoding="utf-8")
    return fichier

if __name__ == "__main__":
    chemin = exporter_points_10_jours_svg()
    print(f"SVG généré : {chemin}")


# points extérieurs #
