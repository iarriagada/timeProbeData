#!/usr/bin/env python3.5

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pickle
import argparse


def parse_args():
    '''
    This routines parses the arguments used when running this script
    '''
    parser = argparse.ArgumentParser(
        description='Use this script to plot captured Time data from different\
        telescope subsystems from a pickled file')

    parser.add_argument('pklFile',
                        metavar='PKL-FILE',
                        help='path to pickled file with data to be plotted')

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

if __name__ == '__main__':
    args = parse_args()
    dataTimeArray = list()
    diffTC1 = list()
    diffTCS = list()
    diffMCS = list()
    diffSCS = list()
    diffCRCS = list()
    # f = open("2018-12-28-nfsTime-10d.txt")
    with open(args.pklFile, 'rb') as f:
        while(True):
            try:
                dataTimeArray.append(pickle.load(f))
            except (EOFError):
                break
    dataLabels = dataTimeArray[0]
    for data in dataTimeArray[1:]:
        recTime = datetime.fromtimestamp(data[0])
        receptionTime = datetime.strftime(recTime, '%m/%d/%Y %H:%M:%S.%f')
        receptionTime = datetime.strptime(receptionTime, '%m/%d/%Y %H:%M:%S.%f')
        diffTC1.append([receptionTime, data[1]-data[0]])
        diffTCS.append([receptionTime, data[2]-data[0]])
        diffMCS.append([receptionTime, data[3]-data[0]])
        diffSCS.append([receptionTime, data[4]-data[0]])
        diffCRCS.append([receptionTime, data[5]-data[0]])

    tsDTC1, dTC1 = zip(*diffTC1)
    tsDTCS, dTCS = zip(*diffTCS)
    tsDMCS, dMCS = zip(*diffMCS)
    tsDSCS, dSCS = zip(*diffSCS)
    tsDCRCS, dCRCS = zip(*diffCRCS)
    # print(diffTCS)
    # print(tsDTCS)
    # print(dTCS)
    # dts, vals = [], []
    # for l in f:
        # lst = l.split()
        # #print lst
        # dt = datetime.strptime(lst[1]+'T'+lst[2], '%Y-%m-%dT%H:%M:%S.%f')
        # dts.append(dt)
        # vals.append(lst[3])


    fig, ax1 = plt.subplots()
    plt.title("pvload+pvsave time on simple soft-ioc running on sbfrtdev-lv1 and r/w to cportprd-lv1 1Hz")
    ax1.plot(tsDTC1, dTC1, "b.", label=dataLabels[1])
    ax1.plot(tsDTCS, dTCS, "r.", label=dataLabels[2])
    ax1.plot(tsDMCS, dMCS, "g.", label=dataLabels[3])
    ax1.plot(tsDSCS, dSCS, "y.", label=dataLabels[4])
    ax1.plot(tsDCRCS, dCRCS, "k.", label=dataLabels[5])
    ax1.grid(True)
    ax1.set_ylabel("Milliseconds")
    ax1.set_ylim(-0.001, 0.007)
    plt.gcf().autofmt_xdate()


    # currDate = dts[0]
    # while currDate < dts[-1]:

        # currDate += timedelta(1)
        # nightStart = (currDate-timedelta(1)).replace(hour=20, minute=0, second=0)
        # nightEnd = currDate.replace(hour=8, minute=0, second=0)

        # #print nightStart, nightEnd
        # ax1.axvspan(nightStart, nightEnd, color = 'grey', alpha = 0.5)

    plt.legend()
    plt.show()
