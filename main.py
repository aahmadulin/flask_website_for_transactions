from app import create_app, db
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import click
from models.user import User

app = create_app()

login_manager = LoginManager()
login_manager.login_view = 'log.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.cli.command('create_admin')
@click.option('--email', prompt='Email', help='Email адрес администратора.')
@click.option('--password', prompt='Password', hide_input=True, help='Пароль для администратора.')
@click.option('--username', prompt='Username', help='Имя пользователя для администратора.')
def create_admin(email, password, username):
    """Создание администратора."""
    with app.app_context():
        # Проверка, существует ли уже администратор с таким email
        existing_admin = User.query.filter_by(email=email).first()
        if existing_admin:
            print(f"Администратор с email {email} уже существует.")
            return

        hashed_password = generate_password_hash(password)

        admin = User(email=email, password=hashed_password, role='admin', username=username)
        db.session.add(admin)
        db.session.commit()
        print(f"Администратор с email '{email}' успешно создан.")

if __name__ == '__main__':
    app.run(debug=True)
