from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..myapp.models import sense_data
from ..myapp.serializers import SenseDataSerializer
from myapp import views, api_views
from myapp.models import sense_data


class SenseDataView(APIView):
    def get(self, request):
        data = sense_data.objects.all()
        serializer = SenseDataSerializer(data, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = SenseDataSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
