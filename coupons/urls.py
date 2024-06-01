from django.urls import path
from .views import search_coupon, apply_coupon

urlpatterns = [
    path('', search_coupon, name='search_coupon'),
    path('apply/', apply_coupon, name='apply_coupon'),
]
