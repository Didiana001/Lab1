from django.urls import path
from .views import index, SenseDataList, SenseDataCreate

urlpatterns = [
    path('', index, name='index'),  # Main index view
    path('sense-data/', SenseDataList.as_view(), name='sense-data-list'),  # List view for sense data
    # The following path is redundant since it repeats the same view as the previous one.
    # Consider removing or renaming it based on different functionality.
    # path('sense-data-api/', SenseDataList.as_view(), name='sensor-data-list'),  
    path('api/sense_data/create/', SenseDataCreate.as_view(), name='sense_data_create'),  # API view for creating sense data
]
