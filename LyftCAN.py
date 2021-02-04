#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 09:28:22 2019

@author: conradmurphy
"""

import cantools
import can
import pandas as pd


def blfToDataframe(blf_filename, dbc_filename, limit=0, msgWhitelist=None):
    log = can.BLFReader(blf_filename)
    if isinstance(dbc_filename, str):
        db = cantools.database.load_file(dbc_filename)
    elif isinstance(dbc_filename, list):
        db = cantools.database.load_file(dbc_filename[0])
        for fn in dbc_filename[1:]:
            db.add_dbc_file(fn)
    else:
        raise TypeError("input must be a string or list of strings")

    appended_dataframe = []
    # for counter, msg in enumerate(log):
    print("Starting to decode (%d records)\n" % (log.object_count))
    counter = 0
    for msg in log:
        counter = counter + 1
        if msgWhitelist is None or msg.arbitration_id in msgWhitelist:
            try:
                if len(msg.data) > 0:
                    decoded = db.decode_message(msg.arbitration_id, msg.data)
                    df = pd.DataFrame({'Timestamp': msg.timestamp,
                                       'Signal': list(decoded.keys()),
                                       'Object': list(decoded.values())})
                    appended_dataframe.append(df)
            except KeyError:
                # Message not in dbc, this is fine
                # print("Key Error %x\n" %(msg.arbitration_id))
                pass
            except:
                print("Unexpected error:", msg.arbitration_id, msg.data)
        if counter % 5000 == 0:
            print("Translated %d messages" % (counter))
        if limit and counter > limit:
            break

    can_log = pd.concat(appended_dataframe)
    can_log['Datetime'] = pd.to_datetime(can_log['Timestamp'], unit='s')

    print("Making MultiLog")
    can_log_multi = can_log.set_index(['Datetime', 'Signal'])
    can_log_multi = can_log_multi.drop(columns='Timestamp')

    # get a list of signals
    print("Making Per Signal Dataframe")
    signals = can_log.Signal.unique()
    can_log_by_signal = {}
    for signal in signals:
        can_log_by_signal[signal] = can_log[can_log.Signal == signal].set_index('Datetime')

    # Make Return Values
    canOut = {}
    canOut['canlog_df'] = can_log_multi
    canOut['signals'] = signals
    canOut['canlogs_by_signal'] = can_log_by_signal

    return canOut


def ascToDataframe(asc_filename, dbc_filename, msgWhitelist=None):
    keyErrDict = {}
    log = can.ASCReader(asc_filename)
    if isinstance(dbc_filename, str):
        db = cantools.database.load_file(dbc_filename)
    elif isinstance(dbc_filename, list):
        db = cantools.database.load_file(dbc_filename[0])
        for fn in dbc_filename[1:]:
            db.add_dbc_file(fn)
    else:
        raise TypeError("input must be a string or list of strings")

    appended_dataframe = []
    print("Starting to decode\n")
    counter = 0
    for msg in log:
        counter = counter + 1
        if msgWhitelist is None or msg.arbitration_id in msgWhitelist:
            try:
                decoded = db.decode_message(msg.arbitration_id, msg.data)
                df = pd.DataFrame({'Timestamp': msg.timestamp,
                                   'Signal': list(decoded.keys()),
                                   'Object': list(decoded.values())})
                appended_dataframe.append(df)
            except KeyError:
                if msg.arbitration_id not in keyErrDict:
                    print("Key Error, id: %d\n", msg.arbitration_id)
                    keyErrDict[msg.arbitration_id] = 1;
            except Exception as ex:
                pass
                '''
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message# print("Unexpected error:", msg.arbitration_id, msg.data) '''
        if counter % 5000 == 0:
            print("Translated %d messages" % (counter))

    print("Making Outputs\n")
    can_log = pd.concat(appended_dataframe)
    can_log['Datetime'] = pd.to_datetime(can_log['Timestamp'], unit='s')
    can_log_multi = can_log.set_index(['Datetime', 'Signal'])
    can_log_multi = can_log_multi.drop(columns='Timestamp')

    # get a list of signals
    signals = can_log.Signal.unique()
    can_log_by_signal = {}
    for signal in signals:
        can_log_by_signal[signal] = can_log[can_log.Signal == signal].set_index('Datetime')


    # Make Return Values
    canOut = {}
    canOut['canlog_df'] = can_log_multi
    canOut['signals'] = signals
    canOut['canlogs_by_signal'] = can_log_by_signal

    return canOut


def ascToString(asc_filename, CAN_ID=0x700):
    log = can.ASCReader(asc_filename)
    outputStr = ""
    for msg in log:
        if msg.arbitration_id == CAN_ID:
            outputStr += msg.data.decode("utf-8")
    return outputStr


''' Filter by time interval'''


def trimASC(inputFilename, outputFilename, start_ts, end_ts, header_lines=4):
    with open(inputFilename, 'r') as f_in:
        with open(outputFilename, 'w') as f_out:
            for ii in range(0, header_lines):
                f_out.write(f_in.readline())
            lines = f_in.readlines()
            for line in lines:
                ts = float(line.split()[0])
                if ts > start_ts and ts < end_ts:
                    f_out.write(line)


''' Filter by msgWhitelist '''


def filterASC(inputFilename, outputFilename, msgWhitelist, header_lines=4):
    with open(inputFilename, 'r') as f_in:
        with open(outputFilename, 'w') as f_out:
            for ii in range(0, header_lines):
                f_out.write(f_in.readline())
            lines = f_in.readlines()
            for line in lines:
                # ts = float(line.split()[0])
                # if ts>start_ts and ts<end_ts:
                f_out.write(line)


def blfToMatlab(blf_filename, dbc_filename, mat_filename):
    log = can.BLFReader(filename)
    db = cantools.database.load_file(dbc_path)

