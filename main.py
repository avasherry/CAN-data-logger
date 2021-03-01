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
    asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL13_100km/logfile2021-01-27_03-32-34.asc'
    # asc_filename = '/Users/asherry/Desktop/Thien-Ride-20210218_1600_CAN.asc'
    db = cantools.database.load_file(dbc_filename)

    filteredSignals = ["MC_DiagnosticMatrix", "MC_FaultMatrix", "MC_WarningMatrix", "BMS_DiagnosticMatrix", "BMS_FaultMatrix", "BMS_WarningMatrix"]
    filteredMsgID = set()

    for signal in filteredSignals:
        msg = db.get_message_by_name(signal)
        filteredMsgID.add(msg.frame_id)


    can_logs = LyftCAN.ascToDataframe(asc_filename, dbc_filename, filteredMsgID)
    can_log_by_signal = can_logs['canlogs_by_signal']

    for signal in can_log_by_signal:
        count = 0
        log = can_log_by_signal[signal]
        for y in range(0, len(log)):
            if log.Object[y] == 1:
                count += 1
        if count >= 1:
            print(str(count) + " :" + signal)


input1 = input('Summary? (y/n) ')
if input1 == 'y':
    summaryFWD()

