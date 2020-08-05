from django.db import models

# Create your models here.
class schedule1(models.Model):
    name = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
