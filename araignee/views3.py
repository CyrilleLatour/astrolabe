from flask import Blueprint, render_template

# IMPORTANT :
# - On garde le nom d'endpoint "araignee" (pour ne rien casser dans url_for('araignee...'))
# - On précise template_folder="templates" car le template est dans araignee_nord/templates/
araignee_bp = Blueprint("araignee", __name__, template_folder="templates")


# ================================================================
# 🟦 PAGE MENU DE L'ARAIGNÉE
# ================================================================
@araignee_bp.route('/menu', methods=['GET'])
def menu():
    return render_template('araignee_menu.html')


# ================================================================
# 🟦 PAGE ARAIGNÉE NORD
# ================================================================
@araignee_bp.route('/araignee_nord', methods=['GET'])
def araignee_nord():
    return render_template('araignee_nord.html')


# ================================================================
# 🟪 PAGE ARAIGNÉE SUD
# ================================================================
@araignee_bp.route('/araignee_sud', methods=['GET'])
def araignee_sud():
    return render_template('araignee_sud.html')


# ================================================================
# 🟩 PAGE PAR DÉFAUT (REDIRIGE VERS LE MENU)
# ================================================================
@araignee_bp.route("/")
def show_araignee():
    # Redirige vers le menu au lieu d'afficher directement araignee_nord.html
    return render_template("araignee_menu.html")