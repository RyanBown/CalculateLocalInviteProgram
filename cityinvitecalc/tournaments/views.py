from django.shortcuts import render
from .models import Tournament, TournamentDetail, Player, FileRun


# Create your city here.



def TournamentView(request):
    all_tournaments = Tournament.objects.all()
    return render(request, 'ListTournaments.html', context= {'tournaments':all_tournaments})

def TournamentDetailView(request, tournament_id):
    print('tourny_id\n\t',tournament_id)
    this_tournament = TournamentDetail.objects.filter(tournament_id=tournament_id).values('id', 'round', 'table_number', 'result', 'player_id', 'player_id__first_name','player_id__last_name' ) .order_by('round', 'table_number')
    print(this_tournament)
    return render(request, 'TournamentDetail.html', context= {'this_tournament':this_tournament})


def PlayerView(request, player_id):
    player = Player.objects.filter(pokemon_id = player_id)
    return render(request, 'Player.html', context={'player':player})


def TdfView(request):
    file_ran = FileRun.objects.all()
    return render(request, 'ViewAllTdf.html', content_type={'tdf_files':file_ran})

def ModifyTdfView(request, file_id):
    file_path = FileRun.objects.get(id=file_id)
    return render(request, 'ModifyTdf.html', content_type={'file_path':file_path} )
