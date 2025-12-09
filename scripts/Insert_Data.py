import sqlite3

from thefuzz import fuzz

## cityinvitecalc\TournamentData.db

def InsertData(insert_statement, variables):
    with sqlite3.connect("./cityinvitecalc/TournamentData.db") as conn:
        cur = conn.cursor()
        cur.execute(insert_statement, variables)
        conn.commit()

def SelectData(select_statement):
    with sqlite3.connect("./cityinvitecalc/TournamentData.db") as conn:
        cur = conn.cursor()
        res = cur.execute(select_statement)
        return res
        

def HasFileBeenRan(file):
    select_statement = '''
    select 
        count(*)
    from
        tournaments_filerun
    where
        file_name = 
    '''

    select_statement = select_statement + "'" + file  +  "'"
    row_count = SelectData(select_statement).fetchone()[0]

    if row_count > 0:
        return True
    else:
        return False



def InsertTournamentData(tournament_data):
    event_type = tournament_data['type']
    event_id = tournament_data['id']
    event_name = tournament_data['name']
    event_date = tournament_data['date']

    insert_tournament = '''
    insert into tournaments_tournament
    (id,event_name,event_date,event_type_id)
    values (
        ?, ?, ?, ? 
    )
'''
    event_vars = [ event_id, event_name, event_date, event_type ]
    InsertData(insert_tournament, event_vars)

def InsertPlayersData(player_data):
    select_players = '''select 
    pokemon_id, 
    first_name, 
    last_name, 
    division 
    from tournaments_player
'''
    players_in_system = SelectData(select_players).fetchall()
    player_id_in_system = [player[0]  for player in players_in_system ]

    insert_player = '''
    insert into tournaments_player
    (pokemon_id, first_name, last_name, birth_year, division )
    values (
    ?, ?, ?, ?, ?
    )
'''
    for player_id in player_data:
        player = player_data[player_id]
        first_name = player['first_name']
        last_name = player['last_name']
        birth_year = player['birth_year']
        division = player['division']
        player_vars = [ player_id, first_name, last_name, birth_year, division ]

        for player_id_in_system in players_in_system:
            if fuzz.ratio(player_id_in_system, player_id) > 90:
                print('player id\n\t', 'new', player, first_name, last_name, '\n\t', player_id)
                continue


        try:
            InsertData( insert_player, player_vars )
        except Exception as e:
            print('Player', player_id, 'had error')
            if str(e) == 'UNIQUE constraint failed: tournaments_player.pokemon_id':
                print('\tPlayer', player_id, ' already in the system')
            else:
                print('\t',e)

def InsertPodData(pod_data, event_id):
    insert_pod = '''
    insert into tournaments_tournamentdetail
    ( round, table_number, result, player_id, tournament_id
    )
    values (
        ?,?,?,?,?
    )

'''
    for round in pod_data:
        for match in pod_data[round]:
            ##print(match)
            tbl_num = match['tblnum']
            player_id = match['player']
            result = match['Result']  
            pod_vars = [round, tbl_num, result, player_id, event_id]
            InsertData(insert_pod, pod_vars)

def InsertStandingsData(standings_data, event_id):
    insert_standings = '''
    insert into tournaments_standing
    (division, placement, player_id, tournament_id )
    values (
        ?,?,?,?
    )
    '''
    for division in standings_data:
        standings_list = standings_data[division]
        for placement in standings_list:
            player = standings_list[placement]
            standing_vars = [division, placement, player, event_id ]
            InsertData(insert_standings, standing_vars)


def InsertFileData(file):
    insert_file = '''
    insert into tournaments_filerun
    (file_name)
    values (
        ?
    )
    '''

    InsertData(insert_file, file)