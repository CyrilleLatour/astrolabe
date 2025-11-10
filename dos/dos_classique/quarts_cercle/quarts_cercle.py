from flask import Blueprint, render_template, request, session, redirect, url_for
import math
import time
import numpy as np
import svgwrite
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from .cercles.cercles import CerclesPrincipaux
from tympan.almucantarats.almucantarats import Almucantarats
from .azimuts.courbes_azimuts import CourbesAzimut
from .h_inegales.h_inegales import HeuresInegales
from tympan.crepuscules.crepuscules import extrapoler_crepuscules
from .h_inegales.points import (
    calculer_point_intersection_gauche,
    calculer_point_intersection_droit,
    calculer_point_intersection_horizon_cancer,
    calculer_point_intersection_horizon_cancer_droit,
    calculer_points_arc_cancer,
    calculer_points_arc_cancer_droit,
    calculer_points_arc_capricorne,
    calculer_points_arc_capricorne_droit,
    calculer_intersection_horizon_equateur,
    calculer_intersection_horizon_equateur_droit,
    calculer_points_equateur,
    calculer_points_equateur_droit
)

with open("debug_flask.txt", "w") as f:
    f.write(">>> Flask a bien exécuté views.py\n")
print("✅ FICHIER views.py EXÉCUTÉ")

tympan_bp = Blueprint('tympan', __name__, template_folder='templates')

def dms_to_decimal(dms_str):
    """Convertit une latitude DMS (format 'DD°MM′SS″') en degrés décimaux."""
    import re
    match = re.match(r"(\d+)°(\d+)′(\d+)″", dms_str)
    if not match:
        return None
    degrees, minutes, seconds = map(int, match.groups())
    return degrees + minutes / 60 + seconds / 3600

def degres_decimaux(degres, minutes, secondes):
    """Convertit les degrés, minutes, secondes en degrés décimaux."""
    return degres + minutes / 60 + secondes / 3600

def convert_to_dms(decimal_degrees):
    """Convertit les degrés décimaux en degrés, minutes, secondes."""
    deg = int(decimal_degrees)
    minutes_float = (decimal_degrees - deg) * 60
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60)
    return deg, minutes, seconds

def intersection_deux_cercles(c1, r1, c2, r2):
    """Calcule l'intersection entre deux cercles"""
    x0, y0 = c1
    x1, y1 = c2
    d = math.hypot(x1 - x0, y1 - y0)
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return []
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h_sq = r1**2 - a**2
    if h_sq < 0:
        return []
    h = math.sqrt(h_sq)
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d
    rx = -(y1 - y0) * (h / d)
    ry = (x1 - x0) * (h / d)
    p1 = (x2 + rx, y2 + ry)
    p2 = (x2 - rx, y2 - ry)
    return [p1, p2] if p1 != p2 else [p1]

def calculer_regressions_xy_azimut_270(df):
    """Calcule les régressions polynomiales pour x et y en fonction de Z"""
    if df.empty:
        return None, None
    
    Z = df[['Z']]
    x_vals = df['x']
    y_vals = df['y']
    
    for var_name, vals in [('x', x_vals), ('y', y_vals)]:
        for degree in range(1, min(len(df), 15)):
            try:
                model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
                model.fit(Z, vals)
                pred = model.predict(Z)
                r2 = r2_score(vals, pred)
                if abs(r2 - 1.0) < 1e-6 or r2 > 0.999999:
                    if var_name == 'x':
                        modele_x = model
                    else:
                        modele_y = model
                    break
            except Exception:
                continue
    
    return locals().get('modele_x'), locals().get('modele_y')

