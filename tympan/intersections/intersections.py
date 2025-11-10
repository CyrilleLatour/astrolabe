import os
from flask import Blueprint, render_template, request

# Chemin vers tympan/templates
template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')

# Définition du blueprint avec le bon dossier de templates
intersections_bp = Blueprint('intersections', __name__, template_folder=template_path)

# Conversion DMS → décimal
def dms_to_decimal(degres, minutes, secondes):
    return degres + minutes / 60 + secondes / 3600

@intersections_bp.route('/', methods=["GET", "POST"])
def intersections():
    latitude_decimal = None
    latitude_dms = None

    if request.method == 'POST':
        try:
            degres = int(request.form['degres'])
            minutes = int(request.form['minutes'])
            secondes = float(request.form['secondes'])

            latitude_decimal = dms_to_decimal(degres, minutes, secondes)
            latitude_dms = f"{degres}° {minutes}' {secondes}''"

        except (ValueError, KeyError):
            latitude_decimal = None
            latitude_dms = None

    return render_template('intersections.html',
                           latitude_dms=latitude_dms,
                           latitude_decimal=latitude_decimal)
