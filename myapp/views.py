from django.shortcuts import render
from rest_framework import generics
from .models import TemperatureReading
from .serializer import TemperatureReadingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# List view for temperature readings
class TemperatureReadingList(generics.ListAPIView):
    queryset = TemperatureReading.objects.all()
    serializer_class = TemperatureReadingSerializer

# Detail view for a specific temperature reading
class TemperatureReadingDetail(generics.RetrieveAPIView):
    queryset = TemperatureReading.objects.all()
    serializer_class = TemperatureReadingSerializer

# Create new temperature reading
class TemperatureCreateAPIView(generics.CreateAPIView):
    queryset = TemperatureReading.objects.all()
    serializer_class = TemperatureReadingSerializer

# Retrieve the latest temperature reading
class LatestTemperatureAPIView(APIView):
    def get(self, request):
        latest_temperature = TemperatureReading.objects.latest('id')
        serializer = TemperatureReadingSerializer(latest_temperature)
        return Response(serializer.data)

# Function-based view for handling both POST and GET requests
@api_view(['POST', 'GET'])
def record_data(request):
    if request.method == 'POST':
        serializer = TemperatureReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        data = TemperatureReading.objects.all().order_by('-timestamp')[:10]
        response_data = [
            {
                "temperature": entry.temperature,
                "humidity": entry.humidity,
                "timestamp": entry.timestamp,
            }
            for entry in data
        ]
        return Response({"data": response_data}, status=status.HTTP_200_OK)

# Render the temperature monitor page
def temperature_monitor(request):
    return render(request, 'myapp/home.html')

relay_state = False  # Initially, relay is OFF


@csrf_exempt
def relay_control_view(request):
    global relay_state

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command', '').strip().lower()  # Get command input

            if command == "on":
                relay_state = True
                
                return JsonResponse({'message': 'Relay turned ON', 'relay_state': 'true'}, status=200)
            elif command == "off":
                relay_state = False
                # Add code here to physically turn the relay OFF
                return JsonResponse({'message': 'Relay turned OFF', 'relay_state': 'false'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid command. Use "on" or "off".'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'GET':
        return JsonResponse({'relay_state': 'true' if relay_state else 'false'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_relay_status(request):
    """
    This view returns the current relay status in JSON format.
    It responds with either "true" or "false" depending on the state.
    """
    global relay_state

    # Return relay status as JSON
    return JsonResponse({'relay_state': relay_state})
