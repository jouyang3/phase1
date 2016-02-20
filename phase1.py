#!/bin/python

import sys

from random import *
from queue import *
from bisect import *
from math import *


# Constants
ARRIVAL = 0
DEPARTURE = 1
MAX_PACKETS = 10000


ARRIVAL_RATE = 0.5
DEPARTURE_RATE = 0.5

time = 0 # current simulation time
currentIndex = -1 # position of current event to be examined
packetCount = -1 # count of packets sent; used to limit simulation



class Event:

    def __init__(self, time=0, eventType=0, packetNumber = -1):
        self.time = time
        self.eventType = eventType
        self.packetNumber = packetNumber
        self.msg = None

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "<time = %d, eventType = %d, packetNumber = %d, msg = %s>" % (self.time, self.eventType, self.packetNumber, self.msg)

    def __str__(self):
        return "<time = %d, eventType = %d, packetNumber = %d>" % (self.time, self.eventType, self.packetNumber, self.msg)



class Packet:

    def __init__(self, serviceTime = 0):
        self.serviceTime = serviceTime
        if(hasattr(self,'packetNumber')):
            Packet.packetNumber = Packet.packetNumber+1
            self.packetNumber = Packet.packetNumber
        else:
            Packet.packetNumber = 0
            self.packetNumber = 0



def exp_dist(rate): # exponential distribution
    u = random()
    return ((-1/rate) * log(1-u))



def arrival(pq, eventList): # process current arrival event
    currentEvent = eventList[currentIndex]
    

    global packetCount
    if(packetCount < MAX_PACKETS): # limits simulation length
        nextTime = currentEvent.time + exp_dist(ARRIVAL_RATE) 
        insort(eventList, Event(time=nextTime, eventType=ARRIVAL))
        packetCount += 1

    serviceTime = exp_dist(DEPARTURE_RATE)
    p = Packet(serviceTime)

    print ("%dth Packet Arriving." % p.packetNumber)

    if(pq.empty()): # create departure event if queue is empty
        dtime = serviceTime+currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))

    if(not pq.full()): # enqueue packet
        pq.put(item = p, block = False)
    else: # queue is full, drop packet
        currentEvent.msg = "PACKET DROPPED"
        print ("Dropping %dth Packet" % p.packetNumber)



def departure(pq, eventList): # process current departure event
    currentEvent = eventList[currentIndex]

    if(not pq.empty()): # send packet if one exists in queue
        packet = pq.get()
        dtime = packet.serviceTime + currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))
        print ("Transmitting %dth Packet" % packet.packetNumber)



def main():
    # Argument Handling
    if(len(sys.argv) != 4):
        print("usage:", str(sys.argv[0]), "[queue] [mu] [lambda]")
        return

    maxQueueLen= int(sys.argv[1])
    arrivalRate = float(sys.argv[2])
    departureRate = float(sys.argv[3])

    pq = Queue(maxQueueLen) # packet queue

    seed(1) # seed for generating random distributions
    
		# initialize event list with arrival event
    currentEvent = Event(time=0, eventType=ARRIVAL)
    eventList = sorted([currentEvent])
    currentIndex = 0

    nextArrivalTime = currentEvent.time + exp_dist(ARRIVAL_RATE);
    p = Packet(serviceTime = random())
    
    nextArrival = Event(time=nextArrivalTime, eventType=ARRIVAL)
    insort(eventList, nextArrival)
    
		# Begin simulation with no packets simulated
    global packetCount
    packetCount = 0

    while(currentIndex < len(eventList)):
        currentEvent = eventList[currentIndex]
        if(currentEvent.eventType == ARRIVAL):
            arrival(pq, eventList)
        else:
            departure(pq, eventList)
        
        currentIndex += 1
    


if __name__ == '__main__':
    main()

