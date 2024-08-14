from django.shortcuts import render
from django.urls import path
from .models import sense_data
from .serializers import SenseDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

# Define the index view
def index(request):
    return render(request, 'myapp/index.html')

# API views
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

class SenseDataCreate(CreateAPIView):
    queryset = sense_data.objects.all()
    serializer_class = SenseDataSerializer