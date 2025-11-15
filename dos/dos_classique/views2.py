# dos/dos_classique/views2.py
from flask import Blueprint, render_template, current_app
import os
import math
from jinja2 import ChoiceLoader, FileSystemLoader

# ===== Blueprint =====
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dos_bp = Blueprint('dos', __name__, template_folder=template_path)

# ===== Hook loader =====
def _ensure_dos_template_paths():
    if getattr(current_app, "_dos_paths_added", False):
        return

    dos_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    candidate_folders = [
        os.path.join(dos_root, "templates"),
        os.path.join(dos_root, "dos_classique", "templates"),
        os.path.join(dos_root, "dos_plus", "templates"),
        os.path.join(dos_root, "anneau_ext", "templates"),
    ]

    loaders = [current_app.jinja_loader]
    for folder in candidate_folders:
        if os.path.isdir(folder):
            loaders.append(FileSystemLoader(folder))

    current_app.jinja_loader = ChoiceLoader(loaders)
    current_app._dos_paths_added = True

@dos_bp.before_app_request
def _setup_loader_once():
    _ensure_dos_template_paths()


# ====== Générateurs (inchangés) ======
def generer_diagonales_correction_direct():
    def generer_diagonales_gauche_25():
        x1, x2 = -6.68216, -6.4125
        angle_depart, angle_arrivee = 225, 180
        lignes = []
        for i in range(25):
            angle = angle_depart + (angle_arrivee - angle_depart) * i / 24
            angle_rad = angle * math.pi / 180
            y1, y2 = x1 * math.tan(angle_rad), x2 * math.tan(angle_rad)
            lignes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'stroke': 'black', 'stroke_width': 0.03})
        return lignes

    def generer_diagonales_gauche_13():
        x1, x2 = -6.4125, -6.1428
        angle_depart, angle_arrivee = 225, 180
        lignes = []
        for i in range(13):
            angle = angle_depart + (angle_arrivee - angle_depart) * i / 12
            angle_rad = angle * math.pi / 180
            y1, y2 = x1 * math.tan(angle_rad), x2 * math.tan(angle_rad)
            lignes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_diagonales_gauche_5():
        x1, x2 = -6.1428, -5.8731
        angle_depart, angle_arrivee = 225, 180
        lignes = []
        for i in range(5):
            angle = angle_depart + (angle_arrivee - angle_depart) * i / 4
            angle_rad = angle * math.pi / 180
            y1, y2 = x1 * math.tan(angle_rad), x2 * math.tan(angle_rad)
            lignes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_diagonales_bas(y_bas, y_haut, total):
        angle_depart, angle_fin = 225, 315
        pas = (angle_fin - angle_depart) / (total - 1)
        lignes = []
        for i in range(total):
            angle_deg = angle_depart + i * pas
            angle_rad = angle_deg * math.pi / 180
            tan_theta = math.tan(angle_rad)
            if abs(tan_theta) < 1e-6:
                continue
            x1, y1 = y_bas / tan_theta, y_bas
            x2, y2 = y_haut / tan_theta, y_haut
            lignes.append({'x1': round(x1, 5), 'y1': round(y1, 5), 'x2': round(x2, 5), 'y2': round(y2, 5), 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_diagonales_droite(x1, x2, nb):
        angle_depart, angle_arrivee = 315, 360
        diviseur = nb - 1
        stroke_width = 0.03 if nb == 25 else 0.02
        lignes = []
        for i in range(nb):
            angle = angle_depart + (angle_arrivee - angle_depart) * i / diviseur
            angle_rad = angle * math.pi / 180
            y1, y2 = x1 * math.tan(angle_rad), x2 * math.tan(angle_rad)
            lignes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'stroke': 'black', 'stroke_width': stroke_width})
        return lignes

    return {
        'diagonales_gauche_25': generer_diagonales_gauche_25(),
        'diagonales_gauche_13': generer_diagonales_gauche_13(),
        'diagonales_gauche_5': generer_diagonales_gauche_5(),
        'diagonales_bas_49': generer_diagonales_bas(-6.6822, -6.4125, 49),
        'diagonales_bas_25': generer_diagonales_bas(-6.4125, -6.1428, 25),
        'diagonales_bas_9': generer_diagonales_bas(-6.1428, -5.8731, 9),
        'diagonales_droite_25': generer_diagonales_droite(6.68216, 6.4125, 25),
        'diagonales_droite_13': generer_diagonales_droite(6.4125, 6.1428, 13),
        'diagonales_droite_5': generer_diagonales_droite(6.1428, 5.8731, 5)
    }

