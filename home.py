import RPi.GPIO as GPIO
import time
import datetime
import threading
import csv
import mysql.connector
import room
import requests
from ctypes import c_short
# BOARD
# chen_room
chen_door_CONTROL_PIN = 13
chen_door_button1 = 31
chen_pir_sensor = 33
chen_mq2_dpin = 37
chen_mq2_apin = 0  # channel
# chih_room
chih_door_CONTROL_PIN = 18
chih_door_button = 15
chih_pir_sensor = 22
chih_mq2_dpin = 16
chih_mq2_apin = 4  # channel
# out_room
out_up_mq2_dpin = 29
out_up_mq2_apin = 1  # channel
out_down_mq2_dpin = 38
out_down_mq2_apin = 3  # channel
# living_room
living_door_CONTROL_PIN = 12
living_pir_sensor = 32
living_up_mq2_dpin = 7
living_up_mq2_apin = 2  # channel
living_down_mq2_dpin = 11
living_down_mq2_apin = 5  # channel
# share
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24
buzzer = 36


def GPIO_init():
    '''setup GPIO'''
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # chen_door
    GPIO.setup(chen_door_CONTROL_PIN, GPIO.OUT)
    GPIO.setup(chen_door_button1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(chen_pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
    # chih_door
    GPIO.setup(chih_door_CONTROL_PIN, GPIO.OUT)
    GPIO.setup(chih_pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(chih_door_button, GPIO.IN, GPIO.PUD_UP)
    # living_door
    GPIO.setup(living_door_CONTROL_PIN, GPIO.OUT)
    GPIO.setup(living_pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
    # smoke
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(out_up_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(out_down_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(chen_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(chih_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(living_up_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(living_down_mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # buzzer
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(buzzer, GPIO.LOW)
    '''setup Line Notify and Mysql'''
    token = 'line_token'  # input Line Notify token
    cnx = mysql.connector.connect(user='user_name', password='user_name_passward',
                                  host='host_ip', database='database_name')  # connect to mysql
    cursor = cnx.cursor()


def lineNotifyMessage(token, msg):
    '''setup Line Notify api'''
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code


def fire_door_operation(living_room, b_room, c_room, num):
    '''open door case'''
    if num == True:
        living_room.open_door()

        if b_room.people_status == 1:
            b_room.open_door()

        else:
            b_room.close_door()

        if c_room.people_status == 1:
            c_room.open_door()
        else:
            c_room.close_door()
    else:
        living_room.close_door()
        b_room.close_door()
        c_room.close_door()


def sql_operation(room):
    '''get value from mysql use for Line bot open or close door'''
    control = cursor.fetchone()
    control = list(map(int, control))
    cnx.commit()
    if control == [1]:
        room.open_door()
    elif control == [2]:
        room.close_door()


def line_message(living_room, out_room, chen_room, chih_room):
    '''setup Line Notify case'''
    if living_room == 1:
        message = "Fire starts from living room. Fire Escape!!!"
        lineNotifyMessage(token, message)
    elif out_room == 1:
        message = "Fire starts from Corridor. Fire Escape!!!"
        lineNotifyMessage(token, message)
    elif chen_room == 1:
        message = "Fire starts from chen room. Fire Escape!!!"
        lineNotifyMessage(token, message)
    elif chih_room == 1:
        message = "Fire starts from chih room. Fire Escape!!!"
        lineNotifyMessage(token, message)


def run_loop():
    try:
        # setup room device
        chen_room = room.Room(chen_mq2_dpin, chen_mq2_apin, None, None,
                              chen_pir_sensor, None, chen_door_CONTROL_PIN, chen_door_button1)
        chih_room = room.Room(chih_mq2_dpin, chih_mq2_apin, None, None,
                              chih_pir_sensor, None, chih_door_CONTROL_PIN, chih_door_button)
        living_room = room.Room(living_up_mq2_dpin, living_up_mq2_apin, living_down_mq2_dpin,
                                living_down_mq2_apin, living_pir_sensor, None, living_door_CONTROL_PIN, None)
        out = room.Room(out_up_mq2_dpin, out_up_mq2_apin, out_down_mq2_dpin,
                        out_down_mq2_apin, living_pir_sensor, None, None, None)
        # add open door operation
        chen_room.Check_door()
        chih_room.Check_door()
        message = "\nHere are the instructions of our design.\n-------------------------------\n1. Open door: \n   #o+room name   e.g. #ochen \n2. Close door: \n   #c+room name   e.g. #cchen \n3. Show humidity: \n   #livhumi \n4. Show temperature: \n   #livtemp"
        lineNotifyMessage(token, message)

        while True:
            living_room.Get_fire()
            chen_room.Get_fire()
            chih_room.Get_fire()
            out.Get_fire()
            living_room.Pir_value()
            chen_room.Pir_value()
            chih_room.Pir_value()
            living_room.Sht31()
            print("living", living_room.people_status, "chen",
                  chen_room.people_status, "chih", chih_room.people_status)

            # update to database
            cursor.execute("INSERT INTO Living_room (temp,humi,smoke) Values(%s,%s,%s)" % (
                str(living_room.temp_sht31), str(living_room.humi_sht31), living_room.fire_status_up))
            cursor.execute("INSERT INTO Out_room (smoke) Values(%s)" %
                           (out.fire_status_up))
            cursor.execute("INSERT INTO Chen_room (smoke) Values(%s)" %
                           (chen_room.fire_status_up))
            cursor.execute("INSERT INTO Chih_room (smoke) Values(%s)" %
                           (chih_room.fire_status_up))

            # control_door
            cursor.execute("SELECT living_door FROM Door")
            sql_operation(living_room)
            cursor.execute("UPDATE Door SET living_door= 0")

            # chen_door
            cursor.execute("SELECT chen_door FROM Door")
            sql_operation(chen_room)
            cursor.execute("UPDATE Door SET chen_door= 0")

            # chih_door
            cursor.execute("SELECT chih_door FROM Door")
            sql_operation(chih_room)
            cursor.execute("UPDATE Door SET chih_door= 0")

            # earthquake
            cursor.execute("SELECT detect FROM Earthquake")
            result = cursor.fetchone()
            result = list(map(int, result))
            cnx.commit()
            if result != [0]:
                print("earthquake")
                message = "Earthquake!!! Doors have been opened."
                lineNotifyMessage(token, message)
                if (chih_room.people_status == 1 or chen_room.people_status == 1 or living_room.people_status == 1):
                    living_room.open_door()
                    chih_room.open_door()
                    chen_room.open_door()
                    cursor.execute("UPDATE Earthquake SET detect= 0")
                    cnx.commit()
                    break

            # fire
            if (living_room.fire_status_up == 1 or out.fire_status_up == 1 or chen_room.fire_status_up == 1 or chih_room.fire_status_up == 1):
                line_message(living_room.fire_status_up, out.fire_status_up,
                             chen_room.fire_status_up, chih_room.fire_status_up)
                if (chih_room.people_status == 1 or chen_room.people_status == 1 or living_room.people_status == 1):
                    fire_door_operation(
                        living_room, chen_room, chih_room, True)
                    while True:
                        line_message(living_room.fire_status_up, out.fire_status_up,
                                     chen_room.fire_status_up, chih_room.fire_status_up)
                        GPIO.output(buzzer, GPIO.HIGH)
                        out.Get_fire()
                        living_room.Get_fire()
                        living_room.Sht31()
                        chen_room.Get_fire()
                        chih_room.Get_fire()
                        living_room.Pir_value()
                        chen_room.Pir_value()
                        chih_room.Pir_value()
                        print("living", living_room.people_status, "chen",
                              chen_room.people_status, "chih", chih_room.people_status)
                        # update to database
                        cursor.execute("INSERT INTO Living_room (temp,humi,smoke) Values(%s,%s,%s)" % (
                            str(living_room.temp_sht31), str(living_room.humi_sht31), living_room.fire_status_up))
                        cursor.execute(
                            "INSERT INTO Out_room (smoke) Values(%s)" % (out.fire_status_up))
                        cursor.execute("INSERT INTO Chen_room (smoke) Values(%s)" % (
                            chen_room.fire_status_up))
                        cursor.execute("INSERT INTO Chih_room (smoke) Values(%s)" % (
                            chih_room.fire_status_up))

                        if (living_room.fire_status_down == 1 or out.fire_status_down == 1):
                            message = "Doors have been closed. Please stay at room!!!"
                            lineNotifyMessage(token, message)
                            fire_door_operation(
                                living_room, chen_room, chih_room, False)
                            break
                        elif (chih_room.people_status == 0 and chen_room.people_status == 0 and living_room.people_status == 0):
                            message = "There is no one in the house. Call 119 ASAP!!!"
                            lineNotifyMessage(token, message)
                            fire_door_operation(
                                living_room, chen_room, chih_room, False)
                            break
                    break
                else:  # no people in the house
                    fire_door_operation(
                        living_room, chen_room, chih_room, False)
                    message = "Doors have been closed. Call 119 ASAP!!!"
                    lineNotifyMessage(token, message)
                    break

    except KeyboardInterrupt:
        print("quit")
    finally:
        cnx.close()
        GPIO.output(buzzer, GPIO.LOW)
        chen_room.pwm.stop()
        chih_room.pwm.stop()
        living_room.pwm.stop()


def main():
    GPIO_init()
    run_loop()


if __name__ == "__main__":
    main()
