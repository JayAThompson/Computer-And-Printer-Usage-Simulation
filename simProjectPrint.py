# -*- coding: utf-8 -*-
"""
Command line argument format is python simProject.py <printer format> <number of trials>
Dependencies: NumPy and SciPy
Notes: 
    With regards to floors so the numbers don't get confusing
    0 is Cathedral ground floor, 1-38 are floors 1-38
    -1 is the basement, -2 is outside the building
"""
import sys
from numpy import random
from scipy.stats import skewnorm

distance = 0

#Generate floors the 8 printers are on
if sys.argv[1] == "default":
    printers = [0] * 8

elif sys.argv[1] == "uniform":
    printers = random.uniform(0, 38, 8)
    printers = [round(x) for x in printers]
    printers.sort()

elif sys.argv[1] == "custom":
    printers = [1.0, 4.0, 8.0, 9.0, 12.0, 13.0, 16.0, 33.0]

#can hardcode other generation schemes if desired later    
else:
    printers = [0] * 8

#The floor the student was at before heading to the printer
#Generate number of people according to command line arguments
fromFloor = random.uniform(-2, 38, int(sys.argv[2]))
fromFloor = [round(x) for x in fromFloor]

#The floor the student is going to after printing something
#change when we figure out skewed normals
toFloor = skewnorm.rvs(0.72554004, loc = 2.444444444, scale = 4.747421584, size = int(sys.argv[2]))
toFloor = [round(x) for x in toFloor]
    
for i in range(int(sys.argv[2])):
    #figure out which list comprehension to use for printers between to and from
    #if there is multiple between them, which printer they go to doesn't matter
    #and the distance travelled is absolute value of diff
    diff = toFloor[i] - fromFloor[i]
    distance += abs(diff)
    
    if (diff < 0):
        printersBetween = [x for x in printers if toFloor[i] <= x <= fromFloor[i]] #double check logic
    else:
        printersBetween = [x for x in printers if fromFloor[i] <= x <= toFloor[i]]
        
    if (len(printersBetween) == 0):
        #if no printer between to and from, calculate closest to each and pick smallest distance of the two
        closestToStart = min(printers, key = lambda x: abs(x - fromFloor[i]))
        closestToDest =  min(printers, key = lambda x: abs(x - toFloor[i]))
        
        #Thus distance traveled is diff + 2 * out of way distance to printer if none between
        if (closestToStart < closestToDest):
            distance += (2 * abs(closestToStart - fromFloor[i]))
        else:
            distance += (2 * abs(closestToDest - toFloor[i]))

print(printers)            
print("Average number of floors traveled: " + str(distance / int(sys.argv[2])))
    