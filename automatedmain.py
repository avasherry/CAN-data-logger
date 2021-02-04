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
    MC_fault = ['MC_f002_HwGateDriverFault', 'MC_f003_HwBusOvervoltage', 'MC_f012_BusOvervoltage',
                'MC_f013_BusUndervoltage', 'MC_f014_PhaseOvercurrent', 'MC_f016_BrakeResSelfTest',
                'MC_f017_TrqSafetySelfTest', 'MC_f028_RotorPosRationality', 'MC_f029_ThrottleRationality',
                'MC_f032_TorqueInputRationality', 'MC_f034_GateDriverConfig', 'MC_f047_FET_OT', 'MC_f050_MotorOT']
    MC_warning = ['MC_w001_EcuReset', 'MC_w004_HwFuse12V', 'MC_w005_HwFuseVbat', 'MC_w006_RailPower12V',
                  'MC_w007_RailPower5V', 'MC_w008_RefVoltage', 'MC_w009_BrakeResistorOverride',
                  'MC_w010_CurrentSensorOffset', 'MC_w011_IsolationLow', 'MC_w012_BusUndervoltage', 'MC_w015_OverSpeed',
                  'MC_w018_PowerAccounting', 'MC_w019_DcVoltRationality', 'MC_w020_DcCurrRationality',
                  'MC_w021_AcVoltRationality', 'MC_w022_AcCurrRationality', 'MC_w023_MotorTempRationality',
                  'MC_w024_FET_TempRationality', 'MC_w025_DcCapTempRationality', 'MC_w026_MicroTempRationality',
                  'MC_w027_BrakeResTempRationality', 'MC_w030_EncoderRationality', 'MC_w031_SpeedInputRationality',
                  'MC_w033_IsolationRationality', 'MC_w035_InertialUnitConfig', 'MC_w036_GateDriverSPI',
                  'MC_w037_ExtAdcSPI', 'MC_w038_InertialUnitSPI', 'MC_w039_ExtEepromSPI', 'MC_w040_SocMIA',
                  'MC_w041_PtMIA', 'MC_w042_BmsMIA', 'MC_w043_LossMotorControl', 'MC_w051_BrakeResOT',
                  'MC_w052_MicroOT', 'MC_w053_GateDriverThermalWarning', 'MC_w056_enableNotAllowed']
    MC_diagnostic = ['MC_d044_HighCpuUsage', 'MC_d045_OverrunISR', 'MC_d046_HighStackUsage', 'MC_d054_MotorClutchStuck']
    BMS_fault = ['BMS_f001_HW_CUV', 'BMS_f002_HW_COV', 'BMS_f003_HW_OCC', 'BMS_f004_HW_OCD', 'BMS_f005_HW_SCD',
                 'BMS_f006_HW_OTC', 'BMS_f007_HW_UTC', 'BMS_f008_HW_OTD', 'BMS_f009_HW_UTD', 'BMS_f010_HW_PF_CUV',
                 'BMS_f011_HW_PF_COV', 'BMS_f012_SW_PF_COT', 'BMS_f013_SW_PF_Voltage_Imbalance',
                 'BMS_f014_SW_PF_FET_Leakage', 'BMS_f015_SW_PF_FET_OT', 'BMS_f016_SW_CUV', 'BMS_f017_SW_COV',
                 'BMS_f018_SW_Cell_Overdischarged', 'BMS_f019_SW_Battery_UV', 'BMS_f020_SW_Battery_OV',
                 'BMS_f021_SW_OCC', 'BMS_f022_SW_OCD', 'BMS_f023_SW_OTC', 'BMS_f024_SW_OTD', 'BMS_f025_SW_UTC',
                 'BMS_f026_SW_UTD', 'BMS_f029_SW_Voltage_Imbalance', 'BMS_f030_SW_FET_OT', 'BMS_f031_HW_FET_OT',
                 'BMS_f032_SW_PF_AFE_MIA', 'BMS_f033_SW_Current_Sensor_MIA', 'BMS_f034_HW_2nd_Prot_Fault_Asserted',
                 'BMS_f037_SW_Low_Power_Bus_OCD', 'BMS_f038_bq796x0_Internal_PF',
                 'BMS_f039_bq796x0_Protection_Mismatch', 'BMS_f040_AFE_OTP_Memory_PF', 'BMS_f041_AFE_ROM_PF',
                 'BMS_f042_AFE_Internal_PF', 'BMS_f043_AFE_Commanded_PF', 'BMS_f044_AFE_Host_Watchdog',
                 'BMS_f046_AFE_Internal_UT', 'BMS_f047_AFE_Internal_OT', 'BMS_f048_SW_Pack_Voltage_Present',
                 'BMS_f049_SW_Predischarge_Fail_Short_Circuit', 'BMS_f050_SW_Predischarge_Fail_Voltage_Diff',
                 'BMS_f051_SW_Predischarge_Fail_Open_Circuit', 'BMS_f054_SW_TrickleChargeExceeded']
    BMS_warning = ['BMS_w001_SW_ECU_Reset', 'BMS_w002_SW_CAN_Integrity', 'BMS_w003_SW_12V_DCDC',
                   'BMS_w004_HW_12V_DCDC_Power_Good', 'BMS_w005_SW_Vref_Bad', 'BMS_w006_SW_EEPROM', 'BMS_w007_SW_NVRAM',
                   'BMS_w016_SW_Large_SOC_Update', 'BMS_w017_SW_SOC_Imbalance', 'BMS_w018_SW_Voltage_Imbalance',
                   'BMS_w019_SW_Temp_Gradient', 'BMS_w032_SW_PWT_MIA', 'BMS_w033_SW_Voltage_Sensor_Irrational',
                   'BMS_w034_SW_Current_Sensor_Irrational', 'BMS_w035_SW_Single_Battery_Temp_Irrational',
                   'BMS_w036_SW_All_Battery_Temp_Irrational', 'BMS_w037_SW_FET_Temp_Irrational',
                   'BMS_w038_SW_AFE_Degraded_Comms', 'BMS_w039_SW_Current_Sensor_Degraded_Comms',
                   'BMS_w040_SW_PWT_Degraded_Comms', 'BMS_w048_SW_Assertion', 'BMS_w049_SW_Low_Capacity',
                   'BMS_w050_SW_NotEnoughEnergyForPredischarge']
    BMS_diagnostic = ['BMS_d001_ECU_Reset', 'BMS_d002_CAN_Communication', 'BMS_d003_SW_Assertion',
                      'BMS_d004_SW_CAN_Integrity', 'BMS_d005_Large_SOC_Update', 'BMS_d006_SW_SOC_Imbalance']
    PT_fault = ['PT_f001_PTFault']
    PT_warning = ['PT_w001_EcuReset', 'PT_w002_FrontLightNoCurrent', 'PT_w003_FrontLightOverCurrent']
    PT_diagnostic = ['PT_d044_HighCpuUsage', 'PT_d045_OverrunISR', 'PT_d046_HighStackUsage']
    CL_fault = ['CL_f001_CLFault', 'CL_f002_CLMotorStall', 'CL_f003_CLCurrentChopping', 'CL_f004_CLOverCurrent',
                'CL_f005_CLPinMagFail', 'CL_f006_CLHolsterMagFail']
    CL_warning = ['CL_w001_EcuReset']
    CL_diagnostic = ['CL_d044_HighCpuUsage', 'CL_d045_OverrunISR', 'CL_d046_HighStackUsage']
    TM_fault = ['TM_f001_TMFault', 'TM_f002_TMMotorStall']
    TM_warning = ['TM_w001_EcuReset', 'TM_w002_TailLightNoCurrent', 'TM_w003_TailLightOverCurrent']
    TM_diagnostic = ['TM_d044_HighCpuUsage', 'TM_d045_OverrunISR', 'TM_d046_HighStackUsage']

    dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
    asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL13_8km/'
    index = ['logfile2021-01-19_07-00-34', 'logfile2021-01-19_07-02-26']

    s = ['MC_fault', 'MC_warning', 'MC_diagnostic', 'BMS_fault', 'BMS_warning', 'BMS_diagnostic', 'PT_fault',
         'PT_warning', 'PT_diagnostic', 'CL_fault', 'CL_warning', 'CL_diagnostic', 'TM_fault', 'TM_warning',
         'TM_diagnostic']
    signal = [MC_fault, MC_warning, MC_diagnostic, BMS_fault, BMS_warning, BMS_diagnostic, PT_fault, PT_warning,
              PT_diagnostic, CL_fault, CL_warning, CL_diagnostic, TM_fault, TM_warning, TM_diagnostic]

    # intialize arrays
    data = []
    columns = []
    for c in range(0, len(signal)):  # for each type of signal (MC_fault, MC_warning, ...),
        for d in range(0, len(signal[c])):
            columns.append(signal[c][d])

    # fill data array
    for a in range(0, len(index)):

        can_logs = LyftCAN.ascToDataframe(asc_filename + index[a] + '.asc', dbc_filename)
        can_log_by_signal = can_logs['canlogs_by_signal']
        d = []

        for b in range(0, len(signal)): # for each type of signal (MC_fault, MC_warning, ...),
            for x in range(0, len(signal[b])):  ## for each type of flag
                count = 0
                log = can_log_by_signal[signal[b][x]]
                for y in range(0, len(log)):  ## for the length of the log
                    count += log.Object[y]
                d.append(count)


        data.append(d)

    print(data)
    print(index)
    print(columns)
    df = pandas.DataFrame(data, index, columns)
    print(df)
    with ExcelWriter('test.xlsx') as writer:
        df.to_excel(writer)


input1 = input('Summary? (y/n) ')
if input1 == 'y':
    summaryFWD()
