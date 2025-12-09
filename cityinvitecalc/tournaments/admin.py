from django.contrib import admin

# Register your models here.
from .models import EventType, Tournament, Player, TournamentDetail, Standing, ChampionshipPoint, FileRun

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_type']
    search_fields = ["event_type"]

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_type', 'event_name', 'event_date']
    search_fields = ["event_type", 'event_name']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['pokemon_id', 'first_name', 'last_name', 'birth_year', 'division']
    search_fields = ["pokemon_id", 'first_name', 'last_name', 'division']

@admin.register(TournamentDetail)
class TournamentDetailAdmin(admin.ModelAdmin):
    list_display = ['tournament__id', 'round', 'table_number','player__pokemon_id','player__first_name', 'player__last_name',  'result']
    search_fields = ["tournament__id", 'player__pokemon_id']

@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ['tournament__id', 'division', 'player__first_name', 'player__last_name', 'placement']
    search_fields = ["tournament__id",'division', 'player__pokemon_id']

@admin.register(ChampionshipPoint)
class ChampionshipPointAdmin(admin.ModelAdmin):
    list_display = ['id','event_type__event_type', 'highest_place', 'lowest_place', 'points', 'kicker']


@admin.register(FileRun)
class FileRunAdmin(admin.ModelAdmin):
    list_display = ['id','file_name']