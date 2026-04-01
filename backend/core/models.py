from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    duration_mins = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    provider = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(blank=True, default="")
    service_name = models.CharField(max_length=255, blank=True, default="")
    provider = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    time_slot = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("booked", "Booked"), ("confirmed", "Confirmed"), ("completed", "Completed"), ("cancelled", "Cancelled"), ("no_show", "No Show")], default="booked")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.client_name

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    total_bookings = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_visit = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
