from django.contrib import admin
from home.models import *

# Register your models here.

admin.site.register(FoodItem)
admin.site.register(BranchFood)
admin.site.register(BranchStaff)
admin.site.register(CafeBranch)
admin.site.register(OrderCart)
admin.site.register(Order)