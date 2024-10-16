from django.contrib import admin
from .models import YogaPose

@admin.register(YogaPose)
class YogaPoseAdmin(admin.ModelAdmin):
    list_display = ('name','description','image')

# Register your models here.
