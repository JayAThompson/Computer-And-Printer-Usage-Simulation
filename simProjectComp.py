"""
Command line argument format is python simProjectComp.py <number of trials>
Dependencies: SimPy, NumPy
"""

import sys
import simpy
from random import expovariate
from numpy.random import normal

concurrentUsers = 0
avgConcurrentUsers = 0
macUsers = 0
PCUsers = 0
comp = None

#Is the computer resource
class computer(object):
    def __init__(self, env, numResource):
        self.env = env
        self.resrce = simpy.resources.resource.Resource(env, numResource)
        
    def useComp(self, person):
        nonNeg = normal(loc = 40, scale = 13)
        
        while nonNeg < 0:
            nonNeg = normal(loc = 40, scale = 13)
            
        yield env.timeout(nonNeg)
    
    
#handles the requests    
def user(env, comp, person):
    with comp.resrce.request() as request:
        yield request
        
        yield env.process(comp.useComp(person))
        
        
#generates the people        
def setUp(env, numComp):
    global comp, avgConcurrentUsers, concurrentUsers
    concurrentUsers = 0
    
    comp = computer(env, numComp)
    
    i = 1
    while (env.now <= 870): 
        
        
        yield env.timeout((expovariate(0.52)))
        env.process(user(env, comp, "Person" + str(i)))
        
        i += 1

        if(comp.resrce.count > concurrentUsers):
            concurrentUsers = comp.resrce.count
        
    
#runs the simulation            
for i in range (int(sys.argv[1])):
    
    env = simpy.Environment() 
    env.process(setUp(env, 67))
    env.run(until = 870)
    avgConcurrentUsers += concurrentUsers

print("Average of max concurrent users per day: " + str(avgConcurrentUsers / int(sys.argv[1])))