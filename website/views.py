from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Event
from django.contrib.auth.forms import UserCreationForm

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
def update_event_status(request, pk, status):
    event = get_object_or_404(Event, id=pk)
    event.status = status
    event.save()
    return redirect('admin_dashboard')
#Admin dashboard view with superuser access control
from website.models import Event


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
            return redirect("login")

    return render(request, "website/login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

# Create your views here.

#All this may change when we come together and decide on the final structure of the events page
# View for all events in the database
def events(request):
    event_list = Event.objects.all()
    event_dict = {'events' : event_list}
    return render(request, 'events.html', event_dict)

# View for all events that current user created
def user_events(request, user_id):
    if request.user.is_authenticated:
        user_event_list = Event.objects.filter(event_owner=user_id)
        user_event_dict = {'events': user_event_list}
        return render(request, 'user_events.html', user_event_dict)
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
            
            # Create a new event instance
            new_event = Event(
                event_name=event_name,
                event_date=event_date,
                event_location=event_location,
                event_category=event_category,
                event_description=event_description,
                event_owner=request.user
            )
            new_event.save()
            # return redirect('user_events', user_id=request.user.id)
            return redirect('home')
        else:
            return render(request, 'website/addEvent.html')
    else:
        return redirect('login')
    
# View for deleting an event
def delete_event(request, pk):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=pk, event_owner=request.user)
        event.delete()
        # return redirect('user_events', user_id=request.user.id)
        return redirect('home')
    else:
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
            event.event_location = data.get('event_location')
            event.event_category = data.get('event_category')
            event.event_description = data.get('event_description')
            event.save()
            messages.success(request, "Event updated successfully.")
            return redirect('home')
        else:
            # Display form with existing event data
            context = {'event': event}
            return render(request, 'website/updateEvent.html', context)
    else:
        return redirect('login')
