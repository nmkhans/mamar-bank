from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .constants import ACCOUNT_TYPE_CHOICES, GENDER_CHOICES
from .models import UserAccount, UserAddress
from .utils import gen_account_no

class UserRegisterForm(UserCreationForm):
  account_type = forms.ChoiceField(choices = ACCOUNT_TYPE_CHOICES)
  date_of_birth = forms.DateField(widget = forms.DateInput(attrs = {
    'type': 'date'
  }))
  gender = forms.ChoiceField(choices = GENDER_CHOICES)
  street_address = forms.CharField(max_length = 100)
  city = forms.CharField(max_length = 100)
  postal_code = forms.IntegerField()
  country = forms.CharField(max_length = 100)

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'account_type', 'date_of_birth', 'gender', 'street_address', 'city', 'postal_code', 'country']

  def save(self, commit = True):
    user = super().save(commit = False)

    if commit == True:
      user.save()

      account_type = self.cleaned_data['account_type']
      date_of_birth = self.cleaned_data['date_of_birth']
      gender = self.cleaned_data['gender']
      street_address = self.cleaned_data['street_address']
      city = self.cleaned_data['city']
      postal_code = self.cleaned_data['postal_code']
      country = self.cleaned_data['country']

      UserAddress.objects.create(
        user = user,
        street_address = street_address,
        city = city,
        postal_code = postal_code,
        country = country
      )

      UserAccount.objects.create(
        user = user,
        account_no = gen_account_no(),
        account_type = account_type,
        date_of_birth = date_of_birth,
        gender = gender
      )

      return user
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    for field in self.fields:
      self.fields[field].widget.attrs.update({
        'class': (
          'appearance-none block w-full bg-gray-200 '
          'text-gray-700 border border-gray-200 rounded '
          'py-3 px-4 leading-tight focus:outline-none '
          'focus:bg-white focus:border-gray-500 '
        )
      })

