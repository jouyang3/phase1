from random import *
from Queue import *
from bisect import *
from math import *

MAXBUFFER = 100
ARRIVAL = 0
DEPARTURE = 1
ARRIVAL_RATE = 0.5
DEPARTURE_RATE = 0.5
MAX_PACKETS = 10000

time = 0
pq = Queue(MAXBUFFER)
eventList=[]
currentIndex = -1
n = -1

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

def exp_dist(rate):
    u = random()
    return ((-1/rate)*log(1-u))

def arrival():
    currentEvent = eventList[currentIndex]
    
    global n
    if(n < MAX_PACKETS):
        nextTime = currentEvent.time + exp_dist(ARRIVAL_RATE) 
        insort(eventList, Event(time=nextTime, eventType=ARRIVAL))
        n += 1

    serviceTime = exp_dist(DEPARTURE_RATE)

    p = Packet(serviceTime)

    print ("%dth Packet Arriving." % p.packetNumber)
    global pq

    if(pq.empty()):
        dtime = serviceTime+currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))

    try:
        pq.put(item = p, block = False)
    except(Full):
        currentEvent.msg = "PACKET DROPPED"
        print ("Dropping %dth Packet" % p.packetNumber)

def departure():
    currentEvent = eventList[currentIndex]

    global pq
    if(not pq.empty()):
        packet = pq.get()
        dtime = packet.serviceTime + currentEvent.time
        insort(eventList, Event(time=dtime, eventType=DEPARTURE))
        print ("Transmitting %dth Packet" % packet.packetNumber)

def main():
    seed(1)
    
    currentEvent = Event(time=0, eventType=ARRIVAL)

    global currentIndex
    currentIndex = 0

    global eventList
    eventList = sorted([currentEvent])

    nextArrivalTime = currentEvent.time + exp_dist(ARRIVAL_RATE);
    p = Packet(serviceTime = random())
    
    nextArrival = Event(time=nextArrivalTime, eventType=ARRIVAL)
    insort(eventList, nextArrival)
    
    global n
    n = 0
    while(currentIndex < len(eventList)):
        currentEvent = eventList[currentIndex]
        if(currentEvent.eventType == ARRIVAL):
            arrival()
        else:
            departure()
        
        currentIndex += 1
    

if __name__ == '__main__':
    main()

    

