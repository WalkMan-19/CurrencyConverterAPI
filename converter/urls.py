from django.urls import path
from converter import views

urlpatterns = [
    path('convert', views.ConverterView.as_view(), name='converter-view'),
]
