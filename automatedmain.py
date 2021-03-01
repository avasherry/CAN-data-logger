#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:43:09 2021

@author: Ava Sherry
"""
import io
from typing import List, Any, Union

import can
import cantools
import mdfreader
import pandas
import numpy as np
import matplotlib.pyplot as plt
import sys
import io
import openpyxl

sys.path.append('../')
import LyftCAN
from pandas import ExcelWriter


# %% Load CAN Dataframe


def summaryFWD():
    dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
    asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL6_150km/'
    db = cantools.database.load_file(dbc_filename)
    # index = ['logfile2021-01-19_07-00-34.asc', 'logfile2021-01-19_07-02-26.asc', 'logfile2021-01-19_07-02-48.asc']
    index = ['logfile2021-01-21_09-28-56.asc', 'logfile2021-01-24_03-07-46.asc']
    # index = ['logfile2021-01-25_02-35-28.asc', 'logfile2021-01-24_08-38-50.asc', 'logfile2021-01-24_03-03-54.asc', 'logfile2021-01-21_07-46-10.asc']

    data = []
    columns = []

    filteredSignals = ["MC_DiagnosticMatrix", "MC_FaultMatrix", "MC_WarningMatrix", "BMS_DiagnosticMatrix",
                       "BMS_FaultMatrix", "BMS_WarningMatrix"]
    filteredMsgID = set()

    for signal in filteredSignals:  ## fill filteredMsgID with hex values of signals
        msg = db.get_message_by_name(signal)
        filteredMsgID.add(msg.frame_id)

    # Fill data array for each log
    for a in range(0, len(index)):

        can_logs = LyftCAN.ascToDataframe(asc_filename + index[a], dbc_filename, filteredMsgID)
        can_log_by_signal = can_logs['canlogs_by_signal']
        d = []

        if a == 0: ## if this is the first log in the array
            for signal in can_log_by_signal:
                columns.append(signal) ## fill the columns array with signal names
        for signal in columns:
            count = 0
            log = can_log_by_signal[signal]
            if len(log) != 0:
                for y in range(0, len(log)):
                    count += log.Object[y]
            d.append(count)
        data.append(d)

    df = pandas.DataFrame(data, index, columns)
    with ExcelWriter('test2.xlsx') as writer:
        df.to_excel(writer)


input1 = input('Summary? (y/n) ')
if input1 == 'y':
    summaryFWD()