def generer_quadrilateres_correction_direct():
    def generer_quadrilateres_gauche():
        coordonnees = [
            "-6.4125,-6.4125 -6.1428,-6.1428 -6.1428,-5.3871 -6.4125,-5.6236",
            "-6.4125,-4.9205 -6.1428,-4.7135 -6.1428,-4.1045 -6.4125,-4.2847",
            "-6.4125,-3.7023 -6.1428,-3.5465 -6.1428,-3.0293 -6.4125,-3.1623",
            "-6.4125,-2.6561 -6.1428,-2.5444 -6.1428,-2.0852 -6.4125,-2.1768",
            "-6.4125,-1.7182 -6.1428,-1.646 -6.1428,-1.2219 -6.4125,-1.2755",
            "-6.4125,-0.8442 -6.1428,-0.8087 -6.1428,-0.4026 -6.4125,-0.4203"
        ]
        return [{'points': points, 'fill': 'black', 'stroke': 'none'} for points in coordonnees]

    def generer_quadrilateres_bas():
        coordonnees = [
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
        return [{'points': points, 'fill': 'black', 'stroke': 'none'} for points in coordonnees]

    def generer_quadrilateres_droite():
        coordonnees = [
            "6.1428,-5.3871 6.4125,-5.6236 6.4125,-4.9205 6.1428,-4.7135",
            "6.1428,-4.1045 6.4125,-4.2847 6.4125,-3.7023 6.1428,-3.5465",
            "6.1428,-3.0293 6.4125,-3.1623 6.4125,-2.6561 6.1428,-2.5444",
            "6.1428,-2.0852 6.4125,-2.1768 6.4125,-1.7182 6.1428,-1.646",
            "6.1428,-1.2219 6.4125,-1.2755 6.4125,-0.8442 6.1428,-0.8087",
            "6.1428,-0.4026 6.4125,-0.4203 6.4125,0.0 6.1428,0.0"
        ]
        return [{'points': points, 'fill': 'black', 'stroke': 'none'} for points in coordonnees]

    return {
        'quadrilateres_gauche': generer_quadrilateres_gauche(),
        'quadrilateres_bas': generer_quadrilateres_bas(),
        'quadrilateres_droite': generer_quadrilateres_droite()
    }

def generer_subdivisions_annee_direct():
    def generer_subdivisions_jours():
        angle_jour = 360 / 365
        lignes = []
        for i in range(365):
            angle_deg = i * angle_jour
            angle_rad = (angle_deg - 90) * math.pi / 180
            x1, y1 = 10.62 * math.cos(angle_rad), 10.62 * math.sin(angle_rad)
            x2, y2 = 10.42 * math.cos(angle_rad), 10.42 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_subdivisions_mois():
        angle_jour_mois = 360 / 365
        jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        jour_cumule = 0
        lignes = []
        for mois in range(12):
            jour_cumule += jours_mois[mois]
            angle_deg_mois = jour_cumule * angle_jour_mois
            angle_rad_mois = (angle_deg_mois - 90) * math.pi / 180
            x1_mois, y1_mois = 10.55 * math.cos(angle_rad_mois), 10.55 * math.sin(angle_rad_mois)
            x2_mois, y2_mois = 9.45 * math.cos(angle_rad_mois), 9.45 * math.sin(angle_rad_mois)
            lignes.append({'x1': round(x1_mois, 3), 'y1': round(y1_mois, 3), 'x2': round(x2_mois, 3), 'y2': round(y2_mois, 3), 'stroke': 'red', 'stroke_width': 0.05})
        return lignes

    def generer_subdivisions_5_jours():
        angle_jour = 360 / 365
        jours_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        subdivisions_par_mois = [6, 5, 6, 5, 6, 5, 6, 6, 5, 6, 5, 6]
        jour_cumule = 0
        lignes = []
        for mois in range(12):
            debut_mois = jour_cumule
            for subdiv in range(1, subdivisions_par_mois[mois] + 1):
                jour_subdivision = debut_mois + (subdiv * 5)
                angle_deg = jour_subdivision * angle_jour
                angle_rad = (angle_deg - 90) * math.pi / 180
                x1, y1 = 10 * math.cos(angle_rad), 10 * math.sin(angle_rad)
                x2, y2 = 10.55 * math.cos(angle_rad), 10.55 * math.sin(angle_rad)
                lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.02})
            jour_cumule += jours_mois[mois]
        return lignes

    return {
        'subdivisions_jours': generer_subdivisions_jours(),
        'subdivisions_mois': generer_subdivisions_mois(),
        'subdivisions_5_jours': generer_subdivisions_5_jours()
    }

