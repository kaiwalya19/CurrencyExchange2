
from django.urls import path
from mycurrency import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/currency/', views.CurrencyListCreateView.as_view(), name='currency-list-create'),
    path('api/currency/<int:pk>/', views.CurrencyRetrieveUpdateDestroyView.as_view(), name='currency-detail'),
    path('api/exchange-rate/', views.ExchangeRateAPIView.as_view(), name='exchange-rate-list'),  # Updated line
    path('api/convert/', views.CurrencyConvertView.as_view(), name='currency-convert'),
]
    