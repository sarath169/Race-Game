from django.urls import path
from . import views

urlpatterns = [
    path('getwords/', views.GetStackViewWords.as_view(), name = 'get_words'),
]