def generer_subdivisions_internes_direct():
    def generer_subdivisions_internes_gauche_1_degre():
        lignes = []
        pas_angle = 90 / 72
        angle_debut = 90 + pas_angle
        nb_subdivisions = int((180 - angle_debut) / pas_angle) + 1
        for i in range(nb_subdivisions):
            angle_deg = angle_debut + i * pas_angle
            if angle_deg >= 180:
                break
            angle_rad = angle_deg * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 8.8 * math.cos(angle_rad), 8.8 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_subdivisions_internes_gauche_15_degres():
        angles_speciaux = [105, 120, 135, 150, 165]
        lignes = []
        for angle in angles_speciaux:
            angle_rad = angle * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 9.45 * math.cos(angle_rad), 9.45 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.05})
        return lignes

    def generer_subdivisions_internes_gauche_5_degres():
        lignes = []
        pas_angle = 90 / 24
        angle_fin = 180 - pas_angle
        nb_subdivisions = int((angle_fin - 90) / pas_angle) + 1
        for i in range(nb_subdivisions):
            angle_deg = angle_fin - i * pas_angle
            if angle_deg <= 90:
                break
            angle_rad = angle_deg * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 9.05 * math.cos(angle_rad), 9.05 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.025})
        return lignes

    def generer_subdivisions_internes_gauche_10_degres():
        return []

    def generer_subdivisions_internes_droite_1_degre():
        lignes = []
        for angle in range(1, 90):
            angle_rad = angle * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 8.8 * math.cos(angle_rad), 8.8 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.02})
        return lignes

    def generer_subdivisions_internes_droite_5_degres():
        lignes = []
        for angle in range(5, 90, 5):
            angle_rad = angle * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 9.05 * math.cos(angle_rad), 9.05 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.025})
        return lignes

    def generer_subdivisions_internes_droite_10_degres():
        lignes = []
        for angle in range(10, 90, 10):
            angle_rad = angle * math.pi / 180
            x1, y1 = 8.55 * math.cos(angle_rad), 8.55 * math.sin(angle_rad)
            x2, y2 = 9.45 * math.cos(angle_rad), 9.45 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.035})
        return lignes

    def generer_subdivisions_internes_droite_15_degres():
        angles_speciaux = [15, 30, 45, 60, 75]
        lignes = []
        for angle in angles_speciaux:
            angle_rad = angle * math.pi / 180
            x1, y1 = 8.25 * math.cos(angle_rad), 8.25 * math.sin(angle_rad)
            x2, y2 = 9.5 * math.cos(angle_rad), 9.5 * math.sin(angle_rad)
            lignes.append({'x1': round(x1, 3), 'y1': round(y1, 3), 'x2': round(x2, 3), 'y2': round(y2, 3), 'stroke': 'black', 'stroke_width': 0.05})
        return lignes

    return {
        'subdivisions_gauche_1_degre': generer_subdivisions_internes_gauche_1_degre(),
        'subdivisions_gauche_15_degres': generer_subdivisions_internes_gauche_15_degres(),
        'subdivisions_gauche_5_degres': generer_subdivisions_internes_gauche_5_degres(),
        'subdivisions_gauche_10_degres': generer_subdivisions_internes_gauche_10_degres(),
        'subdivisions_droite_1_degre': generer_subdivisions_internes_droite_1_degre(),
        'subdivisions_droite_5_degres': generer_subdivisions_internes_droite_5_degres(),
        'subdivisions_droite_10_degres': generer_subdivisions_internes_droite_10_degres(),
        'subdivisions_droite_15_degres': generer_subdivisions_internes_droite_15_degres()
    }

def generer_chiffres_romains_direct():
    chiffres_romains = ["I", "II", "III", "IV", "V", "VI",
                        "VII", "VIII", "IX", "X", "XI", "XII"]

    angles_speciaux = [195 + 15 * i for i in range(12)]
    rayon_texte = 10.93
    decalage = -2  

    textes = []

    for i, angle_deg in enumerate(angles_speciaux):
        angle_rad = math.radians(angle_deg + decalage)
        x = rayon_texte * math.cos(angle_rad)
        y = rayon_texte * math.sin(angle_rad)
        rotation = angle_deg + decalage - 90 + 180

        textes.append({
            'chiffre': chiffres_romains[i],
            'x': round(x, 3),
            'y': round(y, 3),
            'font_size': 0.45,
            'anchor': 'middle',
            'stroke': 'none',
            'fill': 'black',
            'font_family': 'century gothic, arial, calibri',
            'rotation': rotation
        })

    return textes

