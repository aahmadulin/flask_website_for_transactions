from flask_login import login_required, current_user
from flask import Blueprint, jsonify, render_template
from models.transaction import Transaction
from forms import TransactionForm
from flask_wtf.csrf import CSRFProtect
from app import db
from datetime import datetime
from admin_only import admin_required

import logging
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)
csrf = CSRFProtect()

@api.route('/create_transaction', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def create_transaction():
    form = TransactionForm()
    
    if form.validate_on_submit():
        amount = float(form.amount.data) 
        transaction_type = form.transaction_type.data 

        if transaction_type == 'withdrawal' and amount > current_user.balance:
            return render_template('transactions/error.html', message="Недостаточно средств на балансе.")
        
        transaction = Transaction(
            amount=amount,
            user=current_user,
            type=transaction_type,
            created_at=datetime.utcnow()
        )

        commission = transaction.calculate_commission()  
        transaction.commission = commission 

        if transaction_type == 'deposit':
            current_user.balance += amount
            transaction.status = 'confirmed'  
        elif transaction_type == 'withdrawal':
            total_deduction = amount + commission
            current_user.balance -= total_deduction 
            transaction.status = 'confirmed'  
            if current_user.balance < 0:
                transaction.status = 'failed'
                current_user.balance += total_deduction
                db.session.rollback() 
                return render_template('transactions/error.html', message="Ошибка: недостаточно средств для снятия.")

        db.session.add(transaction)
        db.session.commit()

        print(f"Transaction created: {transaction}")

        return render_template('transactions/success_create.html', transaction=transaction)
    else:
        print("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    
    return render_template('transactions/transaction_create.html', form=form)


@api.route('/cancel_transaction/<int:transaction_id>', methods=['POST', 'GET'])
@admin_required
def cancel_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.status == 'pending':
        transaction.status = 'canceled'
        db.session.commit()
        return jsonify({'message': 'Transaction canceled successfully'}), 200
    else:
        return jsonify({'message': 'Cannot cancel non-pending transaction'}), 400


@api.route('/check_transaction/<int:transaction_id>', methods=['GET'])
@login_required
def check_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction_data = jsonify({
        'id': transaction.id,
        'amount': transaction.amount,
        'commission': transaction.commission,
        'status': transaction.status,
        'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })
    return render_template('transactions/transaction_data.html', transaction_data=transaction_data)


@api.route('/transactions/<int:transaction_id>')
@login_required
def transaction_detail(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    status_colors = {
        'pending': 'warning',
        'confirmed': 'success',
        'canceled': 'danger',
        'expired': 'secondary'
    }
    return render_template('transactions/transaction_detail.html', 
                         transaction=transaction,
                         status_colors=status_colors)

@api.route('/transactions/create')
@login_required
def create_transaction_page():
    form = TransactionForm()
    return render_template('transactions/transaction_create.html', form=form)