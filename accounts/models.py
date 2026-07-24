from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
   #creating user
   #asks for both names
   def create_user(self,first_name,last_name,username,email,password=None):
       if not email:
           raise ValueError("Users must have an email address")
       
       if not username:
           raise ValueError("Users must have an username")
       
       
       user=self.model(
           email=self.normalize_email(email),
           first_name=first_name,
           last_name=last_name,
           username=username,
       )
       #set password used to encode the password
       user.set_password(password)
       user.save(using=self._db)
       return user
   def create_superuser(self,first_name,last_name,username,email,password):
       user=self.create_user(
           email=self.normalize_email(email),
           first_name=first_name,
           last_name=last_name,
           username=username,
           password=password
       )
       user.is_admin=True
       user.is_active=True
       user.is_staff=True
       user.is_superadmin=True
       user.save(using=self._db)
       return user

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE=(
        (VENDOR, 'Restaurant'),
        (CUSTOMER,'Customer')
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=50)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    
    #required fields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    
    #Authentication
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    objects=UserManager()
    
    def __str__(self):
         return self.email
    
    def has_perm(self,perm,obj=None):
         return self.is_admin
    
    def has_module_perms(self,add_label):
         return True
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
            return user_role     

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='users/cover_photos',blank=True,null=True)
    address =models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=15,blank=True,null=True)
    state=models.CharField(max_length=15,blank=True,null=True)
    city=models.CharField(max_length=15,blank=True,null=True)
    pin_code=models.CharField(max_length=6,blank=True,null=True)
    latitude=models.CharField(max_length=20,blank=True,null=True)
    longitude=models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.user.email
