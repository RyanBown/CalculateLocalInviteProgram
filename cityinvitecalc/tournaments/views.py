from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tournament, TournamentDetail, Player, FileRun
from .forms import PlayerForm

from django.http import HttpResponseRedirect
# Create your city here.

def HomeView(request):
    return render(request, 'Home.html')

def TournamentView(request):
    all_tournaments = Tournament.objects.all()
    return render(request, 'ListTournaments.html', context= {'tournaments':all_tournaments})

def TournamentDetailView(request, tournament_id):
    print('tourny_id\n\t',tournament_id)
    this_tournament = TournamentDetail.objects.filter(tournament_id=tournament_id).values('id', 'round', 'table_number', 'result', 'player_id', 'player_id__first_name','player_id__last_name' ) .order_by('round', 'table_number')
    print(this_tournament)
    return render(request, 'TournamentDetail.html', context= {'this_tournament':this_tournament})

def ListPlayersView(request, msg = []):

    players = Player.objects.all().order_by('-division__sort_order', 'last_name', 'first_name')

    return render(request, 'ListPlayers.html', context={'players':players, 'messages':msg})

def PlayerView(request, player_id):

    player = Player.objects.get(pokemon_id = player_id)
    return render(request, 'Player.html', context={'player':player})

def EditPlayerView(request, player_id):
    if Player.objects.filter(pokemon_id = player_id).exists():
        player = Player.objects.get(pokemon_id = player_id)
    else:
        return HttpResponseRedirect("Player Does Not Exist")
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            msg = messages.add_message(request, messages.INFO, "Save Successful")
            return ListPlayersView(request, msg )
    else:
        form = PlayerForm(instance=player)

    return render(request, "EditPlayer.html", {"form": form})


def TdfView(request):
    file_ran = FileRun.objects.all()
    return render(request, 'ViewAllTdf.html', content_type={'tdf_files':file_ran})

def ModifyTdfView(request, file_id):
    file_path = FileRun.objects.get(id=file_id)
    return render(request, 'ModifyTdf.html', content_type={'file_path':file_path} )
