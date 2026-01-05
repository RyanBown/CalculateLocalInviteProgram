from django.urls import path
from . import views

app="tournaments"
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('view/', views.TournamentView, name='tournaments-view'),
    path('view/<str:tournament_id>', views.TournamentDetailView, name='tournaments-detail'),
    path('player/<str:player_id>', views.PlayerView, name='player'),
    path('edit_player/<str:player_id>', views.EditPlayerView, name='edit-player'),
    path('players', views.ListPlayersView, name='all-players'),
    path('view/tdf/', views.TdfView, name='all-tdf'),
    path('view/tdf/<int:file_id>', views.ModifyTdfView, name='modify-tdf'),
]