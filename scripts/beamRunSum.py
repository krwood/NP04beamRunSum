#***********************************************************************
#
# Kevin Wood; November, 2018
#
# - Meant to be run with python3:
#     >> cd /path/to/NP04beamRunSum
#     >> source setup.sh                 # sets NP04BRSROOT variable
#     >> python3 scripts/beamRunSum.py
#
# - Be sure to double check how time zones are handled. In some cases
#   datetime uses the system clock to assign a time zone. Time zones
#   can also be forced by hand.
#
#***********************************************************************

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import csv
from datetime import datetime
from matplotlib import transforms
import numpy as np
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from datetime import timedelta
import pandas as pd
import time as pytime
import os
startTime = datetime.now()

# USER: Make a list of the days you want to include in the plot here.
#       There should be a corresponding files in $ROOTDIR/data.

#datelist = ['2018-10-19','2018-10-20']
#datelist = ['2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01']
#datelist = ['2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11']
#datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14']
datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11','2018-11-12']
#datelist = ['2018-09-14','2018-09-15','2018-09-16','2018-09-17','2018-09-18','2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11']

beamperiod = [[datetime(2018,9,20,18,0,0),datetime(2018,9,26,8,0,0)],[datetime(2018,9,26,18,0,0),datetime(2018,10,3,8,0,0)],[datetime(2018,10,10,18,0,0),datetime(2018,10,17,8,0,0)],[datetime(2018,10,17,18,0,0),datetime(2018,10,18,8,0,0)],[datetime(2018,10,18,18,0,0),datetime(2018,10,24,8,0,0)],[datetime(2018,11,1,18,0,0),datetime(2018,11,7,8,0,0)],[datetime(2018,11,7,18,0,0),datetime(2018,11,12,8,0,0)]]

######################
### Beam Momentum:
######################

beamMom    = [0,7,7,1,1,0,0,1,1,0,0,1,1,2,2,1,1,0,0,6,6,3,3,0,0,1,1,7,7,1,1,2,2,0.5,0.5,0.3,0.3,0.5,0.5,0.3,0.3,1,1,0]

beamMom_ts = [datetime(2018,10,10,17,59,59),                                #0
              datetime(2018,10,10,18,0,0),datetime(2018,10,12,8,29,59),     #7
              datetime(2018,10,12,8,30,0),datetime(2018,10,17,7,59,59),     #1
              datetime(2018,10,17,8,0,0),datetime(2018,10,17,17,59,59),     #0
              datetime(2018,10,17,18,0,0),datetime(2018,10,18,7,59,59),     #1
              datetime(2018,10,18,8,0,0),datetime(2018,10,18,17,59,59),     #0
              datetime(2018,10,18,18,0,0),datetime(2018,10,19,7,59,59),     #1
              datetime(2018,10,19,8,0,0),datetime(2018,10,23,11,29,59),     #2
              datetime(2018,10,23,11,30,0),datetime(2018,10,24,7,59,59),    #1
              datetime(2018,10,24,8,0,0),datetime(2018,11,1,17,59,59),      #0
              datetime(2018,11,1,18,0,0),datetime(2018,11,4,10,59,59),      #6
              datetime(2018,11,4,11,0,0),datetime(2018,11,7,7,59,59),       #3
              datetime(2018,11,7,8,0,0),datetime(2018,11,7,17,59,59),       #0
              datetime(2018,11,7,18,0,0),datetime(2018,11,8,16,59,59),      #1
              datetime(2018,11,8,17,0,0),datetime(2018,11,8,18,59,59),      #7
              datetime(2018,11,8,19,0,0),datetime(2018,11,9,7,59,59),       #1
              datetime(2018,11,9,8,0,0),datetime(2018,11,9,22,59,59),       #2
              datetime(2018,11,9,23,0,0),datetime(2018,11,10,14,59,59),     #0.5
              datetime(2018,11,10,15,0,0),datetime(2018,11,11,3,39,59),     #0.3
              datetime(2018,11,11,4,0,0),datetime(2018,11,11,14,29,59),     #0.5
              datetime(2018,11,11,14,30,0),datetime(2018,11,11,21,59,59),   #0.3
              datetime(2018,11,11,22,00,0),datetime(2018,11,12,7,59,59),    #1
              datetime(2018,11,12,8,0,0)]

# accumulated beam triggers:

trigCount = []
trig_ts   = []
Ntrig     = 0.

