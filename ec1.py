#!/usr/bin/python2.7

import sys

from random import *
from Queue import *
from bisect import *
from math import *


# Constants
ARRIVAL = 0
DEPARTURE = 1
MAX_PACKETS = 10000


ARRIVAL_RATE = 0.5
DEPARTURE_RATE = 0.5

currentIndex = -1 # position of current event to be examined
packetCount = -1 # count of packets sent; used to limit simulation


class Statistics:
    """
    Statistics outputs
    """
    
    def __init__(self, busyTime = 0, meanQueueLength = 0, packetsDropped = 0, utilization = 0):
        self.busyTime = busyTime
        self.meanQueueLength = meanQueueLength
        self.packetsDropped = packetsDropped
        self.utilization = utilization


# statistics
statistics = Statistics()

class Event:
    """
    Event class
    """

    def __init__(self, time=0, eventType=0, packetNumber = -1, queueLength = 0):
        self.time = time
        self.eventType = eventType
        self.packetNumber = packetNumber
        self.msg = None
        self.queueLength = queueLength

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "<time = %d, eventType = %d, packetNumber = %d, queueLength = %d, msg = %s>" % (self.time, self.eventType, self.packetNumber, self.queueLength, self.msg)

    def __str__(self):
        return "<time = %d, eventType = %d, packetNumber = %d, queueLength = %d, msg = %s>" % (self.time, self.eventType, self.packetNumber, self.queueLength, self.msg)


class Packet:
    """
    Packet Class
    """

    def __init__(self, serviceTime = 0):
        self.serviceTime = serviceTime
        if(hasattr(self,'packetNumber')):
            Packet.packetNumber = Packet.packetNumber+1
            self.packetNumber = Packet.packetNumber
        else:
            Packet.packetNumber = 1
            self.packetNumber = 1



def exp_dist(rate):
    """
    Exponential Distribution
    """ 
    u = random()
    #return ((-1/rate) * log(1-u))
    return 1/((1-u)**(1/rate))


def arrival(pq, eventList):
    """
    Process and Generate Arrival Events
    """ 
    currentEvent = eventList[currentIndex]
    
    nextTime = 0
    dtime = 0

    global packetCount
    if(packetCount < MAX_PACKETS): # limits simulation length
        nextTime = currentEvent.time + exp_dist(ARRIVAL_RATE) 
        insort(eventList, Event(time=nextTime, eventType=ARRIVAL))
        packetCount += 1

    serviceTime = exp_dist(DEPARTURE_RATE)
    p = Packet(serviceTime)

    print ("%dth Packet Arriving, Arrival Time: %f." % (p.packetNumber, currentEvent.time))

    if(pq.empty()): # create departure event if queue is empty
        dtime = serviceTime+currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))

    
    #print "nextTime = ", nextTime, " dtime = ", dtime

    if(not pq.full()):
        pq.put(item = p, block = False)
    else: # queue is full, drop packet
        currentEvent.msg = "PACKET DROPPED"
        global statistics
        statistics.packetsDropped += 1 
        print ("Dropping %dth Packet" % p.packetNumber)



def departure(pq, eventList):
    """
    Process and Generate Departure Events
    """
    global currentIndex 
    currentEvent = eventList[currentIndex]
   
    packet = pq.get()

    global statistics
    statistics.busyTime += packet.serviceTime
   
    if(not pq.empty()): # send packet if one exists in queue
        dtime = packet.serviceTime + currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))
    print ("Transmitting %dth Packet, Departure Time: %f" % (packet.packetNumber, currentEvent.time))


def main():
    # Argument Handling
    if(len(sys.argv) != 4):
        print("usage:", str(sys.argv[0]), "[queue] [mu] [lambda]")
        return

    global MAX_PACKETS
    global ARRIVAL_RATE
    global DEPARTURE_RATE
    queueLength = int(sys.argv[1])
    ARRIVAL_RATE = float(sys.argv[3])
    DEPARTURE_RATE = float(sys.argv[2])

    print "Queue Length: %d" % queueLength
    print "ARRIVAL_RATE: %f" % ARRIVAL_RATE
    print "DEPARTURE_RATE: %f" % DEPARTURE_RATE

    fp = open("stat.csv", "a")

    pq = Queue(queueLength+1) # packet queue

    seed(200) # seed for generating random distributions
    
    # initialize event list with arrival event
    currentEvent = Event(time=0, eventType=ARRIVAL)
    eventList = sorted([currentEvent])
    
    global currentIndex
    currentIndex = 0

	# Begin simulation with no packets simulated
    global packetCount
    packetCount = 1

    while(currentIndex < len(eventList)):
        currentEvent = eventList[currentIndex]
        if(currentEvent.eventType == ARRIVAL):
            arrival(pq, eventList)
        else:
            departure(pq, eventList)
        
        currentEvent.queueLength = pq.qsize()-1 
        if(currentEvent.queueLength < 0):
            currentEvent.queueLength = 0

        print "queueLength: %d." % currentEvent.queueLength
        currentIndex += 1

    global statistics
    utilization = statistics.busyTime/eventList[-1].time    
    print "Total Busy Duration: %f" % statistics.busyTime
    print "Total Runtime: %f" % eventList[-1].time
    print "Utilization = %f" % utilization

    print "Total Packets Dropped = %d" % statistics.packetsDropped

    qlenTimeProduct = 0
    for i in range(1, len(eventList)):
        qlenTimeProduct += eventList[i-1].queueLength * (eventList[i].time - eventList[i-1].time)
    statistics.meanQueueLength = qlenTimeProduct/eventList[-1].time

    print "Mean Queue Length: %f" % statistics.meanQueueLength
    fp.write("%f,%f,%d,%f,%f,%d\n"% (ARRIVAL_RATE, DEPARTURE_RATE, queueLength, statistics.meanQueueLength, utilization, statistics.packetsDropped))
    

    fp.close()

if __name__ == '__main__':
    main()