def calculer_intersections_azimut_270(latitude_deg, rayon_equateur, facteur):
    """Calcule les intersections entre le cercle d'azimut 270° et les almucantarats"""
    import pandas as pd
    
    S = rayon_equateur / 2
    L_rad = math.radians(latitude_deg)
    NP = 2 * S * math.tan(math.radians((90 - latitude_deg) / 2))
    NK = 2 * S / math.cos(L_rad)
    ycentre = NP - NK
    xcentre = 0
    rayon_270 = abs(2 * S / (math.cos(L_rad) * math.sin(math.radians(270))))
    
    intersections = []
    tol = 1e-9
    
    for Z in range(70, -1, -1):
        try:
            A_B = math.radians((180 - latitude_deg - Z) / 2)
            A_C = math.radians((Z - latitude_deg) / 2)
            B = 2 * S * math.tan(A_B)
            C = 2 * S * math.tan(A_C)
            R_alm = (B - C) / 2
            y_centre_alm = B - R_alm
            
            points = intersection_deux_cercles((xcentre, ycentre), rayon_270, (0, y_centre_alm), R_alm)
            for (x, y) in points:
                if x <= tol:
                    intersections.append({"Z": Z, "x": x, "y": y})
                    break
        except Exception:
            continue
    
    return pd.DataFrame(intersections)

