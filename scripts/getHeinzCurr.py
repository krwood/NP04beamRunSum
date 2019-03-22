#***********************************************************************
#
# Kevin Wood; November, 2018
#
# - Meant to be run with python v2:
#     >> cd /path/to/NP04beamRunSum
#     >> source setup.sh                 # sets NP04BRSROOT variable
#     >> python scripts/getHeinzCurr.py
#
# - Needs to be run from within the CERN network
#
#***********************************************************************

import urllib, json
import csv
import pandas
import os

# use python2

# choose list of days for which you would like to retrieve information

#datelist = ['2018-09-14','2018-09-15','2018-09-16','2018-09-17','2018-09-18']
#datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24']
#datelist = ['2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01']
#datelist = ['2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08']
#datelist = ['2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15']
#datelist = ['2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22']
#datelist = ['2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29']
#datelist = ['2018-10-30','2018-10-31','2018-11-01']
#datelist = ['2018-11-02','2018-11-03','2018-11-04']
#datelist = ['2018-11-09','2018-11-10','2018-11-11']
datelist = ['2018-11-12']

ROOTDIR = os.environ["NP04BRSROOT"]

for date in datelist:
    url = "http://epdtdi-vm-01.cern.ch:5000/day/" + date + "/47894757376282"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    outfile = ROOTDIR + "/data/heinzCurr_" + date + ".csv"
    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for dat in data:
            for da in dat:
                writer.writerow(da)

