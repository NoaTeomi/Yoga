from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class YogaPose(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='poses/', blank=True, null=True)

    def __str__(self):
        return self.name

class YogaSequence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    poses = models.ManyToManyField(YogaPose, related_name='sequences')
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Duration in minutes

    def __str__(self):
        return f"{self.name} by {self.user.username}"