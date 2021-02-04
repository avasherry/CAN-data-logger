import os
import csv
import cantools
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import can



db = cantools.database.load_file(os.path.expanduser('/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'))
raw_log = can.ASCReader(os.path.expanduser('/Users/asherry/Desktop/TestRideData/VAl/logfile010.asc'))

#raw_log=can.ASCReader(os.path.expanduser('~/Workspace/rideable-firmware-automation/easyhtf/logs/65degC/vehicle.asc'))

filter = [802,804,1312,1318,1321]  # torque assist with MC V/I torque input
#filter = [1284] 
df = pd.DataFrame()
_log = []
for l in raw_log:
    try:
        _time = l.timestamp
        _id = l.arbitration_id
        _data = l.data
        if _id in filter or filter == []:

            _parsed = {'timestamp': _time}
            _parsed.update(db.decode_message(_id,_data))
            #print(_parsed)
            _log.append(_parsed)
            #df.append(pd.DataFrame([_parsed]))

    except:
        print(l)
        pass
    #id = _str[3]
    #data = [int('0x'+s[i], 16) for i in range(len(s)-4, len(s))]
    #print(_log)

print("finished parsing")
#print(_log)
df = pd.DataFrame(_log) 
_log = []
#df.to_csv('UXR1043.csv')
#df['timestamp'] = pd.to_datetime(df['timestamp'], format = '%H:%M:%S.%f')
df['timestamp'] = pd.to_datetime(df['timestamp'])
# print(df[['timestamp']])
df['elapsed_time'] = (df['timestamp']-df['timestamp'][0]).dt.total_seconds()
#print(df['BMS_PrechargeTemp'])
#print(df['elapsed_time'].dtypes)
#print(df['PT_EcuInfoMultiplexor'])
fig, ax = plt.subplots()

ax.plot(df['elapsed_time'], df['MC_VehicleSpeed'], marker = 'o', color = 'r', label='MC_VehicleSpeed')
ax.plot(df['elapsed_time'], df['MC_DC_Current'], marker = 'o', label='MC_MotorCurrent')
ax.plot(df['elapsed_time'], df['MC_DC_Voltage'], marker = 'o', label='MC_DC_Voltage')
#ax.plot(df['elapsed_time'], df['BMS_CellTemp_4'], marker = 'o', label='BMS_CellTemp_4')
#ax[0].plot(df['elapsed_time'], df['BMS_CellTemp_4'], marker = 'o', label='BMS_CellTemp_4')
#ax[0].plot(df['elapsed_time'], df['BMS_FetTemp'], marker = 'o', label='BMS_FetTemp')
##ax[0].plot(df['elapsed_time'], df['BMS_FuseTemp'], marker = 'o', label='BMS_FuseTemp')
#ax[1].plot(df['elapsed_time'], df['BMS_BatteryCurrent'], marker = 'o', label='BMS_BatteryCurrent')

#ax[0].set_title('Temperature Plot')
#ax[0].set_xlabel("elapsed time(s)")
#ax[0].set_ylabel("Temperature (degC)")
ax.legend(loc='best')
#ax[1].set_title('Current Plot')
#ax[1].set_xlabel("elapsed time(s)")
#ax[1].set_ylabel("Discharge Current (A)")
#plt.subplots_adjust(hspace=0.5)


plt.show()