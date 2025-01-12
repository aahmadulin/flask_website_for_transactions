from app import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    commission = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    type = db.Column(db.String(20), nullable=False) 
    STATUSES = ['pending', 'confirmed', 'canceled', 'expired']

    user = db.relationship('User', overlaps='user')

    def __init__(self, amount, user, created_at, type = 'deposit', status='pending'):
        if amount <= 0:
            raise ValueError("Сумма транзакции должна быть больше 0.")
        if status not in self.STATUSES:
            raise ValueError(f"Некорректный статус транзакции. Доступные статусы: {', '.join(self.STATUSES)}.")

        self.amount = amount
        self.user = user
        self.commission = self.calculate_commission()
        self.status = status
        self.created_at = created_at
        self.type = type

    
    def calculate_commission(self):
        return (self.amount * self.user.commission_rate) / 100
    
    def process_transaction(self):
        if self.type == 'deposit':
            self.user.balance += self.amount
            self.status = 'confirmed'
        elif self.type == 'withdrawal':
            total_amount_to_deduct = self.amount + self.commission
            if self.user.balance >= total_amount_to_deduct:
                self.user.balance -= total_amount_to_deduct
                self.status = 'confirmed'
            else:
                self.status = 'failed'
        db.session.commit()

    def get_total_amount(self):
        return self.amount + self.commission

    def set_status(self, new_status):
        if new_status in self.STATUSES:
            self.status = new_status
            return f"Статус транзакции обновлен: {self.status}"
        return f"Ошибка: недопустимый статус. Доступные статусы: {', '.join(self.STATUSES)}."

    def get_transaction_info(self):
        return {
            "amount": self.amount,
            "commission": self.commission,
            "total_amount": self.get_total_amount(),
            "status": self.status,
            "user": self.user.username
        }