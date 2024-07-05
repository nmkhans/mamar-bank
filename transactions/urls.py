from django.urls import path
from . import views

urlpatterns = [
  path('deposit/', views.DepositMoneyView.as_view(), name = "deposit-money"),
  path('withdraw/', views.WithdrawMoneyView.as_view(), name = "withdraw-money"),
  path('loan-request/', views.LoanRequestView.as_view(), name = "loan-request"),
  path('report/', views.TransactionReportView.as_view(), name = "transaction-report"),
  path('pay-loan/<int:loan_id>/', views.PayLoanView.as_view(), name = "pay-loan"),
  path('loan-list/', views.LoanListView.as_view(), name = "loan-list"),
]
