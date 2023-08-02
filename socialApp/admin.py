from django.contrib import admin
from socialApp.models import *

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Friend._meta.get_fields()]