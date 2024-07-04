from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.views.generic import FormView
from django.contrib.auth import login

# Create your views here.
class UserRegisterView(FormView):
  template_name = 'accounts/user_register.html'
  form_class = UserRegisterForm
  success_url = reverse_lazy('user-register')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return super().form_valid(form)
