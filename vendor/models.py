from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification 

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    userProfile = models.OneToOneField(UserProfile, related_name='userProfile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return self.vendor_name

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