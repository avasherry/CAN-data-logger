import LyftCAN
import can
import cantools
import mdfreader
import pandas
import numpy as np
import matplotlib.pyplot as plt

import sys

def decodeCAN(filepath):
    dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
    asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/' + filepath + '.asc'
    can_logs = LyftCAN.ascToDataframe(asc_filename, dbc_filename)
    can_log_by_signal = can_logs['canlogs_by_signal']



    can_logs.to_pickle('/Users/asherry/Desktop/DecodedFiles/REL13_8km/logfile2021-01-19_07-00-34')


decodeCAN('REL13_8km/logfile2021-01-19_07-00-34')
