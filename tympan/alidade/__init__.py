from flask import Blueprint, render_template

alidade = Blueprint('alidade', __name__, template_folder='templates')

@alidade.route('/alidade/')
def menu():
    return render_template('alidade.html')
