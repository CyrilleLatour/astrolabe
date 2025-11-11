from flask import Blueprint, render_template, request, session, redirect, url_for
import math
from .almucantarats.almucantarats import Almucantarats
from .crepuscules.crepuscules import Crepuscules
from .azimuts.courbes_azimuts import CourbesAzimut
from .h_inegales.h_inegales import HeuresInegales
from .h_inegales import points

tympan_bp = Blueprint('tympan', __name__, template_folder='templates')


# ================================================================
# 🟦 PAGE PRINCIPALE DU TYMPAN
# ================================================================
@tympan_bp.route('/', methods=['GET', 'POST'])
def tympan():
    reset_param = request.args.get('reset', '0')
    if reset_param == '1':
        session['first_visit_tympan'] = True

    rayon_equateur = session.get('rayon_equateur')
    latitude = None
    latitude_dms = None
    show_chart = False
    first_visit = session.get('first_visit_tympan', True)

    if rayon_equateur is None:
        rayon_equateur = 6
        session['rayon_equateur'] = 6

    latitude_arg = request.args.get('latitude')
    if latitude_arg:
        try:
            latitude = float(latitude_arg)
            session['latitude'] = latitude
        except ValueError:
            latitude = None

    if request.method == 'POST':
        degres = request.form.get('degres')
        minutes = request.form.get('minutes')
        secondes = request.form.get('secondes')
        latitude_decimale = request.form.get('latitudeDecimale')

        if latitude_decimale:
            try:
                latitude = float(latitude_decimale)
            except ValueError:
                latitude = None
        else:
            try:
                d = float(degres or 0)
                m = float(minutes or 0)
                s = float(secondes or 0)
                latitude = d + m / 60 + s / 3600
            except ValueError:
                latitude = None

        if latitude is not None:
            deg = int(latitude)
            minutes_float = (latitude - deg) * 60
            min_ = int(minutes_float)
            sec = round((minutes_float - min_) * 60)
            latitude_dms = f"{deg}° {min_}' {sec}\""
            session['latitude'] = latitude
            show_chart = True
            session['first_visit_tympan'] = False

    if request.method == 'GET' and not latitude and 'latitude' in session:
        latitude = session['latitude']
        deg = int(latitude)
        minutes_float = (latitude - deg) * 60
        min_ = int(minutes_float)
        sec = round((minutes_float - min_) * 60)
        latitude_dms = f"{deg}° {min_}' {sec}\""
        show_chart = True
        first_visit = False

    if not show_chart or latitude is None:
        return render_template(
            'tympan.html',
            show_chart=False,
            first_visit=first_visit,
            reset=reset_param,
            latitude=None,
            latitude_dms=None,
            facteur=1,
            rayon_equateur=rayon_equateur,
            position_centre_ecliptique=0,
            fixed_radius_ecliptique=5.8,
            fixed_radius_equateur=6,
            fixed_radius_cancer=5.8,
            fixed_radius_capricorne=5.8,
            fixed_radius_tropiques=5.8,
            fixed_radius_suppl=5.8,
            fixed_radius_suppl2=5.8,
            fixed_radius_suppl3=5.8,
            fixed_radius_suppl4=5.8,
            fixed_radius_suppl5=5.8,
            almucantarats=[],
            horizon=None,
            cercles_crepuscules=[],
            cercles_solstices=[],
            courbes_azimut=[],
            ligne_suppl_horizon=None,
            masques=[],
            points_heures=None
        )
    facteur = 140 / rayon_equateur
    centre_y = 300

    obliquite = 23.44
    S = rayon_equateur / 2
    rayon_ecliptique = S * (math.tan(math.radians((90 + obliquite) / 2)) + math.tan(math.radians((90 - obliquite) / 2)))
    position_centre_ecliptique = rayon_ecliptique - 2 * S * math.tan(math.radians((90 - obliquite) / 2))

    ratio_cancer = 3.939 / 6
    ratio_capricorne = 9.141 / 6
    ratio_suppl = 10.5 / 6

    fixed_radius_equateur = rayon_equateur
    fixed_radius_cancer = rayon_equateur * ratio_cancer
    fixed_radius_capricorne = rayon_equateur * ratio_capricorne
    fixed_radius_ecliptique = rayon_ecliptique
    fixed_radius_suppl = rayon_equateur * ratio_suppl

    alm = Almucantarats(rayon_equateur, latitude)
    data_alm = alm.get_data()
    almucantarats = data_alm["almucantarats"]
    horizon = data_alm["horizon"]

    crep = Crepuscules(rayon_equateur, latitude, facteur=facteur)
    data_crep = crep.get_data()
    cercles_crepuscules = data_crep.get("cercles_crepuscules", [])
    cercles_solstices = data_crep.get("cercles_solstices", [])

    # AJOUTER LES CERCLES CALCULÉS Z=-6, -12, -18 EN NOIR
    for Z in [-6, -12, -18]:
        cercle = alm.calculer_almucantarat(Z)
        if cercle and cercle.get("type") != "ligne_horizontale":
            cercles_crepuscules.append({
                'cx': 0,
                'cy': cercle['cy'],
                'rayon': cercle['rayon'],
                'hauteur': Z,
                'style': {'fill': 'none', 'stroke': 'black', 'stroke_width': 1, 'stroke_opacity': 0.7}
            })

    courbes_az = CourbesAzimut(rayon_equateur, latitude)
    courbes_azimut = courbes_az.get_data()
    for courbe in courbes_azimut:
        courbe['stroke_width'] = 2.5 if courbe['color'] == 'black' else 1

    latitude_rad = math.radians(latitude)
    angle_max_deg = 90 - latitude
    
    print("=" * 60)
    print(f"AVANT APPEL generer_points_cercles:")
    print(f"  latitude = {latitude}")
    print(f"  horizon type = {horizon.get('type') if horizon else 'None'}")
    print(f"  horizon data = {horizon}")
    print("=" * 60)
    
    points_heures = points.generer_points_cercles(
        cx=300,
        cy=centre_y,
        facteur=facteur,
        rayon_cancer=fixed_radius_cancer,
        rayon_equateur=fixed_radius_equateur,
        rayon_capricorne=fixed_radius_capricorne,
        angle_max_deg=angle_max_deg,
        horizon_data=horizon
    )
    
    print("=" * 60)
    print(f"APRÈS APPEL generer_points_cercles:")
    print(f"  courbes_gauche = {len(points_heures.get('courbes_gauche', []))}")
    print(f"  courbes_droite = {len(points_heures.get('courbes_droite', []))}")
    if points_heures.get('courbes_gauche'):
        print(f"  Premier élément gauche: {points_heures['courbes_gauche'][0]}")
    print("=" * 60)

    ligne_suppl_horizon = None
    
    return render_template(
        'tympan.html',
        show_chart=True,
        latitude=latitude,
        latitude_dms=latitude_dms,
        facteur=facteur,
        rayon_equateur=rayon_equateur,
        position_centre_ecliptique=position_centre_ecliptique,
        fixed_radius_ecliptique=fixed_radius_ecliptique,
        fixed_radius_equateur=fixed_radius_equateur,
        fixed_radius_cancer=fixed_radius_cancer,
        fixed_radius_capricorne=fixed_radius_capricorne,
        fixed_radius_tropiques=fixed_radius_cancer,
        fixed_radius_suppl=fixed_radius_suppl,
        fixed_radius_suppl2=fixed_radius_suppl,
        fixed_radius_suppl3=fixed_radius_suppl,
        fixed_radius_suppl4=fixed_radius_suppl,
        fixed_radius_suppl5=fixed_radius_suppl,
        almucantarats=almucantarats,
        horizon=horizon,
        cercles_crepuscules=cercles_crepuscules,
        cercles_solstices=cercles_solstices,
        courbes_azimut=courbes_azimut,
        ligne_suppl_horizon=ligne_suppl_horizon,
        masques=[],
        points_heures=points_heures
    )


