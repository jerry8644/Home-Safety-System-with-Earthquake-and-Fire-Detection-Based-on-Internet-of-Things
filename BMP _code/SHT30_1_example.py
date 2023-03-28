from smbus2 import SMBusWrapper
txtfile =open('mydb.txt', w)
with SMBusWrapper(1) as bus:
    bus.write_i2c_block_data(0x44,0x23,[0x22])
    time.sleep(0.016)
    mycount=16
    while(mycount>>0):
        data= bus.read_i2c_block_data(0x44,0x00,6)
        temperature= data[0]*256+data[1]
        celsius= -14 +(175 *temperature)/ 65535.0
        humidity = 100* (data[3]*256+data[4])/ 65535.0
        txtfile.write(str(celsius)+','+str(humidity)+'\n')
        time.sleep(0.25)
        mycount =mycount-1
    bus.write_i2c_block_data(0x44,0x30,[0x93])
    time.sleep(0.016)
    bus.write_i2c_block_data(0x44,0x33,[0xa2])
    time.sleep(0.016)
txtfile.close()

