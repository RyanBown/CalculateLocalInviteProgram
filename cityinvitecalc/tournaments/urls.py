from django.urls import path
from . import views

app="tournaments"
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('view_tournament/', views.TournamentView, name='tournaments-view'),
    path('view_tournament/<str:tournament_id>', views.TournamentDetailView, name='tournaments-detail'),
    path('view_player/', views.ListPlayersView),
    path('edit_player_in_tournament/<str:tournament_id>/<str:player_id>', views.edit_player_in_tournament, name='edit-player-in-tournament'),
    path('view_player/<str:player_id>', views.PlayerView, name='player'),
    path('edit_player/<str:player_id>', views.EditPlayerView, name='edit-player'),
    path('players', views.ListPlayersView, name='all-players'),
    path('view_tdf/', views.TdfView, name='all-tdf'),
    path('view_tdf/tdf/<int:file_id>', views.ModifyTdfView, name='modify-tdf'),
]