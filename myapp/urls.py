from django.urls import path
from .views import index, SenseDataList, SenseDataCreate, bulb_control  # Import the views

urlpatterns = [
    path('', index, name='index'),  # Main index view
    path('sense-data/', SenseDataList.as_view(), name='sense-data-list'),  
    path('api/sense_data/create/', SenseDataCreate.as_view(), name='sense_data_create'),  # API view for creating sense data
    path('api/bulb_control/', bulb_control, name='bulb_control')  # API for controlling the bulb
]
