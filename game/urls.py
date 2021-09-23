from django.urls import path
from . import views

urlpatterns = [
    path('getwords/', views.GetStackViewWords.as_view(), name = 'get_words'),
    path('save/', views.SaveGameDetails.as_view(), name= 'save_game' ),
    path('leaderboard/', views.LeaderBoardView.as_view(), name= 'leaderboard'),
    path('stats/', views.UserGameDetails.as_view(), name="user_stats"),
]
