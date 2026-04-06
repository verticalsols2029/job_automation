from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    requires_sponsorship = models.BooleanField(default=False)
    legally_authorized = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="education")
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experience")
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)