from django.db import models
from user.models import *

# Create your models here.

FOLLOW_UP_MEANS = (
    ('WhatsApp', 'whatsApp'),
    ('Phone Call', 'phone call'),
    ('Email', 'email'),
    ('Physical Visitation', 'physical visitation'),
    ('Chat', 'chat'),
    ('Others', 'others'),
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
    additional_comment = models.TextField()
    media = models.FileField(upload_to="report_media")
    remark = models.CharField(max_length = 250)
    customer_feedback = models.CharField(max_length = 250)
    action_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    hour_spent = models.TimeField()
    followup_time = models.TimeField()


class ReportFeedBack(models.Model):
    report = models.ForeignKey(FollowUpReport, on_delete = models.CASCADE)

STATUS_CHOICES = [
        ('propect', 'Propect'),
        ('open', 'Open'),
        ('working', 'Working'),
        ('meeting_set', 'Meeting Set'),
        ('opportunity', 'Opportunity'),
        ('opportunity_lost', 'Opportunity Lost'),
        ('customer', 'Customer'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('in_progress', 'In Progress'),
        ('under_review', 'Under Review'),
        ('pending_approval', 'Pending Approval'),
        ('awaiting_feedback', 'Awaiting Feedback'),
        ('contact_attempted', 'Contact Attempted'),
        ('contract_sent', 'Contract Sent'),
        ('negotiation', 'Negotiation'),
        ('contract_signed', 'Contract Signed'),
        ('pending_payment', 'Pending Payment'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
        ('pending_verification', 'Pending Verification'),
        ('scheduled_for_visit', 'Scheduled for Visit'),
        ('follow_up_needed', 'Follow-up Needed'),
        ('others', 'Others'),
        # Add more choices as needed
    ]

AREA_OF_INTEREST = [
    ('Land','LAND'),
    ('Housing','HOUSING'),
    ('membership','MEMBERSHIP'),
    ('partnership','PARTNERSHIP'),
    ('others','OTHERS'),
]

class Prospect(models.Model):
    prefix = models.CharField(max_length = 250)
    full_name = models.CharField(max_length = 250)
    # address = models.ForeignKey('ProspectLocation', on_delete = models.CASCADE)
    address = models.CharField(max_length = 400)
    email = models.EmailField(max_length = 250)
    phone_number = models.BigIntegerField()
    phone_number2 = models.BigIntegerField(blank =True, null = True)
    whatsapp = models.BigIntegerField()
    facebook_username = models.CharField(max_length = 250, null = True, blank = True)
    twitter_username = models.CharField(max_length = 250, null = True, blank = True)
    instagram_username = models.CharField(max_length = 250, null = True, blank = True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='propect',  # Set a default value if needed
        blank=True,
        null=True,
    )
    contact_source = models.CharField(max_length = 250, null = True, blank = True)
    property = models.ForeignKey(Property, related_name = 'Property', on_delete = models.CASCADE)
    follow_up_marketer = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    area_of_interest = models.CharField(
        max_length=20,
        choices=AREA_OF_INTEREST,
        blank=True,
        null=True,
    )
    other_info = models.CharField(max_length = 250)
    planned_commitment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.full_name) or ''


PAYMENT_STATUS = [
    ('completed', 'COMPLETED'),
    ('incompleted', 'INCOMPLETED'),
]    

class Customer(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete = models.CASCADE)
    receipt = models.FileField(upload_to = 'customers_receipt/')
    other_files = models.FileField(upload_to = 'other_customers_files/')
    amount = models.BigIntegerField()
    payment_status = models.CharField(max_length = 250, choices = PAYMENT_STATUS)
    follow_up_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.prospect) or ''

class ProspectLocation(models.Model):
    city = models.CharField(max_length = 250)
    state = models.CharField(max_length = 250)
    
    
    
class PropectSocialHandle(models.Model):
    name = models.CharField(max_length = 250)
    username = models.CharField(max_length =250)

class PropectContactSource(models.Model):
    name = models.CharField(max_length = 250)
    description = models.CharField(max_length =250)