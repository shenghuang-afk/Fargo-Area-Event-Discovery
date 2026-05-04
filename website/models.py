from django.db import models
from geopy.geocoders import Nominatim

# Create your models here.
class Event(models.Model):
    categories = [
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('education', 'Education'),
        ('technology', 'Technology'),
        ('entertainment', 'Entertainment'),
        ('food', 'Food'),
        ('business', 'Business'),
        ('charity', 'Charity'),
        ('social', 'Social')
    ]

    # Admin page 
    STATUS_CHOICES = [
        ('review', 'In Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='review')

    def __str__(self):
        return self.event_name
    #Admin page

    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField(null=True, blank=True)
    event_location = models.CharField(max_length=255)
    event_category = models.CharField(max_length=50, choices=categories)
    event_description = models.TextField(default="")

    # is_approved = models.BooleanField(default=False)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    event_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['event_date']

    def save(self, *args, **kwargs):
        if self.event_location and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="event_locator")
            location = geolocator.geocode(self.event_location)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        super().save(*args, **kwargs)

