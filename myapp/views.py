from django.shortcuts import render
from django.urls import path
from .models import sense_data
from myapp import views



#define the index 
def index(request):
    return render(request, 'myapp/index.html')

    
# Create your views here.

# create the api view for the sense data using the serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import sense_data
from .serializers import SenseDataSerializer

from myapp.models import sense_data

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

