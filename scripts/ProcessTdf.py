import xml
import os

import xml.etree.ElementTree as ET
import xmltodict
import json
import fiscalyear
from datetime import datetime as dt


#Birth year start at 1900
MA_START = 1900

## take the current FY and minus this to get age division
MA_END = 16
SR_START = 15
SR_END = 12
JR_START = 11
JR_END = 5



fiscalyear.setup_fiscal_calendar(start_month=7)




def merge_pods(pods):
    pod_one = pods[0]
    for pod in pods[1:]:
        pod_one.update(pod)
    return pod_one

def CalculateDivision(birthyear, event_date = dt.now() ):
    birth_year = int(birthyear)
    pokemon_year = fiscalyear.FiscalYear(event_date).fiscal_year
    ma = [MA_START, pokemon_year - MA_END]
    sr = [pokemon_year -SR_START,pokemon_year-SR_END]
    jr = [pokemon_year - JR_START,pokemon_year-JR_END]

    age_divisions = {
        'MA': ma,
        'SR': sr,
        'JR':jr
    }

    for division in age_divisions:
        start_year, end_year = age_divisions[division]
        start_year = int(start_year)
        end_year = int(end_year)
        if birth_year >= start_year and birth_year <= end_year:
            return division



def process_players_section(player_dict_list):
    all_players = {}
    players_dict = player_dict_list['player']
    for player in players_dict:
        pid = player['@userid']
        birth_year = player['birthdate'].split('/')[-1]
        division = CalculateDivision(birth_year)


        player_info = {
            'first_name':player['firstname'],
            'last_name':player['lastname'],
            'birth_year':birth_year,
            'division': division
        }

        all_players[pid] = player_info
    return all_players

def process_match(match):
    match_outcomes_list = []
    winner = match['@outcome']
    table_number = match['tablenumber']
    if winner == '8': ## Late
        match_outcome = {'tblnum':table_number, 'player':match['player']['@userid'], 'Result': 'L' }
        return match_outcome
        

    if winner == '5': ## Bye?
        match_outcome = {'tblnum':table_number, 'player':match['player']['@userid'], 'Result': 'W' }
        return match_outcome
        
    player_one = match['player1']['@userid']
    player_two = match['player2']['@userid']

                
    if winner == '1':
        match_outcome_player_one = {'tblnum':table_number, 'player':player_one, 'Result': 'W' }
        match_outcome_player_two = {'tblnum':table_number, 'player':player_two, 'Result': 'L' }

        return [match_outcome_player_one, match_outcome_player_two]
    if winner == '2':
        match_outcome_player_two = {'tblnum':table_number, 'player':player_two, 'Result': 'W' }
        match_outcome_player_one = {'tblnum':table_number, 'player':player_one, 'Result': 'L' }

        return [match_outcome_player_one, match_outcome_player_two]
    if winner == '3':
        match_outcome_player_two = {'tblnum':table_number, 'player':player_two, 'Result': 'T' }
        match_outcome_player_one = {'tblnum':table_number, 'player':player_one, 'Result': 'T' }

        return [match_outcome_player_one, match_outcome_player_two]
    
    if winner == '10': ##DGL
        match_outcome_player_two = {'tblnum':table_number, 'player':player_two, 'Result': 'L' }
        match_outcome_player_one = {'tblnum':table_number, 'player':player_one, 'Result': 'L' }
        return [match_outcome_player_one, match_outcome_player_two]

    return match_outcomes_list



def process_match_list(match_list):
    match_outcomes_list = []
    ##match_outcomes_list.append({'round_type', round_type})
    if type(match_list) == dict:
        match_result = process_match(match_list)
        if type(match_result) == list:
            player_one_result, player_two_result = match_result
            match_outcomes_list.append(player_one_result)
            match_outcomes_list.append(player_two_result)
        else:
            match_outcomes_list.append(match_result)
    else:
        for match in match_list:
            match_result = process_match(match)
            if type(match_result) == list:
                player_one_result, player_two_result = match_result
                match_outcomes_list.append(player_one_result)
                match_outcomes_list.append(player_two_result)
            else:
                match_outcomes_list.append(match_result)
    return match_outcomes_list



