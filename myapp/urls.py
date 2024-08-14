
from django.urls import path
from .views import index, SenseDataList, SenseDataCreate

urlpatterns = [
    path('', index, name='index'),  # Correctly reference the index view
    path('sense-data/', SenseDataList.as_view(), name='sense-data-list'),  # Use SenseDataList for the list view
    path('sense-data-api/', SenseDataList.as_view(), name='sensor-data-list'),  # This appears redundant, consider combining or clarifying their use
    path('api/sense_data/create/', SenseDataCreate.as_view(), name='sense_data_create'),  # Correctly reference SenseDataCreate
]
