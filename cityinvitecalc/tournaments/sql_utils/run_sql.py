from django.db import connection
import os


def get_data(sql_file):
    sql_query = f"./cityinvitecalc/static/sql/{sql_file}"
    with connection.cursor() as cursor:
        sql = ""
        with open(sql_query, "r") as f:
            sql = f.read()
        cursor.execute(sql)
        return cursor.fetchall()



def get_data_for_leaderboard():
    return get_data("get_LeaderboardForDivision.sql")

def get_data_for_tournament():
    return get_data("tournament.sql")

def get_data_for_player():
    return get_data("player.sql")
