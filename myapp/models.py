from django.db import models

class sense_data (models.Model):
    temperature = models.CharField(max_length= 30)
    humidity = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.temperature}C, {self.humidity}% at {self.time}"
    
    