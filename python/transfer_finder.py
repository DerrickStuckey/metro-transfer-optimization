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

def number_of_stops(start_station, end_station, line, line_positions):
    start_pos = line_positions[start_station][line]
    end_pos = line_positions[end_station][line]
    print "start_pos: ", start_pos
    print "end_pos: ", end_pos
    return abs(int(end_pos) - int(start_pos))

transfer_points = load_transfer_points()
line_positions = load_line_positions()

# print "Metro Center lines: ", transfer_points['Metro Center']
# print "Metro Center line positions", line_positions['Metro Center']
# print "Rosslyn lines: ", get_station_lines(line_positions['Rosslyn'])

def find_transfer_route(start_station, end_station, transfer_penalty=1):
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
        distance = number_of_stops(start_station,end_station,used_line,line_positions)
        return {'lines':[used_line],'transfers':[],'distance':distance}

    # get list of possible transfer points based on line overlap
    routes = []
    direct_transfer_distances = {}

    for xfer_point in transfer_points.keys():
        # find shared lines between (start, xfer), and (xver, end)
        point_lines = transfer_points[xfer_point]
        shared_lines_start = point_lines.intersection(start_station_lines)
        shared_lines_end = point_lines.intersection(end_station_lines)

        # if transfer point is valid, find the distance (total stops) used
        if (shared_lines_start and shared_lines_end):
            start_line = shared_lines_start.pop()
            end_line = shared_lines_end.pop()
            first_distance = number_of_stops(start_station=start_station,end_station=xfer_point,line=start_line,line_positions=line_positions)
            second_distance = number_of_stops(start_station=xfer_point,end_station=end_station,line=end_line,line_positions=line_positions)
            total_distance = first_distance + second_distance
            direct_transfer_distances[xfer_point] = total_distance
            routes.append({'lines':[start_line,end_line], 'transfers':xfer_point, 'distance': total_distance})

    print "direct transfer distances: ", direct_transfer_distances
    print "routes: "
    for route in routes:
        print route

    # try any 2-transfer routes, w/ penalty for extra transfer


    # find best route of those listed
    sorted_routes = sorted(routes, key=lambda x: x['distance'])

    return sorted_routes[0]


best = find_transfer_route('Cleveland Park', 'Anacostia')
# best = find_transfer_route('Cleveland Park', 'Rosslyn')
# best = find_transfer_route('Cleveland Park', 'Metro Center')

print "best: ", best

dist = number_of_stops(start_station='Cleveland Park',end_station='Metro Center',line='Red',line_positions=line_positions)

print dist