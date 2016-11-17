# Functions for standardizing landscape rasters, allocating landscape metrics to NHDPlusV2
# catchments, accumulating metrics for upstream catchments, and writing final landscape metric tables
# Authors: Marc Weber<weber.marc@epa.gov>, Ryan Hill<hill.ryan@epa.gov>,
#          Darren Thornbrugh<thornbrugh.darren@epa.gov>, Rick Debbout<debbout.rick@epa.gov>,
#          and Tad Larsen<laresn.tad@epa.gov>
#          __                                       __
#    _____/ /_________  ____  ____ ___  _________ _/ /_
#   / ___/ __/ ___/ _ \/ __ `/ __ `__ \/ ___/ __ `/ __/
#  (__  ) /_/ /  /  __/ /_/ / / / / / / /__/ /_/ / /_
# /____/\__/_/   \___/\__,_/_/ /_/ /_/\___/\__,_/\__/
#
# Date: October 2015

# load modules

import numpy as np
import pandas as pd
import pysal as ps
from collections import OrderedDict
##############################################################################


def findUpstreamNpy(zone, com, numpy_dir):
    '''
    __author__ =  "Rick Debbout <debbout.rick@epa.gov>"
    Creates an OrderedDict for looping through regions of the NHD RPU zones

    Arguments
    ---------
    zone                  : string of an NHDPlusV2 VPU zone, i.e. 10L, 16, 17
    com                   : COMID of NHD Catchment, integer
    numpy_dir             : directory where .npy files are stored
    '''
    comids = np.load(numpy_dir + '/comids' + zone + '.npy')
    lengths= np.load(numpy_dir + '/lengths' + zone + '.npy')
    upStream = np.load(numpy_dir + '/upStream' + zone + '.npy')
    itemindex = int(np.where(comids == com)[0])
    n = lengths[:itemindex].sum()
    arrlen = lengths[itemindex]
    return upStream[n:n+arrlen]

def makeVPUdict(directory):
    '''
    __author__ =  "Rick Debbout <debbout.rick@epa.gov>"
    Creates an OrderdDict for looping through regions of the NHD to carry InterVPU 
    connections across VPU zones

    Arguments
    ---------
    directory             : the directory contining NHDPlus data at the top level
    '''
    B = dbf2DF('%s/NHDPlusGlobalData/BoundaryUnit.dbf' % directory)
    B = B.drop(B.ix[B.DRAINAGEID.isin(['HI','CI'])].index, axis=0)
    B = B.ix[B.UNITTYPE == 'VPU'].sort_values('HYDROSEQ',ascending=False)
    inputs = OrderedDict()  # inputs = OrderedDict((k, inputs[k]) for k in order)
    for idx, row in B.iterrows():
        inputs[row.UNITID] = row.DRAINAGEID
        #print 'HydroRegion (value): ' + row.DRAINAGEID + ' in VPU (key): ' + row.UNITID
    np.save('%s/StreamCat_npy/zoneInputs.npy' % directory, inputs)
    return inputs
    
    
    
    
def dbf2DF(dbfile, upper=True):
    '''
    __author__ = "Ryan Hill <hill.ryan@epa.gov>"
                 "Marc Weber <weber.marc@epa.gov>"
    Reads and converts a dbf file to a pandas data frame using pysal.

    Arguments
    ---------
    dbfile           : a dbase (.dbf) file
    '''
    db = ps.open(dbfile)
    cols = {col: db.by_col(col) for col in db.header}
    db.close()  #Close dbf 
    pandasDF = pd.DataFrame(cols)
    if upper == True:
        pandasDF.columns = pandasDF.columns.str.upper() 
    return pandasDF