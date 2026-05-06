from sched import Event
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime

# Sheng Huang
def home(request):
    events = Event.objects.all()

    return render(request, 'website/home.html', {
        'events': events
    })

#Admin dashboard view with superuser access control
def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url='/admin/login/')
def update_event_status(request, pk):
    event = get_object_or_404(Event, event_id=pk)

    if request.method == "POST":
        event.status = request.POST.get("status")
        
        event.save()
    return redirect('admin_dashboard')

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
def admin_delete_event(request, pk):
    event = get_object_or_404(Event, event_id=pk)
    event.delete()
    messages.success(request, "Event deleted.")
    return redirect('admin_dashboard')
#Admin dashboard view with superuser access control - Sheng Huang

from website.models import Event
from django.utils import timezone


# Evan Fretheim
from django.utils import timezone

def event_list(request):

    events = Event.objects.all().order_by('event_date')

    category = request.GET.get('category')
    if category:
        events = events.filter(event_category__iexact=category)

    query = request.GET.get('search')
    if query:
        events = events.filter(event_name__icontains=query) | events.filter(event_description__icontains=query)

    date_query = request.GET.get('date')
    if date_query:
        try:
            date_query = datetime.strptime(date_query, '%Y-%m-%d').date()
            events = events.filter(event_date__date=date_query)
        except ValueError:
            pass

    return render(request, 'website/event_list.html', {'events': events, 'categories': category})

def event_detail(request, pk):
    
    event = get_object_or_404(Event, pk=pk)
    events = Event.objects.all()
    
    return render(request, 'website/event_detail.html', {'event': event, 'events': events})

# Jaden Dischinger
def login_user(request):
    if request.method == "POST":
        username_var = request.POST["username"]
        password_var = request.POST["password"]

        user = authenticate(username=username_var, password=password_var)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, "website/login.html", {})

    return render(request, "website/login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

# Create your views here.

# Julius Rosalin
def events(request):
    event_list = Event.objects.all()
    event_dict = {'events' : event_list}
    return render(request, 'events.html', event_dict)

def approved_events(request):
    approved_event_list = Event.objects.filter(status='accepted')
    approved_event_dict = {'events': approved_event_list}
    return render(request, 'website/event_list.html', approved_event_dict)

# View for all events that current user created
def user_events(request):
    if request.user.is_authenticated:
        user = request.user
        user_event_list = Event.objects.filter(event_owner=user)
        user_event_dict = {'events': user_event_list}
        return render(request, 'website/userEvents.html', user_event_dict)
    else:
        return redirect('login')
    
# View for creating a new event
def add_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            event_name = data.get('event_name')
            event_date = data.get('event_date')
            event_location = data.get('event_location')
            event_category = data.get('event_category')
            event_description = data.get('event_description')
            event_time = data.get('event_time')
            
            # Create a new event instance
            new_event = Event(
                event_name=event_name,
                event_date=event_date,
                event_time=event_time,
                event_location=event_location,
                event_category=event_category,
                event_description=event_description,
                event_owner=request.user
            )
            new_event.save()
            return redirect('user_events')
        else:
            return render(request, 'website/addEvent.html')
    else:
        messages.error(request, "You need to be logged in to add an event.")
        return redirect('login')
    
# View for deleting an event
def delete_event(request, pk):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, event_id=pk, event_owner=request.user)
        event.delete()
        return redirect('user_events')
    else:
        messages.error(request, "You need to be logged in to delete an event.")
        return redirect('login')
    
#View for updating events
def update_event(request, pk):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, event_id=pk, event_owner=request.user)
        if request.method == 'POST':
            # Handle form submission
            data = request.POST
            event.event_name = data.get('event_name')
            event.event_date = data.get('event_date')
            event.event_time = data.get('event_time')
            event.event_location = data.get('event_location')
            event.event_category = data.get('event_category')
            event.event_description = data.get('event_description')
            event.save()
            messages.success(request, "Event updated successfully.")
            return redirect('user_events')
        else:
            # Display form with existing event data
            context = {'event': event}
            return render(request, 'website/updateEvent.html', context)
    else:
        messages.error(request, "You need to be logged in to update an event.")
        return redirect('login')