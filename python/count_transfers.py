## Reads actual WMATA ridership dataset
## Finds transfer points for each start/end station combination
## Computes total number of transfers at each transfer point

import transfer_finder as tf
import csv
import collections

# class TransferCount:
#     def __init__(self, distance, direction):
#         self.distance = distance
#         self.direction = direction

sat_morning_file = "../data/2014_Sat_Morn.csv"
entry_station_header,exit_station_header,avg_ridership_header = "Ent Station","Ext Station","AvgRidership"

# {transfer_tuple: count}
transfer_counts = collections.defaultdict(lambda: 0)

with open(sat_morning_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, dialect="excel")
    # for row in [reader.next(),reader.next(),reader.next()]:
    for row in reader:
        entry_station = row[entry_station_header]
        exit_station = row[exit_station_header]
        ridership = float(row[avg_ridership_header])
        route = tf.find_transfer_route(entry_station,exit_station,transfer_penalty=1)
        print "route: ", route.lines, route.directions, route.transfer_stations
        transfers = route.get_transfers()
        for transfer in transfers:
            transfer_counts[transfer.get_tuple()] += ridership
            print "transfer_tuple: ", transfer.get_tuple()
            # print transfer_counts[transfer.get_tuple()]

trans1 = tf.Transfer('Rosslyn','Blue','pos','Orange','neg')

print "trans1 ridership: ", transfer_counts[trans1.get_tuple()]

# save results to csv
output_filename = "../data/2014_Sat_Morn_Transfers.csv"
with open(output_filename, 'wb') as outputcsv:
    writer = csv.writer(outputcsv, delimiter=",")
    writer.writerow(['Station','Entry_Line','Entry_Dir','Exit_Line','Exit_Dir','Avg_Ridership'])
    for transfer_tuple in transfer_counts.keys():
        writer.writerow([transfer_tuple[0],transfer_tuple[1],transfer_tuple[2],transfer_tuple[3],
                        transfer_tuple[4],transfer_counts[transfer_tuple]])