from django.shortcuts import render
from django.urls import path
from .models import sense_data, BulbControl  # Import BulbControl model
from .serializers import SenseDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import requests

ESP32_URL = "http://172.16.60.93:8004/api/bulb_control/"  # Server URL for bulb control

def get_bulb_status():
    try:
        response = requests.get(ESP32_URL)
        if response.status_code == 200:
            return response.json().get("status")  # {"status": "on"}
        return "unknown"
    except requests.ConnectionError:
        return "unknown"

# Function to toggle bulb state via ESP32
def toggle_bulb():
    try:
        response = requests.post(ESP32_URL, json={"toggle": True})
        return response.json().get("status")
    except requests.ConnectionError:
        return "unknown"

# Bulb Control View (for bulb state GET/POST)
@csrf_exempt
def bulb_control(request):
    if request.method == 'POST':
        action = json.loads(request.body).get('action')
        
        if action == "toggle":
            status = toggle_bulb()
            BulbControl.objects.create(status=status, time=datetime.now())  # Record the bulb status change
            return JsonResponse({"status": status})
    
    # Handle the GET request to return the current status
    current_status = get_bulb_status()
    return JsonResponse({"status": current_status})

# Index view to render sensor data
def index(request):
    sensor_data = sense_data.objects.all()
    return render(request, 'myapp/index.html', {'sensor_data': sensor_data})

# API view for listing and creating sensor data
class SenseDataList(APIView):
    def get(self, request):
        sensor_data = sense_data.objects.all()
        serializer = SenseDataSerializer(sensor_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SenseDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for creating sense data
class SenseDataCreate(CreateAPIView):
    queryset = sense_data.objects.all()
    serializer_class = SenseDataSerializer
