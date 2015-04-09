## Determine best transfer point for any combination of stations

import csv

class Route:
    def __init__(self, lines, directions, transfers, total_distance):
        self.lines = lines
        self.directions = directions
        self.transfers = transfers
        self.total_distance = total_distance

class LineTrip:
    def __init__(self, distance, direction):
        self.distance = distance
        self.direction = direction

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

# Returns LineTrip object
def get_trip_metrics(start_station, end_station, line, line_positions):
    try:
        start_pos = line_positions[start_station][line]
        end_pos = line_positions[end_station][line]
        # print "start_pos: ", start_pos
        # print "end_pos: ", end_pos
        distance = abs(int(end_pos) - int(start_pos))
        direction = 'pos' if (int(end_pos) >= int(start_pos)) else 'neg'
        return LineTrip(distance=distance,direction=direction)
        # return {'distance':distance,'direction':direction}
    except:
        print "number_of_stops() error for: ", start_station, " -> ", end_station, " ", "; line=", line

#Returns Route object representing shortest route found
def find_transfer_route(start_station, end_station, transfer_penalty=1):
    # print "start station: ", start_station
    # print "end station: ", end_station

    # get full list of lines for each station
    start_station_lines = get_station_lines(__line_positions[start_station])
    # print "start station lines: ", start_station_lines
    end_station_lines = get_station_lines(__line_positions[end_station])
    # print "end station lines: ", end_station_lines

    routes = []

    # try all single-line routes
    shared_lines = start_station_lines.intersection(end_station_lines)
    for used_line in shared_lines:
        # for each feasible single-line route, compute all the route details and append it to the list
        trip_metrics = get_trip_metrics(start_station,end_station,used_line,__line_positions)
        routes.append(Route(lines=[used_line],transfers=[],total_distance=trip_metrics.distance,
                            directions=[trip_metrics.direction]))

    # try all feasible 1-transfer routes
    for xfer_point in __transfer_points.keys():
        # find shared lines between (start, xfer), and (xver, end)
        point_lines = __transfer_points[xfer_point]
        shared_lines_start = point_lines.intersection(start_station_lines)
        shared_lines_end = point_lines.intersection(end_station_lines)

        # Iterate through all valid line combinations for this set of transfers
        for start_line in shared_lines_start:
            for end_line in shared_lines_end:
                # for each feasible line combination, compute all the route details and append it to the list
                first_trip_metrics = get_trip_metrics(start_station=start_station,end_station=xfer_point,
                                                      line=start_line,line_positions=__line_positions)
                second_trip_metrics = get_trip_metrics(start_station=xfer_point,end_station=end_station,
                                                         line=end_line,line_positions=__line_positions)
                total_distance = first_trip_metrics.distance + second_trip_metrics.distance + transfer_penalty
                directions = [first_trip_metrics.direction,second_trip_metrics.direction]
                routes.append(Route(lines=[start_line,end_line],transfers=xfer_point,
                                    total_distance=total_distance,directions=directions))

    # print "direct routes: "
    # for route in routes:
    #     print route

    # try any 2-transfer routes, w/ penalty for extra transfer
    for xfer_point_1 in __transfer_points.keys():
        for xfer_point_2 in __transfer_points.keys():
            point_1_lines = __transfer_points[xfer_point_1]
            point_2_lines = __transfer_points[xfer_point_2]
            shared_lines_start = start_station_lines.intersection(point_1_lines)
            shared_lines_mid = point_1_lines.intersection(point_2_lines)
            shared_lines_end = point_2_lines.intersection(end_station_lines)

            # Iterate through all valid line combinations for this set of transfers
            for start_line in shared_lines_start:
                for mid_line in shared_lines_mid:
                    for end_line in shared_lines_end:
                        # for each feasible line combination, compute all the route details and append it to the list
                        start_trip_metrics = get_trip_metrics(start_station, xfer_point_1, start_line, __line_positions)
                        mid_trip_metrics = get_trip_metrics(xfer_point_1, xfer_point_2, mid_line, __line_positions)
                        end_trip_metrics = get_trip_metrics(xfer_point_2, end_station, end_line, __line_positions)
                        total_distance = start_trip_metrics.distance + mid_trip_metrics.distance + \
                                         end_trip_metrics.distance + 2*transfer_penalty
                        directions = [start_trip_metrics.direction, mid_trip_metrics.direction, end_trip_metrics.direction]
                        routes.append(Route(lines=[start_line,mid_line,end_line],transfers=[xfer_point_1,xfer_point_2],
                                            total_distance=total_distance,directions=directions))

    # print "all routes: "
    # for route in routes:
    #     print route.transfers, route.lines, route.total_distance

    # find best route of those listed
    # sorted_routes = sorted(routes, key=lambda x: x['total_distance'])
    sorted_routes = sorted(routes, key=lambda x: x.total_distance)

    return sorted_routes[0]

# load as hidden vars
__transfer_points = load_transfer_points()
__line_positions = load_line_positions()