# ================================================================
# 🟦 PAGE MENU DU TYMPAN
# ================================================================
@tympan_bp.route('/menu', methods=['GET'])
def menu():
    return render_template('tympan_menu.html')


# ================================================================
# 🟪 PAGE DU LIMBE
# ================================================================
@tympan_bp.route('/limbe', methods=['GET', 'POST'])
def limbe():
    return render_template('limbe.html')


# ================================================================
# 🟩 PAGE D'INDEX (SÉLECTION DU RAYON DE L'ÉQUATEUR)
# ================================================================
@tympan_bp.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rayon_equateur = request.form.get('rayon')
        if rayon_equateur:
            try:
                rayon_equateur = float(rayon_equateur)
                session['rayon_equateur'] = rayon_equateur
                session['first_visit_tympan'] = True
                return redirect(url_for('tympan.tympan'))
            except ValueError:
                pass
    return render_template('index.html')


# ================================================================
# 🟨 DEBUG : ALMUCANTARATS
# ================================================================
@tympan_bp.route('/debug_almucantarats')
def debug_almucantarats():
    rayon_equateur = session.get('rayon_equateur')
    latitude = session.get('latitude')
    if not rayon_equateur or not latitude:
        return "Rayon ou latitude manquant dans la session.", 400

    alm = Almucantarats(rayon_equateur, latitude)
    data = alm.get_data()
    almucantarats = data["almucantarats"]

    for cercle in almucantarats:
        hauteur = cercle.get('hauteur', cercle.get('Z', '?'))
        rayon = cercle.get('rayon', '?')
        cy = cercle.get('cy', '?')
        print(f"Hauteur={hauteur}° | rayon={rayon} | cy={cy}")

    return f"{len(almucantarats)} cercles calculés. Consultez la console."


# ================================================================
# 🟧 DEBUG : CRÉPUSCULES
# ================================================================
@tympan_bp.route('/debug_crepuscules')
def debug_crepuscules():
    rayon_equateur = session.get('rayon_equateur')
    latitude = session.get('latitude')
    if not rayon_equateur or not latitude:
        return "Rayon ou latitude manquant dans la session.", 400

    crep = Crepuscules(rayon_equateur, latitude)
    cercles = crep.get_data()["cercles_crepuscules"]

    for c in cercles:
        print(f"Z={c['hauteur']:>5.1f}° | cy={c['cy']:.3f} | r={c['rayon']:.3f} | {c['style']['stroke']}")

    return f"{len(cercles)} cercles de crépuscules calculés. Consultez la console."