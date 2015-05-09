## Metro Transfer Optimization Model

#SETS
set I;			#transfer points
set L;			#metro lines (color + direction)

#PARAMETERS
param TRAFFIC{I,L,L};	#avg # of travelers
param TIME_TO{L,I};		#time from start of line l to transfer point i
param INTERVAL;			#interval at which trains are run
param TRANSFER_TIME;	#time needed to transfer at a transfer point

param SHARE{L,L};		#1 if lines share a track, else 0
param OFFSET{L,L};		#start time offset for shared lines
param M;				#big-M for shared lines constraint

#VARIABLES
var s{L} >= 0;				#start time for line l
var k{I,L,L} integer;		#artificial modulo var
var b{L,L} binary;			#var for artificial absolute value

#OBJECTIVE FUNCTION
minimize ExpectedWaitTime:
sum{i in I, l in L, m in L} TRAFFIC[i,l,m]*(s[m]+TIME_TO[m,i]-s[l]-TIME_TO[l,i] - k[i,l,m]*INTERVAL - TRANSFER_TIME);

#CONSTRAINTS
subject to ValidStart{l in L}: 
s[l] <= INTERVAL-1;

subject to ValidModulo{i in I, l in L, m in L}: 
k[i,l,m]*INTERVAL <= (s[m] + TIME_TO[m,i] - s[l] - TIME_TO[l,i] - TRANSFER_TIME);

#Shared Lines requires two constraints: for positive, negative cases
subject to SharedLines1{l in L, m in L}:
(s[m]-s[l]+OFFSET[l,m]) + M*b[l,m] >= SHARE[l,m];

subject to SharedLines2{l in L, m in L}:
-(s[m]-s[l]+OFFSET[l,m]) + M*(1-b[l,m]) >= SHARE[l,m];
