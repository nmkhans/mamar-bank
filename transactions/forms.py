from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ['amount', 'transaction_type']

  def __init__(self, *args, **kwargs):
    self.account = kwargs.pop('account')
    super().__init__(*args, **kwargs)

    self.fields['transaction_type'].disabled = True
    self.fields['transaction_type'].widget = forms.HiddenInput()

  def save(self, commit = True):
    self.instance.account = self.account
    self.instance.balance_after_transaction = self.account.balance
    return super().save()
  
class DepositForm(TransactionForm):
  def clean_amount(self):
    min_amount = 100
    amount = self.cleaned_data['amount']

    if amount < min_amount:
      raise forms.ValidationError(
        f'You need to deposit at least {min_amount}'
      )
    return amount
  
class WithDrawForm(TransactionForm):
  def clean_amount(self):
    account = self.account
    min_amount = 500
    max_amount = 20000
    balance = account.balance
    amount = self.cleaned_data['amount']

    if amount < min_amount:
      raise forms.ValidationError(
        f'You can not withdraw below {min_amount}'
      )
    
    if amount > max_amount:
      raise forms.ValidationError(
        f'You can not withdraw more than {max_amount}'
      )
    
    if amount > balance:
      raise forms.ValidationError(
        f'Insufficient balance.'
        f'your current balance is {balance}'

      ) 
    
    return amount
  
class LoanRequestForm(TransactionForm):
  def clean_amount(self):
    amount = self.cleaned_data['amount']
    return amount