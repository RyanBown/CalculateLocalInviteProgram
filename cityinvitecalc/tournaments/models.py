from django.db import models

# Create your models here.
from django.contrib import admin

class EventType(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    event_type = models.CharField(max_length=15)

class Tournament(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()

class Player(models.Model):
    pokemon_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_year = models.IntegerField()
    division = models.CharField(max_length=3)

    @property
    def player_name(self):
        return self.last_name + ', ' +  self.first_name 
    
    @property
    @admin.display(
        ordering="last_name",
        description="Full name of the person",
        boolean=False,
    )
    def full_name(self):
        return self.first_name + " " + self.last_name

class TournamentDetail(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    round = models.IntegerField()
    table_number = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=1)

class Standing(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    division = models.CharField(max_length=3)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    placement = models.IntegerField()

class ChampionshipPoint(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    highest_place = models.IntegerField()
    lowest_place = models.IntegerField()
    points = models.IntegerField()
    kicker = models.IntegerField()


class FileRun(models.Model):
    file_name = models.CharField(max_length=200)