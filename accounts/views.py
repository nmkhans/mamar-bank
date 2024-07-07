from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserProfileUpdateForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.contrib import messages 
from transactions.views import send_mail_to_user

# Create your views here.
class UserRegisterView(FormView):
  template_name = 'accounts/user_register.html'
  form_class = UserRegisterForm
  success_url = reverse_lazy('user-profile')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return super().form_valid(form)
  
class UserLoginView(LoginView):
  template_name = 'accounts/user_login.html'
  
  def get_success_url(self):
    return reverse_lazy('home')
  
def user_logout(req):
  logout(req)
  return redirect('home')

class UserProfileView(View):
  template_name = 'accounts/user_profile.html'

  def get(self, request):
    form = UserProfileUpdateForm(instance = request.user)
    return render(request, self.template_name, {
      'form': form
    })
  
  def post(self, request):
    form = UserProfileUpdateForm(request.POST, instance = request.user)

    if form.is_valid():
      form.save()
      return redirect('user-profile')
    
    return render(request, self.template_name, {
      'form': form
    })
  
class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/user_password_change.html'
  success_url = reverse_lazy('user-profile')
  model = User

  def form_valid(self, form):
    messages.success(self.request, 'Password has been changed')

    send_mail_to_user(
      "Password change",
      self.request.user,
      0, 
      'accounts/password_change_mail.html'
    )

    return super().form_valid(form)