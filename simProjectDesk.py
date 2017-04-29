"""
Command line argument format is python simProjectDesk.py <number of trials>
"""
import sys
from random import expovariate

#minutesOpen assumes it's monday -thursday as the labs are open from 7:30 am to 10 pm
timeUsed = 0
visits = 0

for i in range(int(sys.argv[1])):
    minutesOpen = 870

    while(minutesOpen > 0):
        #from data collection 3 people visited desk in the 5 hours we have collection data for on the topic
        #thus 3/5 people per hour or 0.6
        #as poisson inter intervals are exponentially distributed, you can use expovariate to do poisson
        genPeople = expovariate(0.6/60)
        
        #this is so it doesn't increment visits if the lab closes before the next arrival
        #same with adding how much time the desks have spent helping people or otherwise doing something
        if(minutesOpen - genPeople > 0):
            visits += 1
            timeUsed += expovariate(1/2)
        
        minutesOpen -= genPeople
    
print("Number of visits: " + str(visits/int(sys.argv[1])))
print("Minutes utilized: " + str(timeUsed/int(sys.argv[1])))
