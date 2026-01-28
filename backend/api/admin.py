"""
Admin configuration for the API models.
"""
from django.contrib import admin
from .models import Equipment, UploadSession


@admin.register(UploadSession)
class UploadSessionAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'record_count']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['filename']
    date_hierarchy = 'uploaded_at'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'session']
    list_filter = ['equipment_type', 'session']
    search_fields = ['name']
