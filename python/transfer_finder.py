## Determine best transfer point for any combination of stations

import csv

def load_transfer_points():
    input_filename = "../data/Transfer_Points.csv"

    with open(input_filename, 'rU') as input_csv:
        reader = csv.DictReader(input_csv, dialect="excel")
        transfer_points = [row for row in reader]
    return transfer_points

def load_line_positions():
    input_filename = "../data/Line_Positions.csv"

    with open(input_filename, 'rU') as input_csv:
        reader = csv.DictReader(input_csv, dialect="excel")
        line_positions = [row for row in reader]
    return line_positions

transfer_points = load_transfer_points()
print transfer_points[0]
line_positions = load_line_positions()
# print line_positions[0]