from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(primary_key=True, validators=[MinValueValidator(100000000), MaxValueValidator(999999999999)])
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    dept = models.CharField(max_length=10)


    def __str__(self):
        return self.user.username
