from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE_CHOICES, GENDER_CHOICES

class UserAccount(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'account')
  account_no = models.CharField(max_length = 6, unique = True)
  account_type = models.CharField(max_length = 100, choices = ACCOUNT_TYPE_CHOICES)
  date_of_birth = models.DateField(null = True, blank = True)
  gender = models.CharField(max_length = 100, choices = GENDER_CHOICES)
  account_created_at = models.DateField(auto_now_add = True)
  balance = models.DecimalField(default = 0, max_digits = 12, decimal_places = 2)

  def __str__(self):
    return f'User: {self.user.username} - Account no: {self.account_no}'


class UserAddress(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'address')
  street_address = models.CharField(max_length = 100)
  city = models.CharField(max_length = 100)
  postal_code = models.IntegerField()
  country = models.CharField(max_length = 100)

  def __str__(self):
    return f'User: {self.user.username} - Address: {self.street_address}'