__author__ = 'dstuckey'

import csv

def concat_line_dir(line,dir):
    return line + "_" + dir

station_keys = ['Metro Center','King Street''Gallery Place-Chinatown',"L'Enfant Plaza",'Fort Totten','Rosslyn',
                'East Falls Church','Stadium-Armory','Pentagon']

line_keys = ['Blue','Green','Orange','Red','Silver','Yellow']

dir_keys = ['pos','neg']

# generate line_dir_keys
line_dir_keys = []
for line in line_keys:
    for dir in dir_keys:
        line_dir_keys.append(concat_line_dir(line,dir))

print line_dir_keys

sample_transfer_filename = "../data/2014_Sat_Morn_Sample_Transfers.csv"

csv_headers = ['Station','Entry_Line','Entry_Dir','Exit_Line','Exit_Dir','Avg_Ridership']


def format_traffic_param(transfer_filename):
    #data format:
    # stations[entry_line_dir][exit_line_dir] -> count

    with open(transfer_filename, 'rU') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            pass
