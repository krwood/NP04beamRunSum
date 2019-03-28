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
from itertools import islice
from datetime import timedelta
import pandas as pd
import os

# TODO:
#  - only plot data during data taking periods
#  - add a pannel with "8-hour uptime [%]"

startTime = datetime.now()
ROOTDIR = os.environ["NP04BRSROOT"]

datelist = ['2019-02-09','2019-02-10','2019-02-11']
#datelist = ['2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01']
#datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11']
#datelist = ['2018-09-14','2018-09-15','2018-09-16','2018-09-17','2018-09-18','2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07']

beamperiod = [[datetime(2018,9,20,18,0,0),datetime(2018,9,26,8,0,0)],[datetime(2018,9,26,18,0,0),datetime(2018,10,3,8,0,0)],[datetime(2018,10,10,18,0,0),datetime(2018,10,17,8,0,0)],[datetime(2018,10,17,18,0,0),datetime(2018,10,18,8,0,0)],[datetime(2018,10,18,18,0,0),datetime(2018,10,24,8,0,0)],[datetime(2018,11,1,18,0,0),datetime(2018,11,7,8,0,0)],[datetime(2018,11,7,18,0,0),datetime(2018,11,12,6,0,0)]]

beginning = datetime.strptime(datelist[0]+' 00:00:00', '%Y-%m-%d %H:%M:%S')
ending = datetime.strptime(datelist[-1]+' 00:00:00', '%Y-%m-%d %H:%M:%S')
#beginning = beginning + timedelta(1,10)
ending = ending + timedelta(1,3599)

secBins = []
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
            t = datetime.fromtimestamp(time)
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
            t = datetime.fromtimestamp(time)
            #print(t)
            v = float(row[1])
            df.at[t,'sumVolt'] = df.at[t,'sumVolt'] + v
            df.at[t,'Nvolt'] = df.at[t,'Nvolt'] + 1

print(df)

eField = []
res    = []

for bin in tempSB:
    if not (df.at[bin,'Nvolt'] == 0. or df.at[bin,'Ncurr'] == 0.):
        vps = df.at[bin,'sumVolt']/df.at[bin,'Nvolt']
        cps = df.at[bin,'sumCurr']/df.at[bin,'Ncurr']
        e = (vps - 97.*cps)/360.
        r = vps/cps
        secBins.append(bin)
        eField.append(e) 
        res.append(r)

fig = plt.figure(figsize=(6, 8))
fig.subplots_adjust(left=0.06, bottom=0.15, right=0.94, top=0.93, wspace=None, hspace=0.)
grid = gridspec.GridSpec(ncols=1,nrows=2,figure=fig,height_ratios=[1,1])
a0 = fig.add_subplot(grid[1,0])                              # electric field
#a0.xaxis_date()
a1 = fig.add_subplot(grid[0,0],xticklabels=[],sharex=a0)    # resistance

a0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d %H:%M:%S"))
a0.set_ylabel('Electric Field [V/cm]',color='red')
a0.tick_params(axis='y',colors='red',labelcolor='red')
a0.grid(color='grey',linestyle='--',linewidth=0.5)
a0.xaxis.set_tick_params(rotation=90)
a0.tick_params(axis='x', rotation=90)
a0.set_ylim(-10.,550.)

a1.set_ylabel('Resistance [Mohm]',color='blue')
a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d %H:%M:%S"))
a1.tick_params(axis='y',colors='blue',labelcolor='blue')
a1.grid(color='grey',linestyle='--',linewidth=0.5)
#a1.set_ylim(-50.,210.)
a1.spines['left'].set_color('blue')
a1.tick_params(labelbottom=False)

rect1 = patches.Rectangle((0.2,1.075),0.1,0.1,clip_on=False,facecolor='green',edgecolor='green',alpha=0.2,transform=a1.transAxes)                                                                 
a1.add_patch(rect1)
a1.text(0.32, 1.075,'Beam ON',transform=a1.transAxes)
rect2 = patches.Rectangle((0.6,1.075),0.1,0.1,clip_on=False,facecolor='salmon',edgecolor='salmon',alpha=0.2,transform=a1.transAxes)
a1.add_patch(rect2)
a1.text(0.72, 1.075,'Beam OFF',transform=a1.transAxes)

a0.plot_date(secBins,eField,color='red',markersize=0.15)
a1.plot(secBins,res,linestyle='None',color='olive',marker='o',markersize=0.15)
a0.set_xlim(secBins[0],secBins[-1])

#days = mdates.DayLocator()
#a0.xaxis.set_major_locator(days)

a0.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)
a1.axvspan(secBins[0],secBins[-1],facecolor='salmon',alpha=0.2)

for period in beamperiod:
    a0.axvspan(period[0],period[1], facecolor='green', alpha=0.2)
    a1.axvspan(period[0],period[1], facecolor='green', alpha=0.2)

print('run time [s] = ')
print(datetime.now() - startTime)
plt.show()
