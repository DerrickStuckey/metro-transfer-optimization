## Determine best transfer point for any combination of stations

import csv

def load_transfer_points():
    input_filename = "../data/Transfer_Points.csv"

    transfer_points = {}

    with open(input_filename, 'rU') as input_csv:
        reader = csv.DictReader(input_csv, dialect="excel")
        for row in reader:
            station = row.pop('Station')
            lines = [line for line in row.keys() if row[line]=='1']
            transfer_points[station] = set(lines)

    return transfer_points

def load_line_positions():
    input_filename = "../data/Line_Positions.csv"

    line_positions = {}
    with open(input_filename, 'rU') as input_csv:
        reader = csv.DictReader(input_csv, dialect="excel")
        for row in reader:
            station = row.pop('Station')
            line_positions[station] = row

    return line_positions

# returns a set of lines based on the station's line positions
def get_station_lines(station_line_positions):
    """
    :param station_line_positions : dictionary of line names and positions on those lines
    :type station_line_positions : dict

    :return : Classifier capable of operating on raw text
    :rtype : set
    """
    lines = [line for line in station_line_positions.keys() if station_line_positions[line]!='']
    return set(lines)

transfer_points = load_transfer_points()
line_positions = load_line_positions()

# print "Metro Center lines: ", transfer_points['Metro Center']
# print "Metro Center line positions", line_positions['Metro Center']
# print "Rosslyn lines: ", get_station_lines(line_positions['Rosslyn'])

def find_transfer_route(start_station, end_station):
    print "start station: ", start_station
    print "end station: ", end_station

    # get full list of lines for each station
    start_station_lines = get_station_lines(line_positions[start_station])
    print "start station lines: ", start_station_lines
    end_station_lines = get_station_lines(line_positions[end_station])
    print "end station lines: ", end_station_lines

    # if start, end stations share a line, no transfer needed
    shared_lines = start_station_lines.intersection(end_station_lines)
    if (shared_lines):
        #select a shared line arbitrarily to use
        used_line = shared_lines.pop()
        return {'lines':[used_line],'transfers':[]}

    # get list of possible transfer points based on line overlap
    direct_transfer_points = []
    for point in transfer_points.keys():
        point_lines = transfer_points[point]
        if (point_lines.intersection(start_station_lines) and point_lines.intersection(end_station_lines)):
            direct_transfer_points.append(point)
    print "direct transfer points: ", direct_transfer_points

    # get minimum distance transfer point


    # try any 2-transfer routes, w/ penalty for extra transfer

    return "who knows?"


# best = find_transfer_route('Cleveland Park', 'Anacostia')
# best = find_transfer_route('Cleveland Park', 'Rosslyn')
best = find_transfer_route('Cleveland Park', 'Metro Center')

print best