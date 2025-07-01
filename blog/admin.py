from django.contrib import admin
from .models import Blog

admin.site.register(Blog)
from django.contrib import admin
from .models import Broker

admin.site.register(Broker)

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')

