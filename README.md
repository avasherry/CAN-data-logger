# CAN-data-logger

### main.py
Input:
```
dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL13_100km/logfile2021-01-26_04-04-20.asc'
```
Output:
```
~~~~~ MC_warning ~~~~~
10 :MC_w040_SocMIA

~~~~~ BMS_fault ~~~~~
1 :BMS_f029_SW_Voltage_Imbalance
```

### automatedmain.py
Input:
```
dbc_filename = '/Users/asherry/Documents/rideable-firmware-master/api/can_dbc/cosmo.dbc'
asc_filename = '/Users/asherry/Desktop/TestRideData/REL/Second_Distance_Track/REL13_100km/'
index = ['logfile2021-01-19_07-00-34', 'logfile2021-01-19_07-02-26']
```
Output:
```
[xlsx file](https://drive.google.com/file/d/1OU2_lCBX6l76Ecx7HUtmUW4ZdspfEOqj/view?usp=sharing) 
with summary of fault/warning/diagnostic matrices
```

### decodeCAN.py
Work in progress. Trying to ouput decoded CAN logs to save on run time

### graphing.py
Work in progress. Trying to output matlab plots of filtered signals
