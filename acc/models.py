from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class Service(models.Model):
    name = models.CharField(max_length=900)
    script = models.TextField(default=None, blank=True)
    slug = models.SlugField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    



class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(
        verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=30, blank=True)
    dob = models.DateField(auto_now=True, blank=True)
    nrc = models.CharField(verbose_name='national registration number', max_length=300, blank=True)
    country = CountryField(blank_label='(select country)', blank=True)
    phone =  PhoneNumberField(blank=True)
    is_staff = models.BooleanField(verbose_name='staff', default=False)
    location = models.CharField(verbose_name='location', max_length=50, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='active', default=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
        
    

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
        

class UserSkill(models.Model):
    worker = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    price = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, default=None)
    cert0 = models.FileField(default=None,upload_to='user/skills/', blank=True)
    cert1 = models.FileField(default=None,upload_to='user/skills/', blank=True)
    cert2 = models.FileField(default=None,upload_to='user/skills/', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'{self.worker} -  {self.service} '
    


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user", default=None)
    service_provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="service_provider", default=None)
    skill = models.ForeignKey(
        UserSkill, on_delete=models.CASCADE, default=None)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            CheckConstraint(check=Q(rate__range=(0, 10)), name='valid_rate'),
            UniqueConstraint(fields=['user', 'skill'], name='rating_once')
        ]


    def __str__(self):
        return f'{self.service_provider} -  {self.rate}'