from rest_framework import serializers
from .models import sense_data

class SenseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = sense_data
        fields = '__all__'