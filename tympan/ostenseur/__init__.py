from flask import Blueprint, render_template

ostenseur = Blueprint('ostenseur', __name__, template_folder='templates')

@ostenseur.route('/ostenseur/')
def menu():
    return render_template('ostenseur.html')
