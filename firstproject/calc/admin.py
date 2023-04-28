from django.contrib import admin

# Register your models here.
from .models import Guide, Traveller
admin.site.register(Guide)
admin.site.register(Traveller)

