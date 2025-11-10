# app.py
from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import time, webbrowser, traceback, os, sys

# -----------------------------------------------------------------------------
# Crée l'app en premier
# -----------------------------------------------------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.secret_key = "superclepourlasession"

# -----------------------------------------------------------------------------
# Ajoute le dossier des templates d'analemme au loader Jinja
# (dos/dos_plus/analemme_classique/templates)
# -----------------------------------------------------------------------------
from jinja2 import ChoiceLoader, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
analemme_templates = os.path.join(BASE_DIR, "dos", "dos_plus", "analemme_classique", "templates")

# Conserve le loader actuel + ajoute le dossier analemme
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(analemme_templates),
])

# -----------------------------------------------------------------------------
# Debug minimal
# -----------------------------------------------------------------------------
@app.route("/ping")
def ping():
    return "pong"

@app.route("/__whoami")
def whoami():
    return f"<pre>PID: {os.getpid()}\nCWD: {os.getcwd()}\nFILE: {__file__}\nPYTHON: {sys.executable}\n</pre>"

@app.route("/__routes")
def routes():
    return "<pre>" + "\n".join(sorted(str(r) for r in app.url_map.iter_rules())) + "</pre>"

# -----------------------------------------------------------------------------
# Imports avec logs (Blueprints)
# -----------------------------------------------------------------------------
tympan_bp = None
intersections_bp = None
dos_bp = None
araignee_bp = None

try:
    from tympan.views import tympan_bp as _tympan_bp
    tympan_bp = _tympan_bp
    print("[OK] Imported tympan.views")
except Exception as e:
    print("[IMPORT ERROR] tympan.views:", e)
    traceback.print_exc()

try:
    from tympan.intersections.intersections import intersections_bp as _intersections_bp
    intersections_bp = _intersections_bp
    print("[OK] Imported tympan.intersections.intersections")
except Exception as e:
    print("[IMPORT ERROR] tympan.intersections.intersections:", e)
    traceback.print_exc()

try:
    # Blueprint du DOS (routes /dos_menu/, /dos_classique/, /dos_plus/ dans dos/dos_classique/views2.py)
    from dos.dos_classique.views2 import dos_bp as _dos_bp
    dos_bp = _dos_bp
    print("[OK] Imported dos.dos_classique.views2")
except Exception as e:
    print("[IMPORT ERROR] dos.dos_classique.views2:", e)
    traceback.print_exc()

try:
    from araignee_nord.views3 import araignee_bp as _araignee_bp
    araignee_bp = _araignee_bp
    print("[OK] Imported araignee_nord.views3")
except Exception as e:
    print("[IMPORT ERROR] araignee_nord.views3:", e)
    traceback.print_exc()

# -----------------------------------------------------------------------------
# Fallbacks si un BP ne charge pas
# -----------------------------------------------------------------------------
if tympan_bp is None:
    tympan_bp = Blueprint("tympan", __name__, template_folder="templates")

    @tympan_bp.route("/", methods=["GET", "POST"], strict_slashes=False, endpoint="tympan")
    @tympan_bp.route("", methods=["GET", "POST"])
    def tympan_fallback():
        latitude = request.form.get("latitudeDecimale") if request.method == "POST" else None
        # Le template 'tympan.html' attend 'latitude' et 'show_chart'
        return render_template("tympan.html", latitude=latitude, show_chart=bool(latitude))

if dos_bp is None:
    # Ce fallback rendra un dos.html "simple" si jamais l'import échoue
    dos_bp = Blueprint("dos", __name__, template_folder="templates")

    @dos_bp.route("/", strict_slashes=False)
    @dos_bp.route("")
    def dos_fallback():
        return render_template("dos.html")

if araignee_bp is None:
    araignee_bp = Blueprint("araignee", __name__, template_folder="templates")

    @araignee_bp.route("/", strict_slashes=False)
    @araignee_bp.route("")
    def araignee_fallback():
        return render_template("araignee_nord.html")

# -----------------------------------------------------------------------------
# Enregistrement des Blueprints
# -----------------------------------------------------------------------------
app.register_blueprint(tympan_bp, url_prefix="/tympan/")
if intersections_bp:
    app.register_blueprint(intersections_bp, url_prefix="/intersections")
app.register_blueprint(dos_bp, url_prefix="/dos")
app.register_blueprint(araignee_bp, url_prefix="/araignee")

# -----------------------------------------------------------------------------
# Accueil
# -----------------------------------------------------------------------------
@app.route('/', methods=["GET", "POST"])
def index():
    reset_param = request.args.get('reset', '0')
    validation_ok = False
    rayon = None

    if request.method == 'POST':
        if 'rayon' in request.form and request.form['rayon']:
            rayon = int(request.form['rayon'])
            session['rayon_equateur'] = rayon
            validation_ok = True
            session['first_visit'] = False
    elif reset_param == '1':
        rayon = None
        session.pop('rayon_equateur', None)
        session['first_visit'] = True
        session['first_visit_tympan'] = True
    else:
        rayon = session.get('rayon_equateur')
        if rayon is not None:
            session['first_visit'] = False

    first_visit = session.get('first_visit', True)
    return render_template('index.html', validation_ok=validation_ok, rayon_equateur=rayon, first_visit=first_visit)

@app.route('/reset')
def reset():
    session.clear()
    session['first_visit'] = True
    session['first_visit_tympan'] = True
    timestamp = int(time.time())
    return redirect(f'/?reset=1&ts={timestamp}')

# -----------------------------------------------------------------------------
# DEBUG TYMPAN IMPORT (routes de diagnostic)
# -----------------------------------------------------------------------------
@app.route("/__tympan_import")
def __tympan_import():
    rows = []
    def line(k, v=""):
        rows.append(f"<tr><th align='left' style='padding:4px 8px'>{k}</th><td><pre style='margin:0'>{v}</pre></td></tr>")

    line("CWD", os.getcwd())
    line("sys.executable", sys.executable)
    line("sys.path[:5]", "\n".join(sys.path[:5]))

    # Liste du dossier racine et du dossier tympan
    try:
        line("ls .", "\n".join(sorted(os.listdir("."))[:200]))
    except Exception as e:
        line("ls . ERROR", str(e))
    try:
        line("ls tympan", "\n".join(sorted(os.listdir("tympan"))[:200]))
    except Exception as e:
        line("ls tympan ERROR", str(e))

    # Tentative d'import détaillée
    try:
        import tympan.views as tv
        line("IMPORT tympan.views", "OK ✅")
        bp = getattr(tv, "tympan_bp", None)
        line("has tympan_bp", str(bool(bp)))
    except Exception:
        line("IMPORT ERROR tympan.views", traceback.format_exc())

    html = "<table border='1' cellspacing='0' cellpadding='0' style='border-collapse:collapse;font-family:monospace;font-size:13px'>" + "".join(rows) + "</table>"
    return f"<h2>__tympan_import</h2>{html}"

@app.route("/__tympan_enable_if_ok")
def __tympan_enable_if_ok():
    try:
        from tympan.views import tympan_bp as _tympan_bp
        app.register_blueprint(_tympan_bp, url_prefix="/tympan_real")
        return "<pre>Blueprint tympan chargé et monté sur /tympan_real ✅</pre>"
    except Exception as e:
        return f"<pre>ECHEC: {e}\n{traceback.format_exc()}</pre>"

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:1200")

if __name__ == "__main__":
    print("\n--- URL MAP AU DÉMARRAGE ---")
    for r in app.url_map.iter_rules():
        print("  ", r)
    print("-----------------------------\n")
    app.run(debug=True, port=1200)
