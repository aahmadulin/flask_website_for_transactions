import requests
from datetime import datetime, timedelta
from celery import Celery
from app import db
from models import Transaction 

celery = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def check_and_update_transactions():
    transactions = Transaction.query.filter(Transaction.status == 'pending').all()

    now = datetime.utcnow()

    for transaction in transactions:
        if now - transaction.created_at > timedelta(minutes=15):
            transaction.status = 'expired'

            if transaction.user.url: 
                payload = {
                    'transaction_id': transaction.id,
                    'status': transaction.status
                }
                try:
                    response = requests.post(transaction.user.url, json=payload)
                    if response.status_code == 200:
                        print(f"Webhook отправлен для транзакции {transaction.id}")
                    else:
                        print(f"Ошибка при отправке вебхука для транзакции {transaction.id}")
                except requests.RequestException as e:
                    print(f"Ошибка при отправке вебхука для транзакции {transaction.id}: {e}")

            db.session.commit()
