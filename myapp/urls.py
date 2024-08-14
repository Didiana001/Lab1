
from django.urls import path
from .views import index, SenseDataList, SenseDataCreate

urlpatterns = [
    path('', index, name='index'),  
    path('sense-data/', SenseDataList.as_view(), name='sense-data-list'),  # 
    path('sense-data-api/', SenseDataList.as_view(), name='sensor-data-list'),  
    path('api/sense_data/create/', SenseDataCreate.as_view(), name='sense_data_create'),  #
