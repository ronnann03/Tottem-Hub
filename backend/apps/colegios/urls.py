from django.urls import path
from .views import ColegioSearchView

urlpatterns = [
    path('search/', ColegioSearchView.as_view(), name='colegio-search'),
]