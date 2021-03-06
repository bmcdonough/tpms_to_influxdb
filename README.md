# rtl_433 TPMS to InfluxDB

A python based script to parse JSON output from rtl_433 and pass it to influx.
* [rtl_433](https://github.com/merbanan/rtl_433)

```
$ sudo rtl_433 -M level -f 315000000 -F json -R 110
or
$ sudo rtl_433 -M level -f 315000000 -F json -R 88

110 example:
{"time" : "2022-06-22 12:50:16", "model" : "PMV-107J", "type" : "TPMS", "id" : "0ceb28a2", "status" : 16, "battery" : "OK", "counter" : 2, "failed" : "OK", "pressure_kPa" : 205.840, "temperature_C" : 19.000, "mic" : "CRC", "mod" : "FSK", "freq1" : 315.015, "freq2" : 314.932, "rssi" : -10.028, "snr" : 7.316, "noise" : -17.359}

88 example:
{"time" : "2022-06-22 13:48:10", "model" : "Toyota", "type" : "TPMS", "id" : "d85146a6", "status" : 128, "pressure_PSI" : 35.000, "temperature_C" : 19.000, "mic" : "CRC", "mod" : "FSK", "freq1" : 314.997, "freq2" : 314.949, "rssi" : -0.118, "snr" : 17.240, "noise" : -17.373}


$ cat tpms.json | python3 tpms2influx.py
$ sudo rtl_433 -M level -f 315000000 -F json -R 88 | python3 tpms2influx.py
