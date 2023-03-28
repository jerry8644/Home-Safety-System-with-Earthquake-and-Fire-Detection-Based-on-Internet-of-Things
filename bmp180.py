# !/usr/bin/python
# coding:utf-8

import smbus
import time
from ctypes import c_short

DEVICE = 0x77      # 預設 I2C 位址

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1 

def convertToString(data):
  # Simple function to convert binary data into a string
  return str((data[1] + (256 * data[0])) / 1.2)

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index] << 8) + data[index + 1]).value

def getUshort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index] << 8) + data[index + 1]

def readBmp180Id(addr=DEVICE):
  # Register Address
  REG_ID     = 0xD0

  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)
  
def readBmp180(addr=DEVICE):
  # Register Addresses
  REG_CALIB  = 0xAA
  REG_MEAS   = 0xF4
  REG_MSB    = 0xF6
  REG_LSB    = 0xF7
  # Control Register Address
  CRV_TEMP   = 0x2E
  CRV_PRES   = 0x34 
  # Oversample setting
  OVERSAMPLE = 3    # 0 - 3
  
  # Read calibration data
  # Read calibration data from EEPROM
  cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)

  # Convert byte data to word values
  AC1 = getShort(cal, 0)
  AC2 = getShort(cal, 2)
  AC3 = getShort(cal, 4)
  AC4 = getUshort(cal, 6)
  AC5 = getUshort(cal, 8)
  AC6 = getUshort(cal, 10)
  B1  = getShort(cal, 12)
  B2  = getShort(cal, 14)
  MB  = getShort(cal, 16)
  MC  = getShort(cal, 18)
  MD  = getShort(cal, 20)

  # 讀取溫度
  bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
  time.sleep(0.005)
  (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
  UT = (msb << 8) + lsb

  # 讀取壓力
  bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
  time.sleep(0.04)
  (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
  UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

  # Refine temperature
  X1 = ((UT - AC6) * AC5) >> 15
  X2 = (MC << 11) / (X1 + MD)
  B5 = X1 + X2
  temperature = (B5 + 8)/16.0

  # Refine pressure
  B6  = B5 - 4000
  B62 = (B6 * B6)/4096.0
  X1  = (B2 * B62)/2048.0
  X2  = (AC2 * B6)/2048.0
  X3  = X1 + X2
  B3  = (((AC1 * 4 + X3)*8.0) + 2)/4.0

  X1 = (AC3 * B6)/8192.0
  X2 = (B1 * B62)/65536.0
  X3 = ((X1 + X2) + 2)/4.0
  B4 = (AC4 * (X3 + 32768))/32768.0
  B7 = (UP - B3) * (50000 >> OVERSAMPLE)

  P = (B7 * 2) / B4

  X1 = (P /256.0) * (P /256.0)
  X1 = (X1 * 3038) /65536.0
  X2 = (-7357 * P) /65536.0
  pressure = P + ((X1 + X2 + 3791)/16.0)

  # 計算高度
  altitude = 44330.0 * (1.0 - pow(pressure / 101325.0, (1.0/5.255)))
  return (temperature/10.0,pressure/ 100.0,round(altitude,2))

def temp_pressure_altitude_value():
  (temperature,pressure,altitude)=readBmp180()
  return temperature, pressure, altitude 

# ~ while True:
  # ~ a,b,c=temp_pressure_altitude_value()
  # ~ print(a,b,c)
