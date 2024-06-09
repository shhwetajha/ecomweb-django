
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('user must have an email')
        if not username:
            raise ValueError('user must have an username')


        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user


class account(AbstractBaseUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100,unique=True)
    phone=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)

    # required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    objects=MyAccountManager()


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email


    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True 

class UserProfile(models.Model):
    user=models.OneToOneField(account,on_delete=models.CASCADE)
    address_line_1=models.CharField(blank=True,max_length=100)
    address_line_2=models.CharField(blank=True,max_length=100)
    state=models.CharField(blank=True,max_length=100)
    city=models.CharField(blank=True,max_length=100,)
    country=models.CharField(blank=True,max_length=100)
    profile_picture=models.ImageField(blank=True,upload_to='userprofile/')


    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'




class Country(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
