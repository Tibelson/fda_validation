from django.urls import path
from .views import ProductVerifyView

urlpatterns = [
    path('verify/', ProductVerifyView.as_view(), name='product-verify'),
]
