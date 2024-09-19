from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
import json
import requests
from datetime import datetime
from .models import sense_data, BulbControl
from .serializers import SenseDataSerializer
import logging

# Constants
ESP32_URL = "http://172.60.61.56:8000/sense-data/create/"  # URL for bulb control API

# Setup logging
logger = logging.getLogger(__name__)

def get_bulb_status():
    try:
        response = requests.get(ESP32_URL)
        if response.status_code == 200:
            return response.json().get("status")
        logger.error(f"Failed to fetch bulb status. Status code: {response.status_code}")
        return "unknown"
    except requests.ConnectionError as e:
        logger.error(f"Connection error while fetching bulb status: {e}")
        return "unknown"

def toggle_bulb():
    try:
        response = requests.post(ESP32_URL, json={"toggle": True})
        if response.status_code == 200:
            return response.json().get("status")
        logger.error(f"Failed to toggle bulb. Status code: {response.status_code}")
        return "unknown"
    except requests.ConnectionError as e:
        logger.error(f"Connection error while toggling bulb: {e}")
        return "unknown"

@csrf_exempt
def bulb_control(request):
    if request.method == 'POST':
        try:
            action = json.loads(request.body).get('action')
            if action == "toggle":
                status = toggle_bulb()
                BulbControl.objects.create(status=status, time=datetime.now())
                return JsonResponse({"status": status})
            else:
                logger.error(f"Invalid action in POST request: {action}")
                return JsonResponse({"error": "Invalid action"}, status=400)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in POST request: {e}")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    # GET request
    current_status = get_bulb_status()
    return JsonResponse({"status": current_status})

class SenseDataCreate(CreateAPIView):
    queryset = sense_data.objects.all()
    serializer_class = SenseDataSerializer

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
        logger.error(f"Invalid sensor data POST request: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Index view to render sensor data
def index(request):
    sensor_data = sense_data.objects.all()
    return render(request, 'myapp/index.html', {'sensor_data': sensor_data})

# New API view to control the ESP32 relay module
class RelayControlView(APIView):
    def put(self, request):
        state = request.data.get('state')
        if state not in ['ON', 'OFF']:
            return Response({"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.put(f"{ESP32_URL}?state={state}")
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed to send PUT request. Status code: {response.status_code}")
                return Response({"error": "Failed to control relay"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.ConnectionError as e:
            logger.error(f"Connection error while sending PUT request: {e}")
            return Response({"error": "Connection error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