ROOTDIR = os.environ["NP04BRSROOT"]

#with open(ROOTDIR + '/data/TIMBER_DATA_newtriggers.csv',newline='') as trigFile:
with open(ROOTDIR + '/data/TIMBER_DATA_alltriggers-DAQaddedNov1.csv',newline='') as trigFile:
    reader = csv.reader(trigFile,delimiter=',')
    lineNum=0
    for row in reader:
        lineNum+=1
        if lineNum>1:
            t = datetime.strptime(str(row[0]),'%Y-%m-%d %H:%M:%S.%f')
            t = t + timedelta(0,3600)       # UTC --> CET
            trig = float(row[2])
            Ntrig = Ntrig + trig
            trigCount.append(Ntrig)
            trig_ts.append(t)

aqTrigCount = []
aqTrig_ts   = []
NaqTrig     = 0.

with open(ROOTDIR + '/data/DAQ-runlist.csv',newline='') as f:
    reader = csv.reader(f,delimiter=',')
    for row in reversed(list(reader)):
        endString = row[3]
        endString = endString[:-4]
        endDAQ = datetime.strptime(endString, '%a, %d %b %Y %H:%M:%S')
        if endDAQ < datetime(2018,11,12,10,0,0) and not (str(row[1]) == 'commissioning' or str(row[1]) == 'calibration'):
            NaqTrig = NaqTrig + float(row[4])
            aqTrigCount.append(NaqTrig)
            aqTrig_ts.append(endDAQ) 


######################
### Lifetime:
######################

etau     = []
etau_ts  = []
contam   = []

with open(ROOTDIR + '/data/prm_Top_lifetime_data.csv',newline='') as purFile:
    reader = csv.reader(purFile,delimiter=',')
    lineNum=0
    for row in reader:
        lineNum+=1
        if lineNum>1:
            t = datetime.strptime(str(row[0]),'%Y-%m-%d %H:%M:%S.%f')
            lt = float(row[1])
            cont = (1./lt)*(0.1*3.)
            etau.append(lt)
            etau_ts.append(t)
            contam.append(cont)

######################
### Electric Field:
#######################

plotEField = True
eField = []
secBins = []

