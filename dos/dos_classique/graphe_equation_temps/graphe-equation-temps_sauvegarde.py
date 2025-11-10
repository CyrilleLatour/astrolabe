import math

def generer_cadre_graphique():
    """GÃ©nÃ¨re le cadre du graphique de l'Ã©quation du temps"""
    
    cadre = []
    
    # CÃ´tÃ© gauche
    cadre.append({
        'x1': -4.7, 'y1': 0.75, 'x2': -4.7, 'y2': 5.7,
        'stroke': 'black', 'stroke_width': 0.02, 'fill': 'none',
        'vector_effect': 'non-scaling-stroke'
    })
    
    # CÃ´tÃ© bas
    cadre.append({
        'x1': -4.7, 'y1': 5.7, 'x2': 4.7, 'y2': 5.7,
        'stroke': 'black', 'stroke_width': 0.02, 'fill': 'none',
        'vector_effect': 'non-scaling-stroke'
    })
    
    # CÃ´tÃ© droit
    cadre.append({
        'x1': 4.7, 'y1': 5.7, 'x2': 4.7, 'y2': 0.75,
        'stroke': 'black', 'stroke_width': 0.02, 'fill': 'none',
        'vector_effect': 'non-scaling-stroke'
    })
    
    # CÃ´tÃ© haut
    cadre.append({
        'x1': 4.7, 'y1': 0.75, 'x2': -4.7, 'y2': 0.75,
        'stroke': 'black', 'stroke_width': 0.02, 'fill': 'none',
        'vector_effect': 'non-scaling-stroke'
    })
    
    return cadre


def generer_lignes_verticales():
    """GÃ©nÃ¨re les lignes verticales (rouges pour les mois, grises pour les 10 jours)
       et ajoute les abrÃ©viations des mois.
    """

    lignes = []

    # Nombre de jours par mois (annÃ©e non bissextile)
    jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    abreviations = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

    # Largeur totale (x de -4.7 Ã  +4.7 â†' 9.4)
    largeur_totale = 9.4
    # Conversion jour â†' x
    def jour_to_x(jour):
        return -4.7 + (jour - 1) * largeur_totale / 365

    jour_cumule = 1  # 1er janvier

    for mois in range(12):
        nb_jours = jours_mois[mois]
        debut_mois = jour_cumule
        fin_mois = jour_cumule + nb_jours

        # Ligne rouge dÃ©but de mois
        x_debut = jour_to_x(debut_mois)
        lignes.append({
            'x1': x_debut, 'y1': 0.75, 'x2': x_debut, 'y2': 5.95,
            'stroke': 'red', 'stroke_width': 0.015,
            'vector_effect': 'non-scaling-stroke'
        })

        # Lignes grises tous les 10 jours
        for d in range(debut_mois + 10, fin_mois, 10):
            x_sep = jour_to_x(d)
            lignes.append({
                'x1': x_sep, 'y1': 0.75, 'x2': x_sep, 'y2': 5.7,
                'stroke': 'grey', 'stroke_width': 0.02,
                'vector_effect': 'non-scaling-stroke'
            })

        # Ligne rouge fin de mois
        x_fin = jour_to_x(fin_mois)
        lignes.append({
            'x1': x_fin, 'y1': 0.75, 'x2': x_fin, 'y2': 5.95,
            'stroke': 'red', 'stroke_width': 0.015,
            'vector_effect': 'non-scaling-stroke'
        })

        # Position du texte au milieu du mois
        x_milieu = (x_debut + x_fin) / 2
        lignes.append({
            'text': abreviations[mois],
            'x': round(x_milieu, 3),
            'y': 6.05,  # placÃ© sous la grille
            'font_size': 0.35,
            'anchor': 'middle',
            'stroke': 'none',
            'fill': 'black'
        })

        jour_cumule = fin_mois

    return lignes


def generer_lignes_horizontales():
    """GÃ©nÃ¨re les 6 lignes horizontales du graphique avec les labels"""
    
    hauteurs = [
        {'y_svg': 1.51429, 'stroke': 'black', 'minutes': '+10'},
        {'y_svg': 2.22857, 'stroke': 'black', 'minutes': '+5'},
        {'y_svg': 2.94286, 'stroke': 'red', 'minutes': '0'},    # Ligne 0 minutes
        {'y_svg': 3.65714, 'stroke': 'black', 'minutes': '-5'},
        {'y_svg': 4.37143, 'stroke': 'black', 'minutes': '-10'},
        {'y_svg': 5.08571, 'stroke': 'black', 'minutes': '-15'}
    ]
    
    lignes = []
    
    for hauteur in hauteurs:
        # Ligne horizontale
        lignes.append({
            'x1': -4.7, 'y1': hauteur['y_svg'], 'x2': 4.7, 'y2': hauteur['y_svg'],
            'stroke': hauteur['stroke'], 'stroke_width': 0.02, 'fill': 'none',
            'vector_effect': 'non-scaling-stroke'
        })
        
        # Label à gauche
        lignes.append({
            'text': hauteur['minutes'],
            'x': -5,
            'y': hauteur['y_svg'] + 0.1,  # Légèrement au-dessus de la ligne
            'font_size': 0.25,
            'anchor': 'middle',
            'stroke': 'none',
            'fill': 'black'
        })
        
        # Label à droite
        lignes.append({
            'text': hauteur['minutes'],
            'x': 5,
            'y': hauteur['y_svg'] + 0.1,
            'font_size': 0.25,
            'anchor': 'middle',
            'stroke': 'none',
            'fill': 'black'
        })
    
    return lignes


def generer_courbe_equation_temps():
    """GÃ©nÃ¨re les donnÃ©es pour la courbe de l'Ã©quation du temps"""
    
    points = []
    
    for N in range(1, 366):  # 1 Ã  365
        B = 2 * math.pi * (N - 81) / 365
        E = -9.87 * math.sin(2 * B) + 7.53 * math.cos(B) + 1.5 * math.sin(B)
        
        x = -4.7 + (N - 1) * 9.4 / 364
        y = 2.94286 - E * 0.14286
        
        points.append({'x': round(x, 4), 'y': round(y, 4)})
    
    if not points:
        return {'path_data': '', 'stroke': 'blue', 'stroke_width': 0.03, 'fill': 'none'}
    
    path_data = f"M {points[0]['x']} {points[0]['y']}"
    for point in points[1:]:
        path_data += f" L {point['x']} {point['y']}"
    
    return {
        'path_data': path_data,
        'stroke': 'purple',
        'stroke_width': 0.03,
        'fill': 'none',
        'vector_effect': 'non-scaling-stroke'
    }


def generer_graphique_equation_temps():
    """Fonction principale qui gÃ©nÃ¨re tous les Ã©lÃ©ments du graphique"""
    
    return {
        'cadre': generer_cadre_graphique(),
        'lignes_verticales': generer_lignes_verticales(),
        'lignes_horizontales': generer_lignes_horizontales(),
        'courbe': generer_courbe_equation_temps()
    }