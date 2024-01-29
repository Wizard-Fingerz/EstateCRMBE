from django.db import models
from user.models import *

# Create your models here.

FOLLOW_UP_MEANS = (
    ('WhatsApp', 'whatsApp'),
    ('Phone Call', 'phone call'),
    ('Email', 'email'),
)

class Property(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length = 250,)
    value = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    other_property_type = models.CharField(max_length=250)
    media1 = models.FileField(upload_to='property_media')
    media2 = models.FileField(upload_to='property_media')
    media3 = models.FileField(upload_to='property_media')
    media4 = models.FileField(upload_to='property_media')


class FollowUpReport(models.Model):
    prospect = models.ForeignKey('Prospect', on_delete = models.CASCADE)
    property = models.ForeignKey(Property, on_delete = models.CASCADE)
    followup_means = models.CharField(max_length = 250, choices=FOLLOW_UP_MEANS, blank=True, null=True)
    other_means = models.CharField(max_length = 250)
    description = models.TextField()
    media = models.FileField(upload_to="report_media")
    remark = models.CharField(max_length = 250)
    action_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()


class ReportFeedBack(models.Model):
    report = models.ForeignKey(FollowUpReport, on_delete = models.CASCADE)


class Prospect(models.Model):
    prefix = models.CharField(max_length = 250)
    full_name = models.CharField(max_length = 250)
    address = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 250)
    phone_number = models.BigIntegerField()
    whatsapp = models.BigIntegerField()
    status = models.CharField(max_length = 250, blank = True, null = True)
    property = models.ForeignKey(Property, related_name = 'Property', on_delete = models.CASCADE)
    follow_up_marketer = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    