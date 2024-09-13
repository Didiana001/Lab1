from django.db import models

# Model to store sensor data
class sense_data(models.Model):
    temperature = models.CharField(max_length=30)
    humidity = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}% at {self.time}"

# Model to store bulb status changes
class BulbControl(models.Model):
    status = models.CharField(max_length=10)  # 'on' or 'off'
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulb is {self.status} at {self.time}"
