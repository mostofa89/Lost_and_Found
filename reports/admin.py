from django.contrib import admin
from .models import Lost_reports, Found_reports, Claimed_items

# Register your models here.
admin.site.register(Lost_reports)
admin.site.register(Found_reports)
admin.site.register(Claimed_items)