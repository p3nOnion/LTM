from GAMES.models import *
from Accounts.models import *
import django
import os
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LTM.settings')
#
django.setup()
# from CTF.models import *
# user = User.objects.all()
# print(user)
BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)
