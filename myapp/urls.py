from django.urls import path
from .views import SenseDataList
from myapp.views import views
urlpatterns = [
    path('', views.index, name='index'),
    path('sense-data/', views.sense_data, name='sense-data-list'),
    path('sense-data-api/', SenseDataList.as_view(), name='sensor-data-list'),
    path('api/sense_data/create/', views.SenseDataCreate.as_view(), name='sense_data_create'),
]