import paho.mqtt.client as paho
import time
import smbus

bus1 = smbus.SMBus(1)
bus1.write_i2c_block_data(0x44, 0x2C, [0x06])
time.sleep(0.5)
data1 = bus1.read_i2c_block_data(0x44, 0x00, 6)
temp1 = data1[0] * 256 + data1[1]
cTemp1 = -45 + (175 * temp1 / 65535.0)
humidity1 = 100 * (data1[3] * 256 + data1[4]) / 65535.0

bus4 = smbus.SMBus(4)
bus4.write_i2c_block_data(0x44, 0x2C, [0x06])
time.sleep(0.5)
data4 = bus4.read_i2c_block_data(0x44, 0x00, 6)
temp4 = data4[0] * 256 + data4[1]
cTemp4 = -45 + (175 * temp4 / 65535.0)
humidity4 = 100 * (data4[3] * 256 + data4[4]) / 65535.0

print ( “Bus 1 Temperature in Celsius is : %.2f C” %cTemp1)
print ( “Bus 1 Relative Humidity is : %.2f %%RH” %humidity1)
print ( “Bus 4 Temperature in Celsius is : %.2f C” %cTemp4)
print ( “Bus 4 Relative Humidity is : %.2f %%RH” %humidity4)