from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.user import User

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@routes.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.all()
    if current_user.is_authenticated:
        return render_template('homepage.html', users=users)
    else:
        return redirect(url_for('log.login'))

@routes.route('/about')
@login_required
def about():
    return render_template('about.html')

@routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