if plotEField:

    beginning = datetime.strptime(datelist[0]+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    ending = datetime.strptime(datelist[-1]+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    #beginning = beginning + timedelta(1,10)
    ending = ending + timedelta(1,7258)

    tempSB  = []
    temp = beginning

    while temp < (ending+timedelta(0,1)):
        #print(temp)
        tempSB.append(temp)
        temp = temp + timedelta(0,1)
    #add the last bin
    tempSB.append(temp)

    df = pd.DataFrame(index=tempSB,columns=['sumCurr','Ncurr','sumVolt','Nvolt'])
    df = df.fillna(0.)

    # Fill data into panda tables to bin into seconds

    for d in datelist:
        inFile = ROOTDIR + '/data/heinzCurr_' + d + '.csv'
        with open(inFile,newline='') as f:
            reader = csv.reader(f,delimiter=' ')
            for row in reader:
                time = float(row[0])/1e3   #in seconds
                #t = datetime.fromtimestamp(time)
                t = datetime.utcfromtimestamp(time) + timedelta(hours=1)
                #print(t)
                c = float(row[1])
                df.at[t,'sumCurr'] = df.at[t,'sumCurr'] + c
                df.at[t,'Ncurr'] = df.at[t,'Ncurr'] + 1

    for d in datelist:
        inFile = ROOTDIR + '/data/heinzVolt_' + d + '.csv'
        with open(inFile,newline='') as f:
            reader = csv.reader(f,delimiter=' ')
            for row in reader:
                time = float(row[0])/1e3   #in seconds
                #t = datetime.utcfromtimestamp(time)
                t = datetime.utcfromtimestamp(time) + timedelta(hours=1)
                #print(t)
                v = float(row[1])
                df.at[t,'sumVolt'] = df.at[t,'sumVolt'] + v
                df.at[t,'Nvolt'] = df.at[t,'Nvolt'] + 1

    print(df)

    # make HV stability cuts and calculate %uptime

    streamerON = False
    cutONperiod = []
    up_bins = []
    upTime  = []
    upSecCount  = 0.
    totSecCount = 0.
    binSize = 12   #hours
    upSC_list = [0.]*12

    b1 = datetime(2018,10,5,0,0,0)
    b2 = datetime(2018,10,17,12,0,0)

    # make HV cut decisions and write to file

    HVcutFile = ROOTDIR + '/data/np04-HVcutPeriods.csv'

    with open(HVcutFile, mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        for b in tempSB:
            if not (df.at[b,'Nvolt'] == 0. or df.at[b,'Ncurr'] == 0.):
                vps = df.at[b,'sumVolt']/df.at[b,'Nvolt']
                cps = df.at[b,'sumCurr']/df.at[b,'Ncurr']
                e = (vps - 97.*cps)/360.
                r = vps/cps
                eField.append(e)
                secBins.append(b)
                # piecewise cut on resistance
                if b <= b1 and (r > 1472 or r < 1452 or vps < 120000.) and not streamerON:
                    streamerON = True
                    startStream = b
                if b <= b1 and (r > 1452 and r < 1472 and vps > 120000.) and streamerON:
                    streamerON = False
                    cutONperiod.append([startStream-timedelta(0,2),b+timedelta(0,2)])
                    writer.writerow([int(pytime.mktime((startStream-timedelta(0,2)).timetuple())),int(pytime.mktime((b+timedelta(0,2)).timetuple()))])

                if b > b1 and b < b2 and (r < 1465 or vps < 120000.) and not streamerON:
                    streamerON = True
                    startStream = b
                if b > b1 and b < b2 and (r > 1465 and vps > 120000.) and streamerON:
                    streamerON = False
                    cutONperiod.append([startStream-timedelta(0,2),b+timedelta(0,2)])
                    writer.writerow([int(pytime.mktime((startStream-timedelta(0,2)).timetuple())),int(pytime.mktime((b+timedelta(0,2)).timetuple()))])
 
                if b >= b2 and (r < 1465 or vps < 180000.) and not streamerON:
                    streamerON = True
                    startStream = b
                if b >= b2 and (r > 1465 and vps > 180000.) and streamerON:
                    streamerON = False
                    cutONperiod.append([startStream-timedelta(0,2),b+timedelta(0,2)]) 
                    writer.writerow([int(pytime.mktime((startStream-timedelta(0,2)).timetuple())),int(pytime.mktime((b+timedelta(0,2)).timetuple()))])
            totSecCount = totSecCount + 1.
            if not streamerON:
                upSecCount = upSecCount + 1.
            #if totSecCount >= timedelta(hours=binSize).total_seconds():
            if totSecCount >= timedelta(hours=1).total_seconds():
                #ut = 100*upSecCount/totSecCount
                for i in range(12):
                    upSC_list[i] = upSC_list[i] + upSecCount
                ut = 100.*upSC_list[11]/timedelta(hours=12).total_seconds()
                upTime.append(ut)
                up_bins.append(b-timedelta(hours=int(binSize/2)))
                for a in range(11):
                    upSC_list[11-a] = upSC_list[10-a]
                upSC_list[0]=0.
                totSecCount = 0.
                upSecCount = 0.

        if streamerON:
            cutONperiod.append([startStream-timedelta(0,2),tempSB[-1]+timedelta(0,2)])
            writer.writerow([int(pytime.mktime((startStream-timedelta(0,2)).timetuple())),int(pytime.mktime((b+timedelta(0,2)).timetuple()))])

else:
    secBins = [datetime(2018,9,17,0,0,0),datetime(2018,11,12,8,0,0)]
    eField  = [0.,0.]

#########################
### Plotting:
#########################

# make the figure and organize the different panels of the plot

fig = plt.figure(figsize=(15, 8))
grid = gridspec.GridSpec(ncols=1,nrows=5,figure=fig,height_ratios=[2,1.5,1.5,0.2,1.5])

fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

a2 = fig.add_subplot(grid[2,0])                            # a2:   electric field
a4 = fig.add_subplot(grid[4,0],sharex=a2)                  # a3:   HV uptime
a3 = fig.add_subplot(grid[3,0],xticklabels=[],sharex=a2)   # a3:   HV stat
a1 = fig.add_subplot(grid[1,0],xticklabels=[],sharex=a2)   # a1:   e- lifetime
a0 = fig.add_subplot(grid[0,0],xticklabels=[],sharex=a2)   # a0:   beam momentum
a0_0 = a0.twinx()                                          # a0_0: trigger count

a0.set_ylabel('Beam Momentum\n[GeV/c]',color='black')
a0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a0.grid(color='grey',linestyle='--',linewidth=0.5)
a0.tick_params(labelbottom=False)

a0_0.set_ylabel('Beam Trigger Count',color='blue')
a0_0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a0_0.tick_params(axis='y',colors='blue',labelcolor='blue')
a0_0.tick_params(labelbottom=False)

# chose if you want the purity monitor data expressed in terms of
# contamination (plotContamination = True) or lifetime (plotContamination = False)

plotContamination = True
#plotContamination = False

if not plotContamination:
    a1.set_ylabel('e- lifetime\n[ms]',color='darkviolet')
    a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1.tick_params(axis='y',colors='darkviolet',labelcolor='darkviolet')
    a1.grid(color='grey',linestyle='--',linewidth=0.5)
    a1.set_ylim(-0.5,6.5)
    a1.spines['left'].set_color('darkviolet')
    a1.tick_params(labelbottom=False)

else:
    a1.set_ylabel('Contamination\n'+ r'[ppb O$^{2}$ equiv.]',color='darkviolet')
    a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1.tick_params(axis='y',which='both',colors='darkviolet',labelcolor='darkviolet')
    a1.grid(color='grey',linestyle='--',linewidth=0.5)
    #a1.xaxis_date()
    a1.tick_params(labelbottom=False)

    a1_1 = a1.twinx()
    a1_1.tick_params(labelbottom=False,labeltop=False)
    a1_1.set_ylabel('e- lifetime\n[ms]',color='darkviolet')
    a1_1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1_1.tick_params(axis='y',which='both',colors='darkviolet',labelcolor='darkviolet')
    a1_1.spines['left'].set_color('darkviolet')
    a1_1.spines['right'].set_color('darkviolet')
    #a1_1.xaxis_date()

# cosmetics...

a2.set_ylabel('Drift Field\n[V/cm]',color='red')
a2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a2.tick_params(axis='y',colors='red',labelcolor='red')
a2.grid(color='grey',linestyle='--',linewidth=0.5)
a2.spines['left'].set_color('red')
a2.set_ylim(-30.,630.)
a2.tick_params(labelbottom=False,left=False)

a3.set_ylabel('HV Status',rotation='horizontal',labelpad=30,va='center')
a3.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
#a3.yaxis.labelpad = 50
a3.tick_params(labelbottom=False,left=False,labelleft=False)
a3.grid(axis='x',color='grey',linestyle='--',linewidth=0.5)

a4.set_ylabel('HV 12-hour Uptime\n[%]',color='navy')
a4.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a4.tick_params(axis='y',colors='navy',labelcolor='navy')
a4.grid(color='grey',linestyle='--',linewidth=0.5)
a4.spines['left'].set_color('navy')
a4.tick_params(axis='x', rotation=90)

rect1 = patches.Rectangle((0.2,1.05),0.1,0.1,clip_on=False,facecolor='green',edgecolor='green',alpha=0.2,transform=a0.transAxes)
a0.add_patch(rect1)
a0.text(0.32, 1.07,'Beam ON',transform=a0.transAxes)
rect2 = patches.Rectangle((0.6,1.05),0.1,0.1,clip_on=False,facecolor='salmon',edgecolor='salmon',alpha=0.2,transform=a0.transAxes)
a0.add_patch(rect2)
a0.text(0.72, 1.07,'Beam OFF',transform=a0.transAxes)

# plot the data

a2.plot_date(secBins,eField,color='red',markersize=0.15)
a0.plot(beamMom_ts,beamMom,linewidth=3,markersize=3,color='black')
BItrig  = a0_0.plot_date(trig_ts,trigCount,color='blue',markersize=0.,linestyle='solid')
DAQtrig = a0_0.plot_date(aqTrig_ts,aqTrigCount,color='blue',markersize=0.,linestyle='dashed')
a4.plot_date(up_bins,upTime,color='navy',markersize=0.3,linestyle='solid')
if plotContamination:
    a1.plot_date(etau_ts,contam,linestyle='None',color='darkviolet',marker='o',markersize=3)
    a1_1.plot_date(etau_ts,contam,linestyle='None',color='darkviolet',marker='o',markersize=3)
    a1_1.plot_date(etau_ts,contam,linestyle='None',color='darkviolet',marker='o',markersize=0.)
    a1.set_yscale("log")
    a1_1.set_yscale("log")
    a1_bot, a1_top = a1.get_ylim()
    a1_1.set_ylim(bottom=a1_bot,top=a1_top)
    #a1.set_yticks([0.05,0.3,0.5,3.0])
    from matplotlib.ticker import FuncFormatter
    def format_fn(tick_val, tick_pos):
        #tick_val = contamination
        et = (1./tick_val)*(0.1*3.)
        return "{0:0.1f}".format(et)
    def minorFormat_fn(tick_val, tick_pos):
        #tick_val = contamination
        et = (1./tick_val)*(0.1*3.)
        if tick_val in [0.05,0.1,0.5,1.,5,] and et > 0.1:
            return "{0:0.1f}".format(et)
        elif tick_val in [0.05,0.1,0.5,1.,5,] and et < 0.1:
            return "{0:0.2f}".format(et)
        else:
            return ''

    a1_1.yaxis.set_major_formatter(FuncFormatter(format_fn))
    a1_1.yaxis.set_minor_formatter(FuncFormatter(minorFormat_fn))

else:
    a1.plot(etau_ts,etau,linestyle='None',color='darkviolet',marker='o',markersize=3)
    a1.set_yticks([0,1,2,3,4,5,6])

# cosmetics done after plotting

a0_0.legend((BItrig[0], DAQtrig[0]), ('BI Trigger Count', 'DAQ Trigger Count'))
a0_0.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
a0_0.set_yticks([0,1000000,2000000,3000000,4000000,5000000,6000000])
a2.set_xlim(secBins[0],secBins[-1])
a0.set_yticks([0,1,2,3,4,5,6,7])
a4.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
#a4.xaxis.set_major_locator(plt.MaxNLocator(6))
a2.set_yticks([0,100,200,300,400,500,600])

# make a tick every day

days = mdates.DayLocator()
a0.xaxis.set_major_locator(days)
a1.xaxis.set_major_locator(days)
a2.xaxis.set_major_locator(days)
a3.xaxis.set_major_locator(days)
a4.xaxis.set_major_locator(days)

# paint beam-on and beam-off periods on background

a0.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)
a1.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)
a2.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)
a4.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)

