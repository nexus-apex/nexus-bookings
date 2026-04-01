from django.contrib import admin
from .models import Service, Appointment, Client

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "duration_mins", "price", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "category", "provider"]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["client_name", "client_email", "service_name", "provider", "date", "created_at"]
    list_filter = ["status"]
    search_fields = ["client_name", "client_email", "service_name"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "total_bookings", "total_spent", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "phone"]
