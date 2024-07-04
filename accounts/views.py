from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class UserRegisterView(FormView):
  template_name = 'accounts/user_register.html'
  form_class = UserRegisterForm
  success_url = reverse_lazy('user-register')

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