from sched import Event
from urllib import request
from django.shortcuts import get_object_or_404, render
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
    # event = get_object_or_404(Event, pk=pk)
    # return render(request, 'website/event_detail.html', {'event': event})
    return render(request, 'website/event_detail.html')