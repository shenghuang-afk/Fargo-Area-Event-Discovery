from sched import Event
from django.shortcuts import render
from .models import Event

# Create your views here.
# website/views.py
def event_list(request):
    events = Event.objects.filter(is_approved=True).order_by('event_date')
    
    category_query = request.GET.get('category')
    if category_query:
        events = events.filter(event_category__iexact=category_query)

    return render(request, 'website/event_list.html', {'events': events})

def event_detail(request, pk):
    event = Event.objects.get(Event, pk=pk)
    return render(request, 'website/event_detail.html', {'event': event})