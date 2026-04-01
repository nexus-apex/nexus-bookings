import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Service, Appointment, Client


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['service_count'] = Service.objects.count()
    ctx['service_active'] = Service.objects.filter(status='active').count()
    ctx['service_inactive'] = Service.objects.filter(status='inactive').count()
    ctx['service_total_price'] = Service.objects.aggregate(t=Sum('price'))['t'] or 0
    ctx['appointment_count'] = Appointment.objects.count()
    ctx['appointment_booked'] = Appointment.objects.filter(status='booked').count()
    ctx['appointment_confirmed'] = Appointment.objects.filter(status='confirmed').count()
    ctx['appointment_completed'] = Appointment.objects.filter(status='completed').count()
    ctx['client_count'] = Client.objects.count()
    ctx['client_active'] = Client.objects.filter(status='active').count()
    ctx['client_inactive'] = Client.objects.filter(status='inactive').count()
    ctx['client_total_total_spent'] = Client.objects.aggregate(t=Sum('total_spent'))['t'] or 0
    ctx['recent'] = Service.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def service_list(request):
    qs = Service.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'service_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def service_create(request):
    if request.method == 'POST':
        obj = Service()
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.price = request.POST.get('price') or 0
        obj.status = request.POST.get('status', '')
        obj.provider = request.POST.get('provider', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/services/')
    return render(request, 'service_form.html', {'editing': False})


@login_required
def service_edit(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.category = request.POST.get('category', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.price = request.POST.get('price') or 0
        obj.status = request.POST.get('status', '')
        obj.provider = request.POST.get('provider', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/services/')
    return render(request, 'service_form.html', {'record': obj, 'editing': True})


@login_required
def service_delete(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/services/')


@login_required
def appointment_list(request):
    qs = Appointment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(client_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'appointment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def appointment_create(request):
    if request.method == 'POST':
        obj = Appointment()
        obj.client_name = request.POST.get('client_name', '')
        obj.client_email = request.POST.get('client_email', '')
        obj.service_name = request.POST.get('service_name', '')
        obj.provider = request.POST.get('provider', '')
        obj.date = request.POST.get('date') or None
        obj.time_slot = request.POST.get('time_slot', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/appointments/')
    return render(request, 'appointment_form.html', {'editing': False})


@login_required
def appointment_edit(request, pk):
    obj = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        obj.client_name = request.POST.get('client_name', '')
        obj.client_email = request.POST.get('client_email', '')
        obj.service_name = request.POST.get('service_name', '')
        obj.provider = request.POST.get('provider', '')
        obj.date = request.POST.get('date') or None
        obj.time_slot = request.POST.get('time_slot', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/appointments/')
    return render(request, 'appointment_form.html', {'record': obj, 'editing': True})


@login_required
def appointment_delete(request, pk):
    obj = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/appointments/')


@login_required
def client_list(request):
    qs = Client.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'client_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def client_create(request):
    if request.method == 'POST':
        obj = Client()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.total_bookings = request.POST.get('total_bookings') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.last_visit = request.POST.get('last_visit') or None
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/clients/')
    return render(request, 'client_form.html', {'editing': False})


@login_required
def client_edit(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.total_bookings = request.POST.get('total_bookings') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.last_visit = request.POST.get('last_visit') or None
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/clients/')
    return render(request, 'client_form.html', {'record': obj, 'editing': True})


@login_required
def client_delete(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/clients/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['service_count'] = Service.objects.count()
    data['appointment_count'] = Appointment.objects.count()
    data['client_count'] = Client.objects.count()
    return JsonResponse(data)
