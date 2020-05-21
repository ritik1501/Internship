from django.contrib import admin
from covid.models import UserData, LargeData

# Register your models here.
admin.site.register(UserData)
admin.site.register(LargeData)

admin.site.site_header = "COVID-19 Admin"
admin.site.site_title = "COVID-19 Admin Portal"
admin.site.index_title = "Welcome to COVID-19 Checker Portal"