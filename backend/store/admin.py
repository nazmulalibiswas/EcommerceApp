from django.contrib import admin
from .models import *

admin.site.register(Cart)
admin.site.register(Categories)
admin.site.register(OrderItems)
admin.site.register(Orders)
admin.site.register(Payments)
admin.site.register(Products)
admin.site.register(Reviews)
admin.site.register(Users)

