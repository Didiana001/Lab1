from django.db import models

# Model to store temperature and humidity readings
class TemperatureReading(models.Model):
    temperature = models.FloatField()  # Storing temperature as a float value
    humidity = models.FloatField()     # Storing humidity as a float value
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}% at {self.timestamp}"
    
    
    

# Model to store the relay state for the bulb
class RelayState(models.Model):
    ON = 'on'
    OFF = 'off'

    STATUS_CHOICES = [
        (ON, 'On'),
        (OFF, 'Off'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=OFF
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"Relay is {self.get_status_display()} at {self.timestamp}"
