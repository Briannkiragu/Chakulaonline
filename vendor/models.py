from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification 
from datetime import time, date, datetime

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    userProfile = models.OneToOneField(UserProfile, related_name='userProfile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return self.vendor_name


    def is_open(self):
        #check current day opening hours
        today_date = date.today()
        today = today_date.isoweekday()

        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S") 

        is_open = None
        for hour in current_opening_hours:
            if not hour.is_closed:
                start = str(datetime.strptime(hour.from_hour, "%I:%M:%p").time())
                end = str(datetime.strptime(hour.from_hour, "%I:%M:%p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
            
            else:
                is_open = False
        return is_open

    def save(self, *args, **kwargs):
        origin = None
        if self.pk is not None:
            origin = Vendor.objects.get(pk=self.pk)

        if (
            origin is not None
            and hasattr(origin, 'is_approved')
            and hasattr(self, 'is_approved')
            and origin.is_approved != self.is_approved
        ):
            if self.is_approved is True:
                # send email to vendor that account is approved
                mail_subject = 'Congratulations! Your account has been approved.'
                mail_template = 'accounts/emails/vendor_approved_email.html'
                context = {'user': self.user, 'is_approved': self.is_approved}
                send_notification(mail_subject, mail_template, context)
            else:
                # send email to vendor that account is rejected
                mail_subject = 'Sorry! Your account has been rejected.'
                mail_template = 'accounts/emails/vendor_rejected_email.html'
                context = {'user': self.user, 'is_approved': self.is_approved}
                send_notification(mail_subject, mail_template, context)

        super(Vendor, self).save(*args, **kwargs)


        #bihness hours
DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]
HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]  
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.TimeField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.TimeField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', '-from_hour']
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return f"{self.get_day_display()} - {self.from_hour} to {self.to_hour}"