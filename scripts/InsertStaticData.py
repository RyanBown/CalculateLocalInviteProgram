import sqlite3
import sys


def InsertData(insert_statement):
    with sqlite3.connect("./cityinvitecalc/TournamentData.db") as conn:
        cur = conn.cursor()
        cur.execute(insert_statement)
        conn.commit()


def InsertEventTypes():
    insert_eventTypes = '''
    insert into tournaments_eventtype
    (id, event_type) values 
    ( 'CHA', 'Challenge' ),
    ('CUP', 'Cup')
'''
    InsertData(insert_eventTypes)

def InsertChampionshipPoints():
    insert_eventTypes = '''
    insert into tournaments_championshippoint
    ( highest_place, lowest_place, points, kicker, event_type_id)
    values 
    (1, 1, 15, 0, 'CHA' ),
    (2, 2, 12, 4, 'CHA' ),
    (3, 4, 10, 8, 'CHA' ),
    (5, 8, 8, 14, 'CHA' ),
    (9, 16, 6, 25, 'CHA' ),
    (17, 32, 4, 48, 'CHA' ),
    (1, 1, 50, 0, 'CUP' ),
    (2, 2, 40, 4, 'CUP' ),
    (3, 4, 32, 8, 'CUP' ),
    (5, 8, 25, 17, 'CUP' ),
    (9, 16, 20, 48, 'CUP' ),
    (17, 32, 16, 80, 'CUP' ),
    (33, 64, 13, 128, 'CUP' )
'''
    InsertData(insert_eventTypes)


def InsertDivision():
    insert_division = '''
    insert into tournaments_division
    (name, sort_order)
    values
    ('JR', 1),
    ('SR', 2),
    ('MA', 3)
'''
    InsertData(insert_division)



if __name__ == '__main__':
    args = sys.argv[1:]
    if args == []:
        InsertEventTypes()
        InsertChampionshipPoints()
        InsertDivision()
    else:
        for arg in args:
            if arg == 'event_types':
                InsertEventTypes()
                continue
            if arg == 'championship_points':
                InsertChampionshipPoints()
                continue
            if arg == 'division':
                InsertDivision()
                continue

