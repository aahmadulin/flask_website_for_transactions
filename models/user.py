from app import db
from flask_login import UserMixin

ROLES = {
    'admin': ['admin_page', 'dashboard', 'manage_users', 'manage_transactions'],
    'user': ['user_page', 'create_transaction', 'view_transactions'],
}

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    balance = db.Column(db.Float, default=0)
    commission_rate = db.Column(db.Float, default=0)
    url = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(80), nullable=False) 

    transactions = db.relationship('Transaction', overlaps='user.transactions')
    
    def __init__(self, username, password, email, role='user', balance=0, commission_rate=2, url=None):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        if commission_rate < 0:
            raise ValueError("Ставка комиссии не может быть отрицательной.")
        if role not in ROLES:
            raise ValueError(f"Некорректная роль: {role}. Доступные роли: {', '.join(ROLES.keys())}.")
        
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.balance = balance
        self.commission_rate = commission_rate
        self.url = url

    def add_balance(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Баланс пополнен на {amount}. Текущий баланс: {self.balance}"
        return "Ошибка: сумма пополнения должна быть больше 0."

    def deduct_balance(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return f"С баланса списано {amount}. Текущий баланс: {self.balance}"
        return "Ошибка: недостаточно средств или некорректная сумма."

    def set_commission_rate(self, rate):
        if rate >= 0:
            self.commission_rate = rate
            return f"Ставка комиссии обновлена: {self.commission_rate}%"
        return "Ошибка: ставка комиссии должна быть больше или равна 0."

    def set_webhook_url(self, url):
        self.url = url
        return f"URL вебхука обновлен: {self.url}"

    def get_webhook_url(self):
        return self.url