from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm, WithDrawForm, LoanRequestForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
  template_name = 'transactions/transaction_form.html'
  model = Transaction
  title = ''
  success_url = reverse_lazy('transaction-report')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs.update({
      'account': self.request.user.account
    })

    return kwargs
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'title': self.title
    })
    return context

class DepositMoneyView(TransactionCreateMixin):
  form_class = DepositForm
  title = 'Deposit'

  def get_initial(self):
    initial = {'transaction_type': 'deposit'}
    return initial
  
  def form_valid(self, form):
    print('hi')
    amount = form.cleaned_data['amount']
    account = self.request.user.account
    account.balance += amount

    account.save(
      update_fields = ['balance']
    )

    messages.success(self.request, f'{amount} was deposited to your account successfully.')

    return super().form_valid(form)
  
class WithdrawMoneyView(TransactionCreateMixin):
  form_class = WithDrawForm
  title = 'Withdraw'

  def get_initial(self):
    initial  = {'transaction_type': 'withdraw'}
    return initial
  
  def form_valid(self, form):
    amount = form.cleaned_data['amount']
    account = self.request.user.account
    account.balance -= amount
    
    account.save(
      update_fields = ['balance']
    )

    messages.success(self.request, f'{amount} was withdrawn from your account successfully.')

    return super().form_valid(form)
  
class LoanRequestView(TransactionCreateMixin):
  form_class = LoanRequestForm
  title = 'Request for loan'

  def get_initial(self):
    initial  = {'transaction_type': 'loan'}
    return initial
  
  def form_valid(self, form):
    amount = form.cleaned_data['amount']
    current_loan_count = Transaction.objects.filter(
      account = self.request.user.account,
      transaction_type = 'loan',
      loan_approved = True
    ).count()

    if current_loan_count >= 3:
      messages.warning(self.request, f'Your loan credit has exceeded! Please repay your pending loans first.')
      return

    messages.success(self.request, f'Requested for loan successfully. We will confirm soon')

    return super().form_valid(form)
  
class TransactionReportView(LoginRequiredMixin, ListView):
  template_name = 'transactions/transaction_report.html'
  model = Transaction
  balance = 0

  def get_queryset(self):
    queryset = super().get_queryset().filter(
      account = self.request.user.account
    )

    start_date_str = self.request.GET.get('start_date')
    end_date_str = self.request.GET.get('end_date')

    if start_date_str and end_date_str:
      start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
      end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

      queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)

      self.balance = queryset.aggregate(Sum('amount'))['amount__sum']
    else:
      self.balance = self.request.user.account.balance

    return queryset.distinct()
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context.update({
      'account': self.request.user.account
    })

    return context

class PayLoanView(LoginRequiredMixin, View):
  def get(self, req, loan_id):
    loan = get_object_or_404(Transaction, id = loan_id)

    if loan.loan_approved:
      user_account = loan.account

      if loan.amount < user_account.balance:
        user_account.balance -= loan.amount
        loan.balance_after_transaction = user_account.balance
        user_account.save()
        loan.transaction_type = 'loan-paid'
        loan.save()
        return redirect('loan-list')
      else:
        messages.warning(self.request, 'Insufficient balance amount.')
        return redirect('loan-list')
      
class LoanListView(LoginRequiredMixin, ListView):
  template_name = 'transactions/loan_request.html'
  model = Transaction
  context_object_name = 'loans'

  def get_queryset(self):
    user_account = self.request.user.account

    queryset = super().get_queryset().filter(account = user_account, transaction_type = 'loan')
    return queryset