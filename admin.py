from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models.user import User as user
from models.transaction import Transaction as transaction
from datetime import datetime
from sqlalchemy import func
from app import db
from admin_only import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard/')
@login_required
@admin_required
def dashboard():
    users_count = user.query.count()
    transactions_count = transaction.query.count()
    today = datetime.now().date()
    today_transactions = transaction.query.filter(
        func.date(transaction.created_at) == today
    ).all()
    today_amount = sum(t.amount for t in today_transactions)
    recent_transactions = transaction.query.order_by(
        transaction.created_at.desc()
    ).limit(5).all()
    
    return render_template('dashboard.html',
                         users_count=users_count,
                         transactions_count=transactions_count,
                         today_amount=today_amount,
                         recent_transactions=recent_transactions)

@admin.route('/users/')
@login_required
@admin_required
def users():
    users = user.query.all()
    return render_template('users.html', users=users)


@admin.route('/users/create/', methods=['POST', 'GET'])
@login_required
@admin_required
def create_user():
    data = request.json
    new_user = user(
        username=data['username'],
        commission_rate=data['commission_rate'],
        role=data['role'],
        password=data['password'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})


@admin.route('/users/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def manage_user(user_id):
    managed_user = user.query.get_or_404(user_id)
    if request.method == 'DELETE':
        db.session.delete(managed_user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    
    data = request.json
    managed_user.username = data['username']
    managed_user.commission_rate = data['commission_rate']
    managed_user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


@admin.route('/transactions/')
@login_required
@admin_required
def transactions():
    transactions = transaction.query.all()
    return render_template('transaction.html', transactions=transactions)


@admin.route('/transactions/update_status', methods=['POST'])
@login_required
@admin_required
def update_status():
    data = request.json
    transaction_id = data.get('transaction_id')
    new_status = data.get('status')

    if new_status not in ['pending', 'confirmed', 'canceled', 'expired']:
        return jsonify({'message': 'Invalid status'}), 400

    selected_transaction = transaction.query.get_or_404(transaction_id)

    selected_transaction.status = new_status
    db.session.commit()

    return jsonify({'message': 'Status updated successfully'})

@admin.route('/transactions/data/')
@login_required
@admin_required
def transactions_data():
    transactions = transaction.query.all()
    return jsonify([{
        'id': t.id,
        'amount': t.amount,
        'commission': t.commission,
        'status': t.status,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for t in transactions])


@admin.route('/transactions/<int:transaction_id>/', methods=['GET', 'PUT'])
@login_required
@admin_required
def transaction_detail(transaction_id):
    selected_transaction = transaction.query.get_or_404(transaction_id)

    status_colors = {
        'pending': 'warning',
        'confirmed': 'success',
        'canceled': 'danger',
        'expired': 'secondary'
    }

    if request.method == 'PUT':
        data = request.json
        if selected_transaction.status == 'pending':
            selected_transaction.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Transaction status updated'})
        return jsonify({'message': 'Cannot update non-pending transaction'}), 400
    
    return render_template('transactions/transaction_detail.html', transaction=selected_transaction, status_colors=status_colors)