def generer_quarts_cercle_direct():
    rayons = [0.7125, 1.425, 2.1375, 2.85, 3.5625, 4.275, 4.9875, 5.7, 6.4125, 7.125, 7.8375]
    arcs = []
    for rayon in rayons:
        arcs.append({'rayon': rayon, 'stroke': 'black', 'stroke_width': 0.05, 'fill': 'none'})

    points = []
    for i, rayon in enumerate(rayons, 1):
        if i > 1:
            nb_points = i - 1
            for j in range(1, nb_points + 1):
                angle = (math.pi / 2) * j / i
                x = -rayon * math.cos(angle)
                y = -rayon * math.sin(angle)
                points.append({'x': round(x, 4), 'y': round(y, 4), 'r': 0.08, 'fill': 'black'})

    points_cercle_855 = []
    rayon_855 = 8.55
    for j in range(1, 12):
        angle = (math.pi / 2) * j / 12
        x = -rayon_855 * math.cos(angle)
        y = -rayon_855 * math.sin(angle)
        points_cercle_855.append({'x': round(x, 4), 'y': round(y, 4), 'r': 0.08, 'fill': 'black'})

    return {'arcs': arcs, 'points': points, 'points_cercle_855': points_cercle_855}

# ===== Contexte =====
def _contexte_dos():
    from .traits_graduation.traits_graduation import generer_tous_traits_graduation
    from .cadre_correction.cadre_correction import generer_tous_cadres_correction
    from .arcs_gauche.arcs_gauche import generer_arcs_gauche
    from .graphe_equation_temps.graphe_equation_temps import generer_graphique_equation_temps

    traits_graduation = generer_tous_traits_graduation()
    cadres_correction = generer_tous_cadres_correction()
    diagonales_correction = generer_diagonales_correction_direct()
    quadrilateres_correction = generer_quadrilateres_correction_direct()
    subdivisions_annee = generer_subdivisions_annee_direct()
    subdivisions_internes = generer_subdivisions_internes_direct()
    chiffres_romains = generer_chiffres_romains_direct()
    quarts_cercle = generer_quarts_cercle_direct()
    arcs_gauche = generer_arcs_gauche()
    graphe_equation_temps = generer_graphique_equation_temps()

    return dict(
        traits_graduation=traits_graduation,
        cadres_correction=cadres_correction,
        diagonales_correction=diagonales_correction,
        quadrilateres_correction=quadrilateres_correction,
        subdivisions_annee=subdivisions_annee,
        subdivisions_internes=subdivisions_internes,
        chiffres_romains=chiffres_romains,
        quarts_cercle=quarts_cercle,
        arcs_gauche=arcs_gauche,
        graphe_equation_temps=graphe_equation_temps,
    )

def _contexte_anneau_ext():
    from .traits_graduation.traits_graduation import generer_tous_traits_graduation
    subdivisions_annee = generer_subdivisions_annee_direct()
    traits_graduation = generer_tous_traits_graduation()
    return dict(
        traits_graduation=traits_graduation,
        subdivisions_annee=subdivisions_annee,
    )


# =========================
# Routes
# =========================

@dos_bp.route("/", strict_slashes=False)
def show_dos():
    ctx = _contexte_dos()
    return render_template("dos.html", **ctx)

@dos_bp.route("/dos_menu/", strict_slashes=False)
def dos_menu():
    return render_template("dos_menu.html")

@dos_bp.route("/dos_classique/", strict_slashes=False)
def dos_classique():
    ctx = _contexte_dos()
    return render_template("dos.html", **ctx)

@dos_bp.route("/dos_plus/", strict_slashes=False)
def dos_plus():
    return render_template("analemme_classique.html")




# =============================================================
# 🚀 R A Y O N S   D Y N A M I Q U E S   D E   L ’ A N N E A U  E X T É R I E U R
# =============================================================
@dos_bp.route("/anneau_ext/", strict_slashes=False)
def anneau_ext():
    from flask import request

    # --- lire la valeur du diamètre envoyée depuis index.html ---
    diametre_str = request.args.get("diametre", "25")
    diametre = float(diametre_str)

    # --- calculs demandés ---
    rayon_ext = diametre / 2
    rayon_int = (9.52 / 12.35) * rayon_ext

    # --- contexte graphique existant (inchangé) ---
    ctx = _contexte_anneau_ext()

    # --- injection dans le template ---
    ctx["rayon_ext"] = round(rayon_ext, 3)
    ctx["rayon_int"] = round(rayon_int, 3)
    ctx["diametre"] = diametre

    return render_template("anneau_ext.html", **ctx)
