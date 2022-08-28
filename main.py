import sys
import time
from argparse import ArgumentParser
import time
import argparse

from bluepy import btle  # linux only (no mac)
import pyrebase


# BLE IoT Sensor Demo
# Author: Gary Stafford
# Reference: https://elinux.org/RPi_Bluetooth_LE
# Requirements: python3 -m pip install –user -r requirements.txt
# To Run: python3 ./rasppi_ble_receiver.py d1:aa:89:0c:ee:82 <- MAC address – change me!
config = {
  "apiKey": "QYE3KKUnA4Wfx4Sa3y7fEz4vYSKxv4vpyu7VsObz",
  "authDomain": "ai-health-telemetry-system-default-rtdb.firebaseio.com",
  "databaseURL": "https://ai-health-telemetry-system-default-rtdb.firebaseio.com",
  "storageBucket": "ai-health-telemetry-system.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()




def main():
    # get args
    args = get_args()

    print("Connecting…")
    nano_sense = btle.Peripheral(args.mac_address)

    print("Discovering Services…")
    _ = nano_sense.services
    environmental_sensing_service = nano_sense.getServiceByUUID("180C")

    print("Discovering Characteristics…")
    _ = environmental_sensing_service.getCharacteristics()

    while True:
        print("\n")
        read_temperature(environmental_sensing_service)
        read_humidity(environmental_sensing_service)
        read_mic(environmental_sensing_service)
        read_Gyo(environmental_sensing_service)
        read_Acc(environmental_sensing_service)
        read_HR(environmental_sensing_service)
        read_roll(environmental_sensing_service)
        telemetry(t,m,g,A,h,R,HR)
        #time.sleep(2) # transmission frequency set on IoT device
    return false

def byte_array_to_char(value):
    # e.g., b'2660,2058,1787,4097\x00' -> 2659,2058,1785,4097
    value = value.decode("utf-8")
    return value


def read_mic(service):
    mic_char = service.getCharacteristics("2A56")[0]
    micro = mic_char.read()
    micro = byte_array_to_char(micro)
    global m
    m=micro
    #micro  = byte_array_to_char(micro)
    print(f"MicroPhone Output: {(micro)} db")
    return m


def read_temperature(service):
    temperature_char = service.getCharacteristics("2A57")[0]
    temperature = temperature_char.read()
    temperature = byte_array_to_char(temperature)
    global t
    t=temperature
    print(f"Temperature: {(temperature)} °C")
    return t
  
 
def read_Gyo(service):
    Gyo_char = service.getCharacteristics("2A58")[0]
    Gyo_meter = Gyo_char.read()
    Gyo_meter = byte_array_to_char(Gyo_meter)
    global g
    g=Gyo_meter
    print(f"Gyro: {(Gyo_meter)}rps")
    return g


def read_Acc(service):
    Acc_char = service.getCharacteristics("2A59")[0]
    Acc_meter = Acc_char.read()
    Acc_meter = byte_array_to_char(Acc_meter)
    global A
    A=Acc_meter
    print(f"Accleo: {(Acc_meter)}m/s2")
    return A


def read_humidity(service):
    humidity_char = service.getCharacteristics("2A60")[0]
    humidity = humidity_char.read()
    humidity  = byte_array_to_char(humidity )
    global h
    h=humidity
    print(f"Humidity: {(humidity)} %")
    return h

def read_roll(service):
    roll_char = service.getCharacteristics("2A61")[0]
    roll_char = roll_char.read()
    roll_char  = byte_array_to_char(roll_char)
    global R
    R=roll_char
    print(f"roll_ Angle: {(roll_char)}°")
    return R

def read_HR(service):
    HR_char = service.getCharacteristics("2A62")[0]
    HR_char = HR_char.read()
    HR_char  = byte_array_to_char(HR_char)
    global HR
    HR=HR_char
    print(f"Heart_rate: {(HR_char)}BPM")
    return HR


def get_args():
    arg_parser = ArgumentParser(description="BLE IoT Sensor Demo")
    arg_parser.add_argument('mac_address', help="MAC address of device to connect")
    args = arg_parser.parse_args()
    return args

def  telemetry(t,m,g,A,h,R,HR):
    data_base={"Temperature":t,"MicroPhone Output":m,"Gyo_meter":g,"Acc_meter":A,"Humidity": h,"Heart_rate":HR,"rolling_angle":R}
    db.child("AI_telemetry system").push(data_base)
    db.child("AI_telemetry system").child("node-red").set(data_base)


if __name__ == "__main__":

    main()
 
    
    
  
