import ProcessTdf as ProcessTdf
import Insert_Data as Insert_Data
import os

import GetData as GetData

file_dir = r'.\data'

for file in os.listdir(file_dir):
    print(file)
    file_path = os.path.join(file_dir, file)

    if os.path.isdir(file_path):
        continue

    has_file_been_processed = Insert_Data.HasFileBeenRan(file)

    if has_file_been_processed:
        print('\tThis has been processed')
        continue

    tournament_data, player_data, pod_data,standings_data, event_id = ProcessTdf.GetDataFromTdf(file_path)



    Insert_Data.InsertTournamentData(tournament_data)
    Insert_Data.InsertPlayersData(player_data)
    if type(pod_data) == list:
        for pod in pod_data:
            Insert_Data.InsertPodData(pod, event_id)
    else:
        Insert_Data.InsertPodData(pod_data, event_id)
    Insert_Data.InsertStandingsData(standings_data, event_id)

    Insert_Data.InsertFileData([file])

GetData.RunData()