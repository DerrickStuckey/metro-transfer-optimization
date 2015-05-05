## Metro Transfer Optimization Model

#SETS
set I;			#transfer points
set L;			#metro lines (color + direction)

#PARAMETERS
param TRAFFIC{I,L,L};	#avg # of travelers
#param SHARE{L,L};		#1 if lines share a track, else 0
param TIME_TO{L,I};		#time from start of line l to transfer point i
param INTERVAL;			#interval at which trains are run
param TRANSFER_TIME;	#time needed to transfer at a transfer point

#VARIABLES
var s{L} >= 0;			#start time for line l
var k{I,L,L} integer;	#artificial modulo var

#OBJECTIVE FUNCTION
minimize ExpectedWaitTime:
sum{i in I, l in L, m in L} TRAFFIC[i,l,m]*(s[m]+TIME_TO[m,i]-s[l]-TIME_TO[l,i] - k[i,l,m]*INTERVAL - TRANSFER_TIME);

#CONSTRAINTS
subject to ValidStart{l in L}: 
s[l] <= INTERVAL-1;

subject to ValidModulo{i in I, l in L, m in L}: 
k[i,l,m]*INTERVAL <= (s[m] + TIME_TO[m,i] - s[l] - TIME_TO[l,i] - TRANSFER_TIME);

# *add shared line constraint*
