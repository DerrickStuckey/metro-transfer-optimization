## Just tests functions in transfer_finder.py

import transfer_finder as tf

### Test stuff: ###

# print "Metro Center lines: ", transfer_points['Metro Center']
# print "Metro Center line positions", line_positions['Metro Center']
# print "Rosslyn lines: ", get_station_lines(line_positions['Rosslyn'])


# best = tf.find_transfer_route('Cleveland Park', 'Anacostia')
# best = tf.find_transfer_route('Cleveland Park', 'Rosslyn')
# best = tf.find_transfer_route('Cleveland Park', 'Metro Center')
# best = tf.find_transfer_route('Huntington', 'Vienna')
# best = tf.find_transfer_route('Waterfront', 'Union Station')
# best = tf.find_transfer_route('New Carrollton', 'Judiciary Square')

## a trip w/ potentially quicker 2-transfer route than single-line route
best = tf.find_transfer_route('Franconia-Springfield','Federal Center SW')

# print "best route: ", best
print "best route: ", best.lines, best.directions, best.transfers, best.total_distance

# metrics = get_trip_metrics(start_station='Cleveland Park',end_station='Metro Center',line='Red',line_positions=line_positions)
#
# print "distance: ", metrics['distance']

