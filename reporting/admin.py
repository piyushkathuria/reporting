from django.contrib import admin
from reporting.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Business)
admin.site.register(Invoice)
admin.site.register(Job)
admin.site.register(LineItem)
admin.site.register(Payment)