def calculer_cercle_par_trois_points(p1, p2, p3):
    """Calcule le centre et le rayon d'un cercle passant par trois points"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    temp = x2**2 + y2**2
    bc = (x1**2 + y1**2 - temp) / 2
    cd = (temp - x3**2 - y3**2) / 2
    det = (x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2)
    
    if abs(det) < 1e-6:
        return None
    
    cx = (bc * (y2 - y3) - cd * (y1 - y2)) / det
    cy = ((x1 - x2) * cd - (x2 - x3) * bc) / det
    rayon = math.sqrt((cx - x1)**2 + (cy - y1)**2)
    
    return {'cx': cx, 'cy': cy, 'rayon': rayon}


@tympan_bp.route('/', methods=["GET", "POST"])
def tympan():
    # Initialiser toutes les variables
    variables = ['courbes_azimut', 'intersection_ligne_horizon', 'data_cercles', 'heures_inegales',
                'point_intersection', 'point_intersection_droit', 'point_horizon_cancer', 'point_horizon_cancer_droit',
                'points_arc', 'points_arc_droit', 'points_arc_cancer', 'points_arc_cancer_droit',
                'points_equateur', 'points_equateur_droit', 'intersection_horizon_equateur', 'intersection_horizon_equateur_droit',
                'cercle_azimut_solstice', 'cercle_azimut_solstice_gauche', 'courbe_azimut_personnalisee', 'courbe_grise_azimut_90_270']
    
    # Initialiser les cercles des heures inégales
    heures_inegales_vars = [f'cercle_heures_inegales{"_" + str(i) if i > 1 else ""}' for i in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]]
    
    # Initialiser toutes les variables à None
    locals().update({var: None for var in variables + heures_inegales_vars})
    
    cercles_crepuscules = []
    show_svg = False
    facteur = 1
    
    # Gestion des paramètres de session
    reset_param = request.args.get('reset', '0')
    if reset_param == '1':
        session['first_visit_tympan'] = True
    
    rayon_equateur = session.get('rayon_equateur')
    latitude = None
    latitude_dms = None
    show_chart = False
    first_visit = session.get('first_visit_tympan', True)
    
    if rayon_equateur is None:
        return redirect(url_for('index'))
    
    # Traitement de la latitude
    if request.method == 'POST':
        latitude = 0.0
        if 'latitudeDecimale' in request.form and request.form['latitudeDecimale']:
            try:
                latitude = float(request.form['latitudeDecimale'])
            except ValueError:
                pass
        if latitude == 0.0 and all(key in request.form and request.form[key] for key in ('degres', 'minutes', 'secondes')):
            try:
                degres = int(request.form['degres'])
                minutes = int(request.form['minutes'])
                secondes = float(request.form['secondes'])
                latitude = degres_decimaux(degres, minutes, secondes)
            except (ValueError, TypeError):
                pass
        if latitude is None:
            latitude = 0.0
        deg, minutes, secondes = convert_to_dms(latitude)
        latitude_dms = f"{deg}° {minutes}' {secondes}''"
        session['first_visit_tympan'] = False
        show_chart = True
    else:
        latitude_arg = request.args.get('latitude')
        if latitude_arg and reset_param != '1':
            try:
                latitude = float(latitude_arg)
                deg, minutes, secondes = convert_to_dms(latitude)
                latitude_dms = f"{deg}° {minutes}' {secondes}''"
                session['first_visit_tympan'] = False
                show_chart = True
            except (ValueError, TypeError):
                latitude = None
                show_chart = False
        else:
            if first_visit or reset_param == '1':
                latitude = None
                show_chart = False
            else:
                latitude = 48.8
                deg, minutes, secondes = convert_to_dms(latitude)
                latitude_dms = f"{deg}° {minutes}' {secondes}''"
                show_chart = True

    # Initialiser les points d'intersection
    points_intersection_azimut_180 = []
    points_intersection_azimut_270 = []

    if show_chart and rayon_equateur:
        # Calculer les cercles principaux
        cercles = CerclesPrincipaux(float(rayon_equateur))
        data_cercles = cercles.get_data()
        facteur = 240 / data_cercles["rayon_suppl"]

        horizon = None
        almucantarats = []

        if latitude is not None:
            almucantarats_obj = Almucantarats(float(rayon_equateur), latitude)
            data_almucantarats = almucantarats_obj.get_data()
            if data_almucantarats is None:
                horizon = None
                almucantarats = []
            else:
                horizon = data_almucantarats.get('horizon')
                almucantarats = data_almucantarats.get('almucantarats') or []

            # Calcul des points d'intersection pour les crépuscules
            import pandas as pd
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import PolynomialFeatures
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score

            # Points de régression (Z = 0 à 65 par pas de 5)
            resultats = []
            for Z in range(0, 66, 5):
                cercle = almucantarats_obj.calculer_almucantarat(Z)
                if cercle:
                    y_cartesien = cercle["cy"] - cercle["rayon"]
                    resultats.append({"Z": Z, "y_cartesien": y_cartesien})

            # Points d'intersection Z négatifs pour azimut 180°
            for Z_neg in [-6, -12, -18]:
                cercle_neg = almucantarats_obj.calculer_almucantarat(Z_neg)
                if cercle_neg:
                    y_calc = cercle_neg["cy"] - cercle_neg["rayon"]
                    points_intersection_azimut_180.append({
                        "x": 300, "y": 250 - y_calc * facteur, "Z": Z_neg, "type": "calcule"
                    })
                else:
                    if len(resultats) >= 3:
                        df_reel = pd.DataFrame(resultats)
                        X = df_reel[["Z"]]
                        y = df_reel["y_cartesien"]
                        
                        for degre in range(1, min(len(resultats), 15)):
                            try:
                                modele = make_pipeline(PolynomialFeatures(degre), LinearRegression())
                                modele.fit(X, y)
                                y_pred = modele.predict(X)
                                r2 = r2_score(y, y_pred)
                                if abs(r2 - 1.0) < 1e-10:
                                    y_ext = modele.predict(pd.DataFrame({"Z": [Z_neg]}))[0]
                                    points_intersection_azimut_180.append({
                                        "x": 300, "y": 250 - y_ext * facteur, "Z": Z_neg, "type": "extrapole"
                                    })
                                    break
                            except:
                                continue

            # Calcul du cercle d'azimut 270°
            S = rayon_equateur / 2
            L_rad = math.radians(latitude)
            NP = 2 * S * math.tan(math.radians((90 - latitude) / 2))
            NK = 2 * S / math.cos(L_rad)
            ycentre = NP - NK
            xcentre = 0
            rayon_270 = abs(2 * S / (math.cos(L_rad) * math.sin(math.radians(270))))
            
            cercle_azimut_270 = {
                'cx': 300, 'cy': 250 - (ycentre * facteur), 'rayon': rayon_270 * facteur,
                'style': {'stroke': 'gray', 'stroke_width': 2, 'fill': 'none'}
            }

            # Points d'intersection azimut 270°
            if cercle_azimut_270:
                df_intersections = calculer_intersections_azimut_270(latitude, rayon_equateur, facteur)
                if not df_intersections.empty:
                    modele_x, modele_y = calculer_regressions_xy_azimut_270(df_intersections)
                    if modele_x and modele_y:
                        for Z_neg in [-6, -12, -18]:
                            cercle_neg = almucantarats_obj.calculer_almucantarat(Z_neg)
                            if cercle_neg:
                                # Calculé directement
                                cx_azimut, cy_azimut, r_azimut = cercle_azimut_270['cx'], cercle_azimut_270['cy'], cercle_azimut_270['rayon']
                                cx_alm, cy_alm, r_alm = 300, 250 - (cercle_neg['cy'] * facteur), cercle_neg['rayon'] * facteur
                                points_intersect = intersection_deux_cercles((cx_azimut, cy_azimut), r_azimut, (cx_alm, cy_alm), r_alm)
                                for x_int, y_int in points_intersect:
                                    if x_int == min(p[0] for p in points_intersect):
                                        points_intersection_azimut_270.append({
                                            "x": x_int, "y": y_int, "Z": Z_neg, "type": "calcule"
                                        })
                                        break
                            else:
                                # Extrapolé
                                try:
                                    x_ext = modele_x.predict(pd.DataFrame({"Z": [Z_neg]}))[0]
                                    y_ext = modele_y.predict(pd.DataFrame({"Z": [Z_neg]}))[0]
                                    x_svg, y_svg = 300 + x_ext * facteur, 250 - y_ext * facteur
                                    points_intersection_azimut_270.append({
                                        "x": x_svg, "y": y_svg, "Z": Z_neg, "type": "extrapole"
                                    })
                                except Exception:
                                    continue

            # Points symétriques
            points_intersection_azimut_180_symetriques = []
            points_intersection_azimut_270_symetriques = []
            
            for points_list, sym_list in [(points_intersection_azimut_180, points_intersection_azimut_180_symetriques),
                                         (points_intersection_azimut_270, points_intersection_azimut_270_symetriques)]:
                for point in points_list:
                    if point["Z"] in [-6, -12, -18]:
                        x_sym = 2 * 300 - point["x"]
                        sym_list.append({
                            "x": x_sym, "y": point["y"], "Z": point["Z"], "type": point["type"]
                        })

            # Cercles de crépuscules
            for Z_crepuscule in [-6, -12, -18]:
                points_pour_cercle = []
                types_points = []
                
                # Rassembler les trois points
                for points_list in [points_intersection_azimut_180, points_intersection_azimut_270, points_intersection_azimut_270_symetriques]:
                    for point in points_list:
                        if point["Z"] == Z_crepuscule:
                            points_pour_cercle.append((point["x"], point["y"]))
                            types_points.append(point["type"])
                            break
                
                if len(points_pour_cercle) == 3:
                    cercle = calculer_cercle_par_trois_points(points_pour_cercle[0], points_pour_cercle[1], points_pour_cercle[2])
                    if cercle:
                        couleur_cercle = "gray" if all(t == "calcule" for t in types_points) else "red"
                        cercles_crepuscules.append({
                            'type': 'cercle', 'cx': cercle['cx'], 'cy': cercle['cy'], 'rayon': cercle['rayon'],
                            'hauteur': Z_crepuscule, 'style': {'stroke': couleur_cercle, 'stroke_width': 1.0, 'stroke_opacity': 1.0, 'fill': 'none'},
                            'invisible': False
                        })

            # HEURES INÉGALES
            if horizon:
                # Calculer tous les points nécessaires
                points_data = {
                    'intersection': calculer_point_intersection_gauche(horizon, data_cercles["rayon_capricorne"], facteur),
                    'intersection_droit': calculer_point_intersection_droit(horizon, data_cercles["rayon_capricorne"], facteur),
                    'horizon_cancer': calculer_point_intersection_horizon_cancer(horizon, data_cercles["rayon_cancer"], facteur),
                    'horizon_cancer_droit': calculer_point_intersection_horizon_cancer_droit(horizon, data_cercles["rayon_cancer"], facteur)
                }
                
                points_data.update({
                    'arc': calculer_points_arc_capricorne(points_data['intersection'], data_cercles["rayon_capricorne"], facteur),
                    'arc_droit': calculer_points_arc_capricorne_droit(points_data['intersection_droit'], data_cercles["rayon_capricorne"], facteur),
                    'arc_cancer': calculer_points_arc_cancer(points_data['horizon_cancer'], data_cercles["rayon_cancer"], facteur),
                    'arc_cancer_droit': calculer_points_arc_cancer_droit(points_data['horizon_cancer_droit'], data_cercles["rayon_cancer"], facteur)
                })
                
                # Points sur l'équateur
                cx, cy = 300, 250
                point_vertical_equateur = {'x': cx, 'y': cy + data_cercles["rayon_equateur"] * facteur}
                intersection_horizon_equateur = calculer_intersection_horizon_equateur(horizon, data_cercles["rayon_equateur"], facteur)
                intersection_horizon_equateur_droit = calculer_intersection_horizon_equateur_droit(horizon, data_cercles["rayon_equateur"], facteur)
                
                points_equateur = calculer_points_equateur(cx, cy, intersection_horizon_equateur, point_vertical_equateur, data_cercles["rayon_equateur"], facteur)
                points_equateur_droit = calculer_points_equateur_droit(cx, cy, intersection_horizon_equateur_droit, point_vertical_equateur, data_cercles["rayon_equateur"], facteur)
                
                # Calculer les cercles des heures inégales avec une boucle
                heures_inegales_obj = HeuresInegales(float(rayon_equateur), latitude)
                heures_config = [
                    # (nom_variable, index_arc, index_arc_cancer, index_equateur, côté)
                    ('cercle_heures_inegales', 0, 0, 1, 'gauche'),
                    ('cercle_heures_inegales_2', 1, 1, 2, 'gauche'),
                    ('cercle_heures_inegales_3', 2, 2, 3, 'gauche'),
                    ('cercle_heures_inegales_4', 3, 3, 4, 'gauche'),
                    ('cercle_heures_inegales_5', 4, 4, 5, 'gauche'),
                    ('cercle_heures_inegales_7', 4, 4, 5, 'droit'),
                    ('cercle_heures_inegales_8', 3, 3, 4, 'droit'),
                    ('cercle_heures_inegales_9', 2, 2, 3, 'droit'),
                    ('cercle_heures_inegales_10', 1, 1, 2, 'droit'),
                    ('cercle_heures_inegales_11', 0, 0, 1, 'droit')
                ]
                
                for var_name, idx_arc, idx_cancer, idx_eq, cote in heures_config:
                    try:
                        if cote == 'gauche':
                            if (len(points_data['arc']) > idx_arc and len(points_data['arc_cancer']) > idx_cancer and len(points_equateur) > idx_eq):
                                cercle = heures_inegales_obj.calculer_cercle_par_trois_points(
                                    points_data['arc'][idx_arc], points_data['arc_cancer'][idx_cancer], points_equateur[idx_eq]
                                )
                        else:
                            if (len(points_data['arc_droit']) > idx_arc and len(points_data['arc_cancer_droit']) > idx_cancer and len(points_equateur_droit) > idx_eq):
                                cercle = heures_inegales_obj.calculer_cercle_par_trois_points(
                                    points_data['arc_droit'][idx_arc], points_data['arc_cancer_droit'][idx_cancer], points_equateur_droit[idx_eq]
                                )
                        
                        if cercle:
                            locals()[var_name] = {'cx': cercle['cx'], 'cy': cercle['cy'], 'rayon': cercle['rayon']}
                    except:
                        locals()[var_name] = None

        # Courbes d'azimut
        courbes_azimut_obj = CourbesAzimut(float(rayon_equateur), latitude)
        courbes_azimut = courbes_azimut_obj.get_data()
        
        # Données des cercles - CORRECTION ICI
        for key in ['rayon_equateur', 'rayon_cancer', 'rayon_capricorne', 'rayon_suppl', 'rayon_ecliptique']:
            locals()[f'fixed_radius_{key.replace("rayon_", "")}'] = data_cercles[key]
        position_centre_ecliptique = data_cercles["position_centre_ecliptique"]

    else:
        # Réinitialiser toutes les variables si pas de données
        for var in ['fixed_radius_equateur', 'fixed_radius_cancer', 'fixed_radius_capricorne', 'fixed_radius_suppl', 
                   'fixed_radius_ecliptique', 'position_centre_ecliptique'] + variables + heures_inegales_vars:
            locals()[var] = None
        
        horizon = almucantarats = courbes_azimut = None
        facteur = 1
        cercles_crepuscules = []
        cercle_azimut_270 = None
        points_intersection_azimut_180_symetriques = []
        points_intersection_azimut_270_symetriques = []

    # Variables finales
    courbe_grise_azimut_90_270 = {'points': [], 'azimut': 'gris', 'color': 'gray', 'stroke_width': 2.5}
    if latitude is not None:
        alm = Almucantarats(rayon_equateur, latitude)
        cercle_horizon = alm.calculer_almucantarat(0)
    else:
        cercle_horizon = None
    
    if latitude is None and latitude_dms:
        latitude = dms_to_decimal(latitude_dms)
    
    points_crepusculaires = []

    # Calcul de la ligne du cercle suppl. vers l'horizon
    ligne_suppl_horizon = None

    if show_chart and horizon and data_cercles and latitude is not None:
        # Point de départ : haut du cercle supplémentaire
        cx_suppl, cy_suppl = 300, 250  # Centre du cercle suppl
        rayon_suppl = data_cercles["rayon_suppl"]
        point_haut_suppl = {
            'x': cx_suppl, 
            'y': cy_suppl - (rayon_suppl * facteur)  # Haut du cercle
        }
        
        # Point d'arrivée : intersection avec l'horizon
        if horizon.get('type') == 'ligne_horizontale':
            # Horizon horizontal : intersection simple avec la ligne y = 250
            point_bas_horizon = {
                'x': 300,
                'y': 250
            }
        else:
            # Horizon circulaire : intersection de la ligne verticale (x = 300) avec le cercle d'horizon
            cx_horizon = horizon.get('cx', 300)
            cy_horizon_svg = 250 - (horizon.get('cy', 0) * facteur)  # Conversion en coordonnées SVG
            rayon_horizon_svg = horizon.get('rayon', 0) * facteur
            
            # Équation du cercle : (x - cx_horizon)² + (y - cy_horizon_svg)² = rayon_horizon_svg²
            # Pour x = 300 : (300 - cx_horizon)² + (y - cy_horizon_svg)² = rayon_horizon_svg²
            dx = 300 - cx_horizon
            discriminant = rayon_horizon_svg**2 - dx**2
            
            if discriminant >= 0:
                # Deux points d'intersection possibles, on prend celui du bas
                dy = math.sqrt(discriminant)
                y1 = cy_horizon_svg + dy  # Point du bas
                y2 = cy_horizon_svg - dy  # Point du haut
                
                # On choisit le point le plus bas (plus proche du bord du tympan)
                point_bas_horizon = {
                    'x': 300,
                    'y': max(y1, y2)
                }
            else:
                # Pas d'intersection, on prend le point le plus proche
                point_bas_horizon = {
                    'x': 300,
                    'y': cy_horizon_svg
                }
        
        # Créer la ligne
        ligne_suppl_horizon = {
            'x1': point_haut_suppl['x'],
            'y1': point_haut_suppl['y'],
            'x2': point_bas_horizon['x'],
            'y2': point_bas_horizon['y'],
            'style': {
                'stroke': 'black',
                'stroke_width': 2,
                'fill': 'none'
            }
        }

    heures_inegales = None






    @tympan_bp.route('/test')
    def test():
        return "Test tympan fonctionne !"





    return render_template('tympan.html',
        rayon_equateur=rayon_equateur, 
        latitude=latitude, 
        latitude_dms=latitude_dms, 
        show_chart=show_chart,
        first_visit=first_visit, 
        reset=reset_param, 
        fixed_radius_equateur=locals().get('fixed_radius_equateur'),
        fixed_radius_cancer=locals().get('fixed_radius_cancer'), 
        fixed_radius_capricorne=locals().get('fixed_radius_capricorne'),
        fixed_radius_suppl=locals().get('fixed_radius_suppl'), 
        fixed_radius_ecliptique=locals().get('fixed_radius_ecliptique'),
        position_centre_ecliptique=locals().get('position_centre_ecliptique'), 
        horizon=horizon, 
        almucantarats=almucantarats,
        courbes_azimut=courbes_azimut, 
        heures_inegales=heures_inegales, 
        point_intersection=locals().get('point_intersection'),
        point_intersection_droit=locals().get('point_intersection_droit'), 
        point_horizon_cancer=locals().get('point_horizon_cancer'),
        point_horizon_cancer_droit=locals().get('point_horizon_cancer_droit'), 
        points_arc=locals().get('points_arc'),
        points_arc_droit=locals().get('points_arc_droit'), 
        points_arc_cancer=locals().get('points_arc_cancer'),
        points_arc_cancer_droit=locals().get('points_arc_cancer_droit'), 
        points_equateur=locals().get('points_equateur'),
        points_equateur_droit=locals().get('points_equateur_droit'), 
        intersection_horizon_equateur=locals().get('intersection_horizon_equateur'),
        cercle_heures_inegales=locals().get('cercle_heures_inegales'), 
        cercle_heures_inegales_2=locals().get('cercle_heures_inegales_2'),
        cercle_heures_inegales_3=locals().get('cercle_heures_inegales_3'), 
        cercle_heures_inegales_4=locals().get('cercle_heures_inegales_4'),
        cercle_heures_inegales_5=locals().get('cercle_heures_inegales_5'), 
        cercle_heures_inegales_7=locals().get('cercle_heures_inegales_7'),
        cercle_heures_inegales_8=locals().get('cercle_heures_inegales_8'), 
        cercle_heures_inegales_9=locals().get('cercle_heures_inegales_9'),
        cercle_heures_inegales_10=locals().get('cercle_heures_inegales_10'), 
        cercle_heures_inegales_11=locals().get('cercle_heures_inegales_11'),
        courbe_grise_azimut_90_270=courbe_grise_azimut_90_270, 
        points_intersection_azimut_180=points_intersection_azimut_180,
        points_intersection_azimut_270=points_intersection_azimut_270,
        points_intersection_azimut_180_symetriques=points_intersection_azimut_180_symetriques,
        points_intersection_azimut_270_symetriques=points_intersection_azimut_270_symetriques,
        facteur=facteur,
        show_svg=show_svg if 'show_svg' in locals() else False,
        points_crepusculaires=points_crepusculaires,
        cercles_crepuscules=cercles_crepuscules,
        cercle_azimut_270=cercle_azimut_270,
        ligne_suppl_horizon=ligne_suppl_horizon,
    )

@tympan_bp.route('/reset')
def reset():
    session.clear()
    session['first_visit'] = True
    session['first_visit_tympan'] = True
    timestamp = int(time.time())
    return redirect(url_for('index', reset=1, ts=timestamp))import os
import math

# Code SVG original des arcs de cercle intérieurs (repris exactement de dos.html)
arcs_cercle_svg = """        <!-- arcs de cercle intérieurs -->
        <path d="M -0.7125 0 A 0.7125 0.7125 0 0 1 0 -0.7125" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -1.425 0 A 1.425 1.425 0 0 1 0 -1.425" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -2.1375 0 A 2.1375 2.1375 0 0 1 0 -2.1375" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -2.85 0 A 2.85 2.85 0 0 1 0 -2.85" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -3.5625 0 A 3.5625 3.5625 0 0 1 0 -3.5625" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -4.275 0 A 4.275 4.275 0 0 1 0 -4.275" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -4.9875 0 A 4.9875 4.9875 0 0 1 0 -4.9875" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -5.7 0 A 5.7 5.7 0 0 1 0 -5.7" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -6.4125 0 A 6.4125 6.4125 0 0 1 0 -6.4125" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -7.125 0 A 7.125 7.125 0 0 1 0 -7.125" stroke="black" stroke-width="0.05" fill="none" />
        <path d="M -7.8375 0 A 7.8375 7.8375 0 0 1 0 -7.8375" stroke="black" stroke-width="0.05" fill="none" />"""

def generer_quarts_cercle_direct():
    """Code direct pour générer les quarts de cercle avec points de division"""
    
    # Rayons des 11 quarts de cercle (repris exactement de dos.html)
    rayons = [0.7125, 1.425, 2.1375, 2.85, 3.5625, 4.275, 4.9875, 5.7, 6.4125, 7.125, 7.8375]
    
    # Génération des arcs de cercle
    arcs = []
    for rayon in rayons:
        arcs.append({
            'rayon': rayon,
            'stroke': 'black',
            'stroke_width': 0.05,
            'fill': 'none'
        })
    
    # Génération des points de division
    points = []
    for i, rayon in enumerate(rayons, 1):
        if i > 1:  # Pas de points pour le 1er quart de cercle
            nb_points = i - 1
            for j in range(1, nb_points + 1):
                # Angle pour diviser le quart de cercle en i parties égales
                angle = (math.pi / 2) * j / i  # angle en radians
                
                # Coordonnées du point sur le cercle (coordonnées cartésiennes)
                x = -rayon * math.cos(angle)
                y = -rayon * math.sin(angle)
                
                points.append({
                    'x': round(x, 4),
                    'y': round(y, 4),
                    'r': 0.08,
                    'fill': 'black'
                })
    
    # Génération des 11 points sur le cercle de rayon 8.55 (division en 12 parties égales)
    points_cercle_855 = []
    rayon_855 = 8.55
    for j in range(1, 12):  # 11 points pour diviser en 12 parties
        # Angle pour diviser le quart de cercle en 12 parties égales
        angle = (math.pi / 2) * j / 12  # angle en radians
        
        # Coordonnées du point sur le cercle (coordonnées cartésiennes)
        x = -rayon_855 * math.cos(angle)
        y = -rayon_855 * math.sin(angle)
        
        points_cercle_855.append({
            'x': round(x, 4),
            'y': round(y, 4),
            'r': 0.08,
            'fill': 'black'
        })
    
    return {
        'arcs_svg': arcs_cercle_svg,
        'arcs': arcs,
        'points': points,
        'points_cercle_855': points_cercle_855
    }

def main():
    """Fonction principale pour test"""
    print("Code SVG original des arcs de cercle :")
    print("=" * 50)
    print(arcs_cercle_svg)
    print("=" * 50)
    
    print("\nTest de génération des quarts de cercle...")
    data = generer_quarts_cercle_direct()
    print(f"Nombre d'arcs générés : {len(data['arcs'])}")
    print(f"Nombre de points de division générés : {len(data['points'])}")
    print(f"Nombre de points sur cercle 8.55 générés : {len(data['points_cercle_855'])}")
    print("Code SVG original conservé dans 'arcs_svg'")

if __name__ == "__main__":
    main()