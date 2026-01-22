import sqlite3
import pandas as pd


def SelectData(select_statement):
    with sqlite3.connect("./cityinvitecalc/TournamentData.db") as conn:
        df = pd.read_sql_query(select_statement, conn)
        return df
        

def RunData():
    select_statement = '''
select
	RANK() over (order by total_points desc, match_points desc ) as ranking,
	first_name || ' ' || 
    CASE 
        WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name and division_id = '{0}' AND substr(n2.last_name, 1, 1) = substr(n1.last_name, 1, 1)) = 1 
			THEN substr(n1.last_name, 1, 1) || '.'
		WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name and division_id = '{0}'  AND substr(n2.last_name, 1, 2) = substr(n1.last_name, 1, 2)) = 1 
			THEN substr(n1.last_name, 1, 2) || '.'
		WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name AND division_id = '{0}' and substr(n2.last_name, 1, 3) = substr(n1.last_name, 1, 3)) = 1 
			THEN substr(n1.last_name, 1, 3) || '.'
		WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name AND division_id = '{0}' and substr(n2.last_name, 1, 4) = substr(n1.last_name, 1, 4)) = 1 
			THEN substr(n1.last_name, 1, 4) || '.'
		WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name AND division_id = '{0}' and substr(n2.last_name, 1, 5) = substr(n1.last_name, 1, 5)) = 1 
			THEN substr(n1.last_name, 1, 5) || '.'
		WHEN (SELECT COUNT(*) FROM tournaments_player n2 WHERE n2.first_name = n1.first_name AND division_id = '{0}' and substr(n2.last_name, 1, 6) = substr(n1.last_name, 1, 6)) = 1 
			THEN substr(n1.last_name, 1, 6) || '.'
        ELSE substr(n1.last_name, 1, 7) || case when length(last_name) > 7 then  '.' else '' end
    END  AS [Name],
    total_points as [Total CP],
    match_points as [Total Match Points],
    first_name,
    last_name,
    player_id
from (
    select      
	    p.pokemon_id,
	    sum(case when td.result ='W' then 3 when td.result= 'T' then 1 else 0 end) as match_points
    from 
	    tournaments_tournamentdetail td
	    join tournaments_player  p
		    on td.player_id = p.pokemon_id
    group by
	    p.pokemon_id
) pmp
join (
    select 
        s.player_id,
        sum(cs.points) as total_points

    from 
        tournaments_standing  s
        join tournaments_tournament t   
            ON s.tournament_id = t.id
        join tournaments_championshippoint cs
            on  s.placement >= cs.highest_place
            and s.placement <= cs.lowest_place
            and cs.kicker <= (select count(*) from tournaments_standing ts where ts.tournament_id = s.tournament_id and ts.division = '{0}'  )
            and t.event_type_id = cs.event_type_id 
        join tournaments_player p 
            on p.pokemon_id = s.player_id
    where
        p.division_id = '{0}'
    group by 
        p.division_id,
        s.player_id

) pcp 
    on pmp.pokemon_id = pcp.player_id
join 
	tournaments_player n1
		on pcp.player_id = n1.pokemon_id
order by 
	ranking
'''

    select_tournaments_in_system = '''
    select 
        event_name as [Event Name],
        event_date as [Event Date]
    from tournaments_tournament 
    order by 
        event_date desc
'''




    data_sheets = []


    for division in ['JR', 'SR', 'MA']:
        formatted_select_statement = select_statement.format(division)
        get_data = SelectData(formatted_select_statement)
    
        data = {division:get_data}
        data_sheets.append(data)

    file_name = 'Leaderboard.xlsx'
    with pd.ExcelWriter(file_name) as writer:

        ##headers = ['player_id', 'first_name', 'Last Name', 'Standing', 'Total_points']
        for division in data_sheets:
            key = list(division.keys())[0]
            standings = division[key]
            standings.to_excel(writer, sheet_name=key, index=False)

        tournament_data = SelectData(select_tournaments_in_system)

        tournament_data.to_excel(writer, sheet_name='events',index=False)


if __name__ == '__main__':
    RunData()