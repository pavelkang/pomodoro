##
# Receives a list of Access Point data in string format from an Android phone, reads standard data from RSSIS_GHC7.csv, compares them to estimate the location of the phone.
# Author: Kai Kang
##

import csv
from util import notAllInf, stripInf, Bssid, plotBssids

def readStandard(filename="RSSIS_GHC7.csv"):
    """ Reads data from RSSIS_GHC7.csv. Returns (BSSID_LIST, RSSI_LIST,  AREA_LIST) """
    BSSID_LIST = []
    RSSI_LIST = []
    AREA_LIST = []
    csvreader = csv.DictReader( open( filename, 'r' ) )
    for row in csvreader:
        BSSID_LIST.append(row["BSSID"])
        RSSI_LIST.append(row["rssi_med"])
        AREA_LIST.append(row["area"])
    assert(len(BSSID_LIST)==len(RSSI_LIST))
    assert(len(RSSI_LIST) ==len(AREA_LIST))
    return (BSSID_LIST, RSSI_LIST,  AREA_LIST)


def processRaw(raw_samples):
    """
    Process the raw data (a list of AP) in string format (separated by comma)
    Returns a list of format [{'bssid':xxx, 'rssi':xxx}....]
    """
    samples = []
    for i in xrange(len(raw_samples)):
        sample = dict()
        raw_sample_space = raw_samples[i].split(',')
        raw_sample = []
        for i in raw_sample_space:
            raw_sample.append( i.strip() ) # strip spaces
        for e in raw_sample:
            if e.startswith('BSSID'):
                sample['bssid'] = str(e[e.index(':')+1:][1:])
            if e.startswith('level'):
                sample['rssi'] = str(e[e.index(':')+1:][1:])
        samples.append(sample)
    while dict() in samples: # remove empty dictionaries
        samples.remove(dict())
    return samples


def calc(samples_list, bssid_list, rssi_list, area_list):
    """ Returns a list of lists of [ (a, d), (a, d), ... ] """
    inf = float("inf")
    ERRORS_LIST = []
    for sample in samples_list:
        sample_error = []
        sample_bssid, sample_rssi = sample['bssid'], sample['rssi']
        for bssid_index in xrange(len(bssid_list)):
            area = area_list[bssid_index]
            if bssid_list[bssid_index] == sample_bssid:
                dif = abs(float(sample_rssi)-float(rssi_list[bssid_index]))
                sample_error.append( (area, dif) )
            else:
                sample_error.append( (area, inf) )
        ERRORS_LIST.append( (sample_bssid, sample_error) )
    return ERRORS_LIST


def prettyPrint(l):
    """ Print [(bssid:error_list), (bssid:error_list) ...}] in nicer format for debugging purpose """
    for tup in l:
        print tup[0],
        noOfInf = 0
        for error in tup[1]:
            if error[1] == float('inf'):
                noOfInf += 1
            else:
                print error,
        print "\ninf:%d" %(noOfInf)

def getAllNonInf(l):
    """
    Keep only the non-inf entries
    """
    allNonInf = []
    for tup in l:
        if notAllInf(tup[1]):
            allNonInf.append( (tup[0], stripInf(tup[1])) )
    return allNonInf

def plot(choice=0):
    x = []
    for i in getAllNonInf(errors_list):
        x.append(Bssid(i))
    if choice == 0:
        pass

def algo(errors_list):
    """ Returns the best estimated area in the format of (x, y)"""
    # TODO
    return "YES"


def main(info):
    # 1. Get SAMPLES_LIST in the format of [ {'bssid':xxx, 'rssi':xxx} ... ]
    try:
        SAMPLES_LIST = processRaw(str(info).splitlines())
        # the number of samples should be equal to the number of bssids
        assert(len(SAMPLES_LIST) == info.count("BSSID"))
    except:
        return "Wrong Input Data Format !!!"
    # 2. Read the standard csv
    try:
        (BSSID_LIST, RSSI_LIST, AREA_LIST) = readStandard()
    except:
        return "Read standard file error !!!"
    # 4. Get errors list
    try:
        errors_list = calc(SAMPLES_LIST, BSSID_LIST, RSSI_LIST, AREA_LIST)
    except Exception as e:
        return "error list processing ERROR %s" %(str(e))
    x = []
    for i in getAllNonInf(errors_list):
        x.append(Bssid(i))
    try:
        result = plotBssids(x, False)
    except Exception as e:
        print str(e)
    str_result = "%d,%d" %(result[0], result[1])
    print ">>> Calculated result is %s" %(str_result)

    return str_result
