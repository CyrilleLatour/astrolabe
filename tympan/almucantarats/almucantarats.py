import math

class Almucantarats:
    # Facteurs de correction pour l'échelle
    f_rayon_custom = 0.0368633
    f_position_custom = 0.0381462
    
    # ✅ SEUIL : au-delà de ce rayon, on considère que c'est une ligne horizontale
    SEUIL_RAYON_LIGNE = 1000

    def __init__(self, rayon_equateur, latitude):
        self.rayon_equateur = float(rayon_equateur)
        self.latitude = float(latitude)
        self.facteur_echelle = self.rayon_equateur / 6
        self.latitude_secondes = abs(self.latitude * 3600)

    def calculer_intersection_azimut_180(self, hauteur, latitude_deg, rayon_equateur=6):
        """
        Calcule l'intersection inférieure entre la droite d'azimut 180° (x=0)
        et un cercle d'almucantarat à une certaine hauteur.
        Retourne None si le calcul est instable.
        """
        try:
            phi = math.radians(latitude_deg)
            theta = 90 - hauteur

            # Sécurité : si les angles deviennent trop proches de 90°, arrêt
            angle_B = (90 - latitude_deg + theta) / 2
            angle_C = (90 - latitude_deg - theta) / 2

            if abs(angle_B) >= 89.0 or abs(angle_C) >= 89.0:
                return None  # basculement nécessaire vers extrapolation

            # Calculs standards des cercles
            B = 6 * math.tan(math.radians(angle_B))
            C = 6 * math.tan(math.radians(angle_C))
            r = abs(B - C) / 2  # ✅ CORRECTION : valeur absolue
            y_centre = B - r

            # Intersection inférieure : y_centre - rayon
            y_intersection = y_centre - r

            # Conversion à l'échelle du rayon équateur
            facteur = rayon_equateur / 6
            y_intersection *= facteur

            # x = 0 car azimut 180° est une droite verticale
            return (0.0, y_intersection)

        except Exception as e:
            return None  # Sécurité anti-crash

    def intersection_almucantarat_inferieure_azimut_180(self, hauteur):
        """
        Calcule le point d'intersection INFÉRIEURE entre la droite d'azimut 180°
        (verticale, x=0) et le cercle d'almucantarat donné (hauteur en degrés).
        
        Retourne les coordonnées (x=0, y) en unités de l'astrolabe.
        Utilise l'extrapolation si le calcul direct n'est pas possible.
        """
        # Calculer d'abord l'almucantarat pour récupérer ses paramètres
        almucantarat = self.calculer_almucantarat(hauteur)
        
        # Si l'almucantarat n'existe pas (retourne None), pas d'intersection possible
        if almucantarat is None:
            print(f"DEBUG ALMU - Almucantarat {hauteur}° n'existe pas à latitude {self.latitude}°")
            return None
        
        # Si c'est une ligne horizontale, pas d'intersection classique
        if almucantarat.get('type') == 'ligne_horizontale':
            return None
        
        print(f"DEBUG ALMU - Almucantarat {hauteur}° :")
        print(f"  - cy = {almucantarat['cy']}")
        print(f"  - rayon = {almucantarat['rayon']}")
        
        # L'intersection inférieure est à y = cy + rayon (point le plus bas du cercle)
        # Note: dans le système de coordonnées de l'astrolabe, Y positif est vers le bas
        y_intersection = almucantarat['cy'] + almucantarat['rayon']
        
        print(f"ALMU 6° — Calcul du point : y = cy + rayon = {almucantarat['cy']} + {almucantarat['rayon']}")
        print(f"ALMU 6° — Point renvoyé : (0.0, {y_intersection})")
        
        return (0.0, y_intersection)

    def get_almucantarats_basses_latitudes(self):
        donnees_basses_latitudes = {
            0: {
                'horizon': {
                    'type': 'ligne_horizontale',
                    'y_offset': 0,
                    'hauteur': 0,
                    'style': {
                        'stroke': 'black',
                        'stroke_width': 1.5,
                        'stroke_opacity': 1.0
                    }
                },

                'almucantarats': [
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 68.84,
                        'rayon': 68.58,
                        'hauteur': 5,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 34.55,
                        'rayon': 34.03,
                        'hauteur': 10,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 23.18,
                        'rayon': 22.39,
                        'hauteur': 15,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 17.54,
                        'rayon': 16.48,
                        'hauteur': 20,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 14.2,
                        'rayon': 12.87,
                        'hauteur': 25,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 12.0,
                        'rayon': 10.39,
                        'hauteur': 30,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 10.46,
                        'rayon': 8.57,
                        'hauteur': 35,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 9.33,
                        'rayon': 7.15,
                        'hauteur': 40,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 8.49,
                        'rayon': 6.0,
                        'hauteur': 45,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 7.84,
                        'rayon': 5.04,
                        'hauteur': 50,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 7.33,
                        'rayon': 4.23,
                        'hauteur': 55,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 6.93,
                        'rayon': 3.46,
                        'hauteur': 60,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 6.62,
                        'rayon': 2.8,
                        'hauteur': 65,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 6.39,
                        'rayon': 2.18,
                        'hauteur': 70,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        }
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 6.21,
                        'rayon': 1.61,
                        'hauteur': 75,
                        'style': {
                            'stroke': 'gray',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        },
                        'invisible': True
                    },
                    {
                        'type': 'cercle',
                        'cx': 0,
                        'cy': 6.09,
                        'rayon': 1.06,
                        'hauteur': 80,
                        'style': {
                            'stroke': 'black',
                            'stroke_width': 1.0,
                            'stroke_opacity': 1.0,
                            'fill': 'none'
                        },
                        'invisible': True
                    }
                ]
            }
        }
        return donnees_basses_latitudes

    def get_data(self):
        # Utiliser les données hardcodées uniquement pour latitude = 0° exactement
        # Car l'horizon (hauteur 0°) donne angle_B = 90° → tangente infinie
        if self.latitude_secondes == 0:
            data = self.get_almucantarats_basses_latitudes()[0]
            # Appliquer le facteur d'échelle aux coordonnées hardcodées
            # Ces coordonnées sont pour rayon_equateur = 6
            # Il faut les ajuster au rayon_equateur actuel
            facteur_echelle = self.rayon_equateur / 6
            
            # Ajuster l'horizon si c'est une ligne
            if data['horizon'].get('type') == 'ligne_horizontale':
                data['horizon']['y_offset'] *= facteur_echelle
            
            # Ajuster tous les almucantarats
            for alm in data['almucantarats']:
                if alm.get('type') == 'cercle':
                    alm['cy'] *= facteur_echelle
                    alm['rayon'] *= facteur_echelle
                elif alm.get('type') == 'ligne_horizontale':
                    alm['y_offset'] *= facteur_echelle
            
            return data

        horizon = self.calculer_almucantarat(0)
        almucantarats = []

        # Cercles crépusculaires (-18°, -12°, -6°) sont gérés dans views.py
        # Ne pas les générer ici pour éviter les doublons

        # Cercles normaux de 5° à 80°
        for hauteur in list(range(5, 85, 5)):
            alm = self.calculer_almucantarat(hauteur)
            if alm is not None:  # Seulement si le calcul est possible
                almucantarats.append(alm)

        return {
            'horizon': horizon,
            'almucantarats': almucantarats
        }

    def calculer_almucantarat(self, hauteur):
        # CAS SPÉCIAL : Latitude exactement 0° et horizon
        # L'horizon à l'équateur est une ligne horizontale (rayon infini)
        if self.latitude == 0 and hauteur == 0:
            if hauteur == 0:
                stroke = "black"
                stroke_width = 1.5
            else:
                stroke = "gray"
                stroke_width = 1.0
            
            return {
                'type': 'ligne_horizontale',
                'y_offset': 0,
                'hauteur': 0,
                'style': {
                    'stroke': stroke,
                    'stroke_width': stroke_width,
                    'stroke_opacity': 1.0,
                    'fill': 'none'
                }
            }
        
        elevation = 90.0 - hauteur

        # Vérifier si le cercle peut exister à cette latitude
        # Un almucantarat à hauteur h ne peut exister que si |latitude - h| < 90°
        if hauteur < 0:  # Pour les cercles crépusculaires
            # ✅ CORRECTION : Détecter la zone critique où latitude ≈ |hauteur|
            # Dans cette zone, le rayon devient gigantesque
            diff = abs(abs(self.latitude) - abs(hauteur))
            
            # Si la différence est très petite (< 0.05°), on est dans la zone de transition
            # où le cercle a un rayon gigantesque
            if diff < 0.05:  # 0.05° = 3 arcminutes = 180 arcsec
                print(f"⚠️  Zone critique détectée : latitude {self.latitude}° ≈ |hauteur| {abs(hauteur)}° (diff={diff:.4f}°)")
                # On va quand même calculer, mais on vérifiera le rayon après
            
            # Si latitude < |hauteur|, le cercle n'existe pas du tout
            if abs(self.latitude) < abs(hauteur):
                print(f"DEBUG ALMU - Almucantarat {hauteur}° impossible à latitude {self.latitude}°")
                return None

        if hauteur == 0:
            stroke = "black"
            stroke_width = 1.5
        elif hauteur == 70:
            stroke = "black"
            stroke_width = 1.0
        elif hauteur % 10 == 0:
            stroke = "black"
            stroke_width = 1.0
        else:
            stroke = "gray"
            stroke_width = 1.0

        angle_B = (90 - self.latitude + elevation) / 2
        angle_C = (90 - self.latitude - elevation) / 2

        # Vérification préliminaire des angles
        if abs(angle_B) >= 90 or abs(angle_C) >= 90:
            print(f"DEBUG ALMU - Angles hors domaine pour hauteur {hauteur}° à latitude {self.latitude}°")
            return None

        try:
            # Cas normal
            B = 6 * math.tan(math.radians(angle_B))
            C = 6 * math.tan(math.radians(angle_C))
            
            # ✅ CORRECTION : Utiliser la valeur absolue pour le rayon
            rayon = abs(B - C) / 2
            Y = B - rayon
            
            # Appliquer le facteur d'échelle
            rayon_scaled = rayon * self.facteur_echelle
            Y_scaled = Y * self.facteur_echelle
            
            # ✅ NOUVELLE VÉRIFICATION : Si le rayon est gigantesque (> seuil)
            # C'est qu'on est dans la zone de transition juste après latitude = |hauteur|
            # On doit convertir en ligne horizontale
            if rayon_scaled > self.SEUIL_RAYON_LIGNE:
                y_position = Y_scaled - rayon_scaled  # Position y de la ligne
                print(f"🔶 Almucantarat {hauteur}° converti en LIGNE HORIZONTALE (rayon={rayon_scaled:.1f} > {self.SEUIL_RAYON_LIGNE})")
                return {
                    'type': 'ligne_horizontale',
                    'y_offset': y_position,
                    'hauteur': hauteur,
                    'style': {
                        'stroke': stroke,
                        'stroke_width': stroke_width,
                        'stroke_opacity': 1.0,
                        'fill': 'none'
                    }
                }
            
            style = {
                'stroke': stroke,
                'stroke_width': stroke_width,
                'stroke_opacity': 1.0,
                'fill': 'none'
            }
            
            # Cas normal (cercle)
            return {
                'type': 'cercle',
                'cx': 0,
                'cy': Y_scaled,
                'rayon': rayon_scaled,
                'hauteur': hauteur,
                'style': style
            }
            
        except Exception as e:
            print(f"DEBUG ALMU - Erreur de calcul pour hauteur {hauteur}° à latitude {self.latitude}°: {e}")
            return None