#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:43:09 2021

@author: Ava Sherry
"""
from typing import List, Any, Union

import can
import cantools
import mdfreader
import pandas
import numpy as np
import matplotlib.pyplot as plt

import sys

sys.path.append('../')
import LyftCAN
import time


# %% Load CAN Dataframe

def summaryFWD():
    dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
    # asc_filename = '/Users/asherry/Desktop/TestRideData/VAL/logfile010.asc'
    asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL13_100km/logfile2021-01-27_10-05-12.asc'
    can_logs = LyftCAN.ascToDataframe(asc_filename, dbc_filename)
    can_log_by_signal = can_logs['canlogs_by_signal']


    for signal in can_log_by_signal:
        count = 0
        s = signal.split("_")  ## "MC_f032_TorqueInputRationality" --> ["MC", "f032", "TorqueInputRationality"]
        if s[1][0] in ['w', 'f', 'd']:  ## is the signal in a fault/warning/diagnostic matrix (ex. MC_w001)
            log = can_log_by_signal[signal]
            for y in range(0, len(log)):
                if log.Object[y] == 1:
                    count += 1
            if count >= 1:
                print(str(count) + " :" + signal)


# input2 = input('Decode? (y/n) ')
# if input2 == 'y':
# inputVAL1 = input('Which faults are you interested in (MC/BMS)? ')
# else:


input3 = input('Summary? (y/n) ')
if input3 == 'y':
    start_time = time.time()
    summaryFWD()
    print("My program took", time.time() - start_time, " seconds to run")

