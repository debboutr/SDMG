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
