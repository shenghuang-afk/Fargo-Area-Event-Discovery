from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Event

def home(request):
    events = Event.objects.all()

    return render(request, 'website/home.html', {
        'events': events
    })

#Admin dashboard view with superuser access control
def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url='/admin/login/')
def admin_dashboard(request):
    events = Event.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')
    area = request.GET.get('area')

    if search:
        events = events.filter(name__icontains=search)
    if category:
        events = events.filter(category__icontains=category)
    if area:
        events = events.filter(area__icontains=area)
    return render(request, 'website/admin_dashboard.html', {
        'events': events
    })

@user_passes_test(superuser_required, login_url='/admin/login/')
def update_event_status(request, event_id, status):
    event = get_object_or_404(Event, id=event_id)
    event.status = status
    event.save()
    return redirect('admin_dashboard')
#Admin dashboard view with superuser access control