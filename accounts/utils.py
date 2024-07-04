import random
import math

digits = [i for i in range(0, 10)]


def gen_account_no():
  account_no = ""
  for i in range(6):
    index = math.floor(random.random() * 10)
    account_no += str(digits[index])
  return account_no