#!/usr/bin/env python3
import sys
#import fileinput
import json
import time

db_name = "tpms"
influx_host = "http://admin:password@192.168.1.100:8086/write?db=%s&precision=s" % (
    db_name)


def is_json(myjson):
    print("###DEBUG is_json()")
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def convert_pressure(pressure, unit):
    unit = unit.lower()
    if unit == "kpa":
        pressure = pressure / 6.895
        return (pressure)

def convert_temp(temp, unit):
    unit = unit.lower()
    if unit == "c":
        temp = 9.0 / 5.0 * temp + 32
        return (temp)
    if unit == "f":
        temp = (temp - 32) / 9.0 * 5.0
        return (temp)


def write_influx(measurement, pressure, temp, freq1, freq2, rssi, snr, noise):
    curly = ("curl -i -XPOST '%s' --data-binary 'tpms,id=%s pressure=%s,temp=%s,freq1=%s,freq2=%s,rssi=%s,snr=%s,noise=%s %s'" %
             (influx_host, measurement, pressure, temp, freq1, freq2, rssi, snr, noise, int(time.time())))
    print(curly)
    from subprocess import call
    status = call(curly, shell=True)
    return (status)


def main():
    for line in sys.stdin:
        if is_json(line):
            print(line, flush=True, end='\r')
            data = json.loads(line)
            for k, v in data.items():
                if 'id' in k:
                    measurement = v
                if 'pressure' in k:
                    pressure_change = convert_pressure(v, "kPa")
                    pressure_change = round(pressure_change, 1)
                    print("pressure_PSI", pressure_change)
                    pressure = pressure_change
                if k == "temperature_C":
                    temp_change = convert_temp(v, "C")
                    temp_change = round(temp_change, 1)
                    print("temperature_F", temp_change)
                    temp = temp_change
                if 'freq1' in k:
                    freq1 = v
                if 'freq2' in k:
                    freq2 = v
                if 'rssi' in k:
                    rssi = v
                if 'snr' in k:
                    snr = v
                if 'noise' in k:
                    noise = v
            if all ([measurement, pressure, temp, freq1, freq2, rssi, snr, noise]):
                results = write_influx(measurement, pressure, temp,
                             freq1, freq2, rssi, snr, noise)
                print(results)
    return None


if __name__ == '__main__':
    main()
