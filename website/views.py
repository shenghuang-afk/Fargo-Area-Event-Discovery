from sched import Event
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from website.models import Event
from django.utils import timezone


# Create your views here.
# website/views.py
from django.utils import timezone

def event_list(request):
    events = Event.objects.filter(is_approved=True).order_by('event_date')

    category = request.GET.get('category')
    if category:
        events = events.filter(event_category__icontains=category)

    if request.GET.get('upcoming') == 'true':
        events = events.filter(event_date__gte=timezone.now())

    return render(request, 'website/event_list.html', {'events': events})

def event_detail(request, pk):
    # event = get_object_or_404(Event, pk=pk)
    # return render(request, 'website/event_detail.html', {'event': event})
    return render(request, 'website/event_detail.html')

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
            return redirect('user_events', user_id=request.user.id)
        else:
            return render(request, 'addEvent.html')
    else:
        return redirect('login')
    
# View for deleting an event
def delete_event(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=event_id, event_owner=request.user)
        event.delete()
        return redirect('user_events', user_id=request.user.id)
    else:
        return redirect('login')
    
#View for updating events
def update_event(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=event_id, event_owner=request.user)
        if request.method == 'POST':
            # Handle form submission
            data = request.POST
            event.event_name = data.get('event_name')
            event.event_date = data.get('event_date')
            event.event_location = data.get('event_location')
            event.event_category = data.get('event_category')
            event.event_description = data.get('event_description')
            event.save()
            return redirect('user_events', user_id=request.user.id)
        else:
            # Display form with existing event data
            context = {'event': event}
            return render(request, 'updateEvent.html', context)
    else:
        return redirect('login')