for period in beamperiod:
    a0.axvspan(period[0],period[1],facecolor='green',alpha=0.2)
    a1.axvspan(period[0],period[1],facecolor='green',alpha=0.2)
    a2.axvspan(period[0],period[1],facecolor='green',alpha=0.2)
    a4.axvspan(period[0],period[1],facecolor='green',alpha=0.2)

#########################
### Streamer Periods:
#########################

a3.axvspan(secBins[0],secBins[-1], facecolor='green')

for cut in cutONperiod:
    a3.axvspan(cut[0],cut[1], facecolor='red')

#########################
### Data Taking Periods:
#########################

#TODO: CHECK TIME ZONE IS HANDLED CORRECTLY!!!

#a3.axvspan(secBins[0],secBins[-1],facecolor='salmon')

#with open(ROOTDIR + '/data/DAQ-runlist.csv',newline='') as f:
#    reader = csv.reader(f,delimiter=',')
#    for row in reader:
#        startString = row[2]
#        startString = startString[:-4]
#        startDAQ = datetime.strptime(startString, '%a, %d %b %Y %H:%M:%S')
#        endString = row[3]
#        endString = endString[:-4]
#        endDAQ = datetime.strptime(endString, '%a, %d %b %Y %H:%M:%S')
#        runType = str(row[1])
#        if runType == "physics":
#            a3.axvspan(startDAQ,endDAQ,facecolor='green',alpha=0.5)
#        if runType == "cosmics":
#            a3.axvspan(startDAQ,endDAQ,facecolor='blue',alpha=0.5)
#        else:
#            a3.axvspan(startDAQ,endDAQ,facecolor='purple',alpha=0.5)

########################

print('run time [s]')
print(datetime.now() - startTime)
#plt.tight_layout(pad=0)
#plt.savefig(ROOTDIR + '/output/beamRunSummary.eps', format='eps', dpi=1200)
#plt.savefig(ROOTDIR + '/output/beamRunSummary.svg', format='svg', dpi=1200)
#plt.savefig(ROOTDIR + '/output/beamRunSummary.pdf', format='pdf', dpi=1200)
#plt.savefig(ROOTDIR + '/output/beamRunSummary.png', format='png', dpi=1200)
#plt.savefig(ROOTDIR + '/output/beamRunSummary.ps', format='ps', dpi=1200)
plt.show()
