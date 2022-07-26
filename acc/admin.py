from django.contrib import admin

# Register your models here.

from .models import *
from core.models import *

admin.site.register([User, Service, UserSkill, UserRating,])
admin.site.register([OrderItem, Order, Address, Payment,Refund, ContractService])