def process_pod(pod):
    rounds_results = {}

    for key in pod:
        if key in ['@category', '@stage' ]:
            continue
        ##print('Key\n\t', key)
        ##print('value\n\t\t', pods_dict[key])
        if key == 'poddata':
            continue
        if key == 'subgroups':
            continue
        if key == 'rounds':
            rounds = pod[key]
            round_list = rounds['round']
            for round in round_list:
                round_number = round['@number']
                ## round_type = round['@type'] ## this is for if it is Swiss, Single Elim, or whatever
                match_list = round['matches']['match']
                match_outcomes_list = []

                if type(round) == list:
                    for matches in match_list:
                        this_round = process_match_list(matches)
                        for round in this_round:
                            match_outcomes_list.append(this_round)
                else:
                    match_outcomes_list = process_match_list(match_list)



                    ##print(match)
                rounds_results[round_number] = match_outcomes_list
            ##print(rounds_results)
            ##for round in rounds_results:
            ##    print('round\n\t',round)
            ##    print('\tmatches\n\t\t', rounds_results[round])
    return rounds_results

def process_pods_section(pods_dict):
    rounds_results = {}
    pods_info = pods_dict['pod']
    ##category = pods_info['@category']
    ##stage = pods_info['@stage']
    pod_count = len(pods_info)
    if pod_count > 1 and type(pods_info) == list:
        pods_result = []
        for pod in pods_info:
            pods_result.append(process_pod(pod))
        return pods_result
        ##rounds_results = merge_pods(pods_result)
        ### going have to see how to do this
    else:
        rounds_results = process_pod(pods_info)


    return rounds_results


def clean_player_standings(standings_list):
    final_standings = {}
    if len(standings_list) == 0:
        return final_standings

    if '@place' in standings_list:
        place = standings_list['@place']
        pid = standings_list['@id']
        final_standings[place] = pid
        return final_standings
    for result in standings_list:
        place = result['@place']
        pid = result['@id']
        final_standings[place] = pid
    return final_standings

def process_standings_section(standings_dict):
    final_standings = {}
    standings_list = standings_dict['pod']
    for standing in standings_list:
        category = standing['@category']
        if category == '2':
            category = 'MA'
        if category == '1':
            category = 'SR'
        if category == '0':
            category = 'JR'
        if '@type' in standing:
            if standing['@type'] == 'finished':
                if 'player' in standing:
                    final_standings[category] = clean_player_standings(standing['player']) 
    return final_standings

def process_finaloptions_section(data_dict):
    divisions = data_dict['categorycut']
    return divisions




## Generate File

def GetDataFromTdf(file_path):

    json_data = ''
    with open(file_path) as f:
        o = xmltodict.parse(f.read())
        str_data = json.dumps(o)
        json_data = json.loads(str_data)



    tournament_data = {}

    player_data = {}

    pod_data = {}

    standings_data = {}

    event_id = ''

    tournament_date = ''

    for tournament in json_data:
        for detail in json_data[tournament]:

            if detail == '@mode':
                tournament_type = json_data[tournament][detail]
                if tournament_type == 'LEAGUECHALLENGE':
                    tournament_type = 'CHA'
                if tournament_type == 'TCG1DAY':
                    tournament_type = 'CUP'
                tournament_data['type'] = tournament_type
                continue

            tournament_detail = json_data[tournament][detail]

            if detail == 'data':
                event_id = tournament_detail['id']
                tournament_data['id'] = tournament_detail['id']
                tournament_data['name'] = tournament_detail['name']
                tournament_data['date'] = tournament_detail['startdate']
                tournament_date = tournament_detail['startdate']


            if detail == 'players':
                player_data = process_players_section(tournament_detail)

            if detail == 'pods':
                pod_data = process_pods_section(tournament_detail)

            if detail == 'standings':
                standings_data = process_standings_section(tournament_detail)
                continue


            if detail == 'finalsoptions':
                continue
                ##process_finaloptions_section(tournament_detail)
    return [tournament_data, player_data, pod_data,standings_data, event_id ]
