from wtforms import IntegerField, SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    id = IntegerField('ID транзакции', validators=[])
    amount = IntegerField('Amount', validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], validators=[DataRequired()])
    submit = SubmitField('Submit')
