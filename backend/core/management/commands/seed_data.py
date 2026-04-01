from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Service, Appointment, Client
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusBookings with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusbookings.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Service.objects.count() == 0:
            for i in range(10):
                Service.objects.create(
                    name=f"Sample Service {i+1}",
                    category=f"Sample {i+1}",
                    duration_mins=random.randint(1, 100),
                    price=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["active", "inactive"]),
                    provider=f"Sample {i+1}",
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Service records created'))

        if Appointment.objects.count() == 0:
            for i in range(10):
                Appointment.objects.create(
                    client_name=f"Sample Appointment {i+1}",
                    client_email=f"demo{i+1}@example.com",
                    service_name=f"Sample Appointment {i+1}",
                    provider=f"Sample {i+1}",
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    time_slot=f"Sample {i+1}",
                    status=random.choice(["booked", "confirmed", "completed", "cancelled", "no_show"]),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Appointment records created'))

        if Client.objects.count() == 0:
            for i in range(10):
                Client.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    total_bookings=random.randint(1, 100),
                    total_spent=round(random.uniform(1000, 50000), 2),
                    last_visit=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["active", "inactive"]),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Client records created'))
