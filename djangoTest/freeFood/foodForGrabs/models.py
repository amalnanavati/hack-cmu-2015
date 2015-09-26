from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    when = models.DateTimeField('time of the event')
    where = models.CharField('location of the event', max_length=200)
    who = models.CharField('group that is hosting the event', max_length=200)
    what = models.TextField('description of the event')
    def __unicode__(self):
        return self.who+" "+str(self.when)
    def is_upcoming(self):
        return self.when >= timezone.now()
