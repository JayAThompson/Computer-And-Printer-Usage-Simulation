"""
Command line argument format is python simProjectOS.py <number of trials>
Dependencies: SimPy, NumPy
"""

import sys
import simpy
from random import expovariate
from numpy.random import normal
from numpy.random import uniform

macConcurrentUsers = 0
pcConcurrentUsers = 0
avgMacConcurrentUsers = 0
avgPCConcurrentUsers = 0

macUsers = 0
pcUsers = 0
pc = None
osx = None

#Is the pc resource
class PC(object):
    def __init__(self, env, numResource):
        self.env = env
        self.resrce = simpy.resources.resource.Resource(env, numResource)
        
    def useComp(self, person):
        nonNeg = normal(loc = 40, scale = 13)
        
        while nonNeg < 0:
            nonNeg = normal(loc = 40, scale = 13)
            
        yield env.timeout(nonNeg)

#Is the mac resource
class mac(object):
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
def setUp(env, numPC, numMac):
    global pc, osx, macConcurrentUsers, pcConcurrentUsers, avgMacConcurrentUsers, avgPCConcurrentUsers, macUsers, pcUsers
    macConcurrentUsers = 0
    pcConcurrentUsers = 0
    
    pc = PC(env, numPC)
    osx = mac(env, numMac) 
    i = 1
    while (env.now <= 870): 
        
        
        yield env.timeout((expovariate(0.52)))
        
        #Got this
        if(uniform() <=  0.75665):
            env.process(user(env, pc, "Person" + str(i)))
            pcUsers += 1
        else:
            env.process(user(env, osx, "Person" + str(i)))
            macUsers += 1
        i += 1

        if(pc.resrce.count > pcConcurrentUsers):
            pcConcurrentUsers = pc.resrce.count
            
        if(osx.resrce.count > macConcurrentUsers):
            macConcurrentUsers = osx.resrce.count
        
    
#runs the simulation            
for i in range (int(sys.argv[1])):
    
    env = simpy.Environment() 
    env.process(setUp(env, 44, 21))
    env.run(until = 870)
    avgPCConcurrentUsers += pcConcurrentUsers
    avgMacConcurrentUsers += macConcurrentUsers
    
print("Average total users of PCs per day: " + str(pcUsers / int(sys.argv[1])))
print("Average total users of macs per day: " + str(macUsers / int(sys.argv[1])))
print("Average of max concurrent users of macs per day: " + str(avgMacConcurrentUsers / int(sys.argv[1])))
print("Average of max concurrent users of PCs per day: " + str(avgPCConcurrentUsers / int(sys.argv[1])))
