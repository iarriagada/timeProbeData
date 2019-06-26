#!/usr/bin/env python3.5

from collections import namedtuple
import os
from datetime import datetime
import csv
import epics
import time
import pickle

# set the the IP Address for the systems from which you need to read
# timeData = namedtuple('timeData', 'la1 tcs mcs scs crcs')
os.environ["EPICS_CA_ADDR_LIST"] = "172.17.2.255"
currDate = datetime.now()
currDateStr = datetime.strftime(currDate, '%Y%m%dT%H%M%S')
fileName = 'timedata'+currDateStr+'.pkl'
chanNames = ['la1:timeProbe:TAI.VALA', 'tc2:timeProbe:TAI.VALA',\
             'tcs:timeProbe:TAI.VALA', 'm2:timeProbe:TAI.VALA',\
             'mc:timeProbe:TAI.VALA', 'cr:timeProbe:TAI.VALA']


def monChan(chanList, chanNames):
    chanList = []
    for cn in chanNames:
        chan = epics.PV(cn)
        if chan.status:
            chanList.append(chan)
    return chanList


timeLA1Array = epics.PV('la1:timeProbe:TAI.VALA', auto_monitor=False)
timeTC1Array = epics.PV('tc2:timeProbe:TAI.VALA', auto_monitor=False)
timeTCSArray = epics.PV('tcs:timeProbe:TAI.VALA', auto_monitor=False)
timeSCSArray = epics.PV('m2:timeProbe:TAI.VALA', auto_monitor=False)
timeMCSArray = epics.PV('mc:timeProbe:TAI.VALA', auto_monitor=False)
timeCRCSArray = epics.PV('cr:timeProbe:TAI.VALA', auto_monitor=False)
cnt = 0
while (cnt < 2):
    timeLA1 = timeLA1Array.get(timeout=0.01)
    timeTCS = timeTCSArray.get(timeout=0.01)
    print('tc1 start connection')
    timeTC1 = timeTC1Array.get(timeout=10)
    print('tc1 connected')
    # print('test:')
    # print(timeTC1)
    timeMCS = timeMCSArray.get(timeout=0.01)
    timeSCS = timeSCSArray.get(timeout=0.01)
    timeCRCS = timeCRCSArray.get(timeout=0.01)
    timeData = [timeLA1[2], timeTCS[2], timeMCS[2], timeSCS[2], timeCRCS[2]]
    if not(timeData.count(None)):
        with open(fileName, 'ab') as f:
            pickle.dump(timeData, f)
    cnt += 1
    time.sleep(0.075)

sampleTimeArray = []
with open(fileName, 'rb') as f:
    while(True):
        try:
            sampleTimeArray.append(pickle.load(f))
        except (EOFError):
            break

print("sample of Time array:")
print(sampleTimeArray[0])
print("size of pickle: " + str(len(sampleTimeArray)))

