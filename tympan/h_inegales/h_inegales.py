import math

class HeuresInegales:
    def __init__(self, rayon_equateur, latitude):
        """
        Initialise le calculateur pour les heures inégales.
        
        Args:
            rayon_equateur: Rayon de l'équateur en unités de mesure (S)
            latitude: Latitude en degrés
        """
        self.rayon_equateur = rayon_equateur
        self.latitude = latitude
        
    def calculer_cercle_par_trois_points(self, point1, point2, point3):
        """
        Calcule le centre et le rayon d'un cercle passant par trois points.
        
        Args:
            point1, point2, point3: Dictionnaires avec les clés 'x' et 'y'
        
        Returns:
            Dictionnaire avec les clés 'cx', 'cy' pour le centre et 'rayon'
        """
        # 1. Calculer le milieu entre les points 1 et 2
        milieu1_2 = {
            'x': (point1['x'] + point2['x']) / 2,
            'y': (point1['y'] + point2['y']) / 2
        }
        
        # 2. Calculer la pente de la droite entre les points 1 et 2
        if point2['x'] - point1['x'] != 0:  # Éviter division par zéro
            pente1_2 = (point2['y'] - point1['y']) / (point2['x'] - point1['x'])
            # Pente de la perpendiculaire
            if pente1_2 != 0:
                pente_perp1_2 = -1 / pente1_2
            else:
                pente_perp1_2 = float('inf')  # Pente infinie (droite verticale)
        else:
            pente1_2 = float('inf')  # Pente infinie (droite verticale)
            pente_perp1_2 = 0  # Droite horizontale

        # 3. Calculer le milieu entre les points 2 et 3
        milieu2_3 = {
            'x': (point2['x'] + point3['x']) / 2,
            'y': (point2['y'] + point3['y']) / 2
        }
        
        # 4. Calculer la pente de la droite entre les points 2 et 3
        if point3['x'] - point2['x'] != 0:  # Éviter division par zéro
            pente2_3 = (point3['y'] - point2['y']) / (point3['x'] - point2['x'])
            # Pente de la perpendiculaire
            if pente2_3 != 0:
                pente_perp2_3 = -1 / pente2_3
            else:
                pente_perp2_3 = float('inf')  # Pente infinie (droite verticale)
        else:
            pente2_3 = float('inf')  # Pente infinie (droite verticale)
            pente_perp2_3 = 0  # Droite horizontale
            
        # 5. Calculer l'intersection des deux droites perpendiculaires
        # Pour une droite avec pente m passant par le point (x0, y0), l'équation est:
        # y - y0 = m(x - x0)  =>  y = m*x - m*x0 + y0  =>  y = m*x + b où b = -m*x0 + y0
        
        # Cas spécial si une des pentes est infinie
        if pente_perp1_2 == float('inf'):
            # La première droite est verticale, x = milieu1_2['x']
            cx = milieu1_2['x']
            # Utiliser la deuxième droite pour trouver y
            b2_3 = milieu2_3['y'] - pente_perp2_3 * milieu2_3['x']
            cy = pente_perp2_3 * cx + b2_3
        elif pente_perp2_3 == float('inf'):
            # La deuxième droite est verticale, x = milieu2_3['x']
            cx = milieu2_3['x']
            # Utiliser la première droite pour trouver y
            b1_2 = milieu1_2['y'] - pente_perp1_2 * milieu1_2['x']
            cy = pente_perp1_2 * cx + b1_2
        else:
            # Équations des deux droites perpendiculaires:
            # y = pente_perp1_2 * x + b1_2
            # y = pente_perp2_3 * x + b2_3
            b1_2 = milieu1_2['y'] - pente_perp1_2 * milieu1_2['x']
            b2_3 = milieu2_3['y'] - pente_perp2_3 * milieu2_3['x']
            
            # À l'intersection: pente_perp1_2 * x + b1_2 = pente_perp2_3 * x + b2_3
            # => (pente_perp1_2 - pente_perp2_3) * x = b2_3 - b1_2
            if pente_perp1_2 == pente_perp2_3:
                # Les droites sont parallèles, pas de solution unique
                # Retour d'une valeur par défaut ou gestion d'erreur
                return {'cx': 0, 'cy': 0, 'rayon': 0}
            
            cx = (b2_3 - b1_2) / (pente_perp1_2 - pente_perp2_3)
            cy = pente_perp1_2 * cx + b1_2
        
        # 6. Calculer le rayon (distance du centre à n'importe lequel des 3 points)
        rayon = math.sqrt((cx - point1['x'])**2 + (cy - point1['y'])**2)
        
        return {
            'cx': cx,
            'cy': cy,
            'rayon': rayon
        }

    def get_data(self):
        """
        Retourne les données pour dessiner les heures inégales.
        
        Returns:
            Données des cercles d'heures inégales
        """
        # Cette fonction est appelée par la vue mais ne contient pas encore
        # la logique complète pour générer toutes les heures inégales.
        # Dans la version actuelle, nous retournons simplement une structure vide
        # qui sera remplie dans views.py
        return {
            'heures_inegales': []
        }