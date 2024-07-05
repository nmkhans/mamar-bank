from django.contrib import admin
from .models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
  list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approved']

  def save_model(self, req, obj, form, change):
    if obj.loan_approved == True:
      obj.account.balance += obj.amount
      obj.account.save()

      obj.balance_after_transaction = obj.account.balance
      obj.save()
    return super().save_model(req, obj, form, change)