__author__ = 'dstuckey'

import csv

def concat_line_dir(line,dir):
    return line + "_" + dir

station_keys = ['Metro Center','King Street','Gallery Place-Chinatown',"L'Enfant Plaza",'Fort Totten','Rosslyn',
                'East Falls Church','Stadium-Armory','Pentagon']

line_keys = ['Blue','Green','Orange','Red','Silver','Yellow']

dir_keys = ['pos','neg']

#station_keys = ['Rosslyn']
#line_keys = ['Blue','Orange']
#dir_keys = ['pos','neg']

# generate line_dir_keys
line_dir_keys = []
for line in line_keys:
    for dir in dir_keys:
        line_dir_keys.append(concat_line_dir(line,dir))

print line_dir_keys

#transfer_filename = "../data/2014_Sat_Morn_Transfers.csv"
transfer_filename = "../data/2014_Sat_Eve_Transfers.csv"

csv_headers = ['Station','Entry_Line','Entry_Dir','Exit_Line','Exit_Dir','Avg_Ridership']

#def format_traffic_param(transfer_filename):

#data format:
# traffic[station][entry_line_dir][exit_line_dir] -> count

#initialize traffic triple dict w/ all 0's
traffic = {}
for station in station_keys:
    traffic[station] = {}
    for entry_line_dir in line_dir_keys:
        traffic[station][entry_line_dir] = {}
        for exit_line_dir in line_dir_keys:
            traffic[station][entry_line_dir][exit_line_dir] = 0

with open(transfer_filename, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        station = row['Station']
        entry_line_dir = concat_line_dir(row['Entry_Line'],row['Entry_Dir'])
        exit_line_dir = concat_line_dir(row['Exit_Line'],row['Exit_Dir'])
        ridership = row['Avg_Ridership']
        traffic[station][entry_line_dir][exit_line_dir] = ridership

#print the actual traffic data parameter
print("param TRAFFIC :=")
for station in station_keys:
    print '\t[{0},*,*]:\t\t'.format(station),
    for exit_line_dir in line_dir_keys:
        print exit_line_dir, "\t",
    print ":="

    for entry_line_dir in line_dir_keys:
        print "\t\t", entry_line_dir, "\t\t",
        for exit_line_dir in line_dir_keys:
            ridership = traffic[station][entry_line_dir][exit_line_dir]
            print ridership, "\t\t\t",
        print ""

print ";"
