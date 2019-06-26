#!/usr/bin/env python3.5

from collections import namedtuple
import os
import argparse
from datetime import datetime
from datetime import timedelta
import csv
import epics
import time
import pickle

# set the the IP Address for the systems from which you need to read
# timeData = namedtuple('timeData', 'la1 tcs mcs scs crcs')
os.environ["EPICS_CA_ADDR_LIST"] = "172.17.2.255"
fileName = 'timedata'+startDateStr+'.pkl'
chanNames = ['la1:timeProbe:TAI.VALA', 'tc1:timeProbe:TAI.VALA',\
             'tcs:timeProbe:TAI.VALA', 'm2:timeProbe:TAI.VALA',\
             'mc:timeProbe:TAI.VALA', 'cr:timeProbe:TAI.VALA']


def parse_args():
    '''
    This routines parses the arguments used when running this script
    '''
    parser = argparse.ArgumentParser(
        description='Use this script to capture Time data from different\
        telescope subsystems')

    parser.add_argument('-hr',
                        '--hrs',
                        dest='rtHrs',
                        default=0,
                        help='Number of hours for data capture\
                        e.g.: -h 3')

    parser.add_argument('-m',
                        '--min',
                        dest='rtMin',
                        default=1,
                        help='Number of minutes for data capture\
                        e.g.: -m 60')

    args = parser.parse_args()
    return args

def monChan(chanNames):
    chanList = []
    cnameList = []
    for cn in chanNames:
        chan = epics.PV(cn)
        chanStatus = chan.status
        if not(chanStatus == None):
            cnameList.append(cn)
            chanList.append(chan)
    return chanList, cnameList

if __name__ == '__main__':
    args = parse_args()
    dataCapDur = timedelta(hours=int(args.rtHrs), minutes=int(args.rtMin))
    monChanList, pvNames = monChan(chanNames)
    print(pvNames)
    with open(fileName, 'ab') as f:
        pickle.dump(pvNames, f)
    # cnt = 0
    startTime = datetime.now()
    startDateStr = datetime.strftime(startTime, '%Y%m%dT%H%M%S')
    currTime = datetime.now()
    while ((currTime - startTime) < dataCapDur):
        chanStatus = [chan.status for chan in monChanList]
        if not(chanStatus.count(None)):
            timeData = [chan.value[2] for chan in monChanList]
            with open(fileName, 'ab') as f:
                pickle.dump(timeData, f)
        currTime = datetime.now()
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
    print(sampleTimeArray[1])
    print("size of pickle: " + str(len(sampleTimeArray)))

