from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserProfileUpdateForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView

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