from django.urls import path
from . import views

app="tournaments"
urlpatterns = [
    path('view/', views.TournamentView, name='tournaments-view'),
    path('view/<str:tournament_id>', views.TournamentDetailView, name='tournaments-detail'),
    path('player/<str:player_id>', views.PlayerView, name='tournaments-detail'),
    path('view/tdf/', views.TdfView, name='all-tdf'),
    path('view/tdf/<int:file_id>', views.ModifyTdfView, name='modify-tdf'),
]