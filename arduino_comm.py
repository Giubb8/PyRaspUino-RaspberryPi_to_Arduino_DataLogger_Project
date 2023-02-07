import json

import serial
import time
import datetime
def connect_to_arduino():
    ser = serial.Serial('/dev/ttyACM3', baudrate=9600,timeout=1)  # definiamo la connessione seriale con l'arduino sulla porta,con bump 9600 e delay di 1 secondo
    ser.flush()
    return ser

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM2', baudrate=9600,timeout=1)  # definiamo la connessione seriale con l'arduino sulla porta,con bump 9600 e delay di 1 secondo
    ser.flush()  # flushiamo il buffer
    print("eseguo")
    while (True):
        time.sleep(1)
        if (ser.in_waiting > 0):
            # line1=ser.readline().decode("utf-8").rstrip()
            # print(line1)
            temperature = ser.readline().decode("utf-8").rstrip()
            newtemperature = int(float(temperature))
            humidity = ser.readline().decode("utf-8").rstrip()
            newhumidity = int(float(humidity))
            print(f"TEMPERATURE:{newtemperature} HUMIDITY:{newhumidity}%")
            if (newtemperature >= 23):
                print(f"MAGGIORE >20 {temperature}")
                ser.write(b"light\n")
            else:
                print(f"MINORE <20 {temperature}")
                ser.write(b"off\n")


def measure_temp_and_hum():
    ser=connect_to_arduino()
    if (ser.in_waiting > 0):
        temperature = int(float(ser.readline().decode("utf-8").rstrip()))
        humidity =int(float(ser.readline().decode("utf-8").rstrip()))
        print(f"TEMPERATURE:{temperature} HUMIDITY:{humidity}%")
    return None


def monitor_th_measurement(th_list:list):
    print("dentro funzione")
    ser = serial.Serial('/dev/ttyACM3', baudrate=9600,timeout=1)  # definiamo la connessione seriale con l'arduino sulla porta,con bump 9600 e delay di 1 secondo
    ser.flush()
    print("dopo connessione ad arduino")
    while(True):
        time.sleep(1)
        if (ser.in_waiting > 0):
            print("connesso ad arduino")
            temperature = int(float(ser.readline().decode("utf-8").rstrip()))
            humidity =int(float(ser.readline().decode("utf-8").rstrip()))
            now = datetime.datetime.now()
            print(f"TEMPERATURE:{temperature} HUMIDITY:{humidity}% TIME:{now.strftime('%Y-%m-%d %H:%M:%S')}")
            th_list.append(temperature,humidity,now)
            print(str(th_list))
            with open('data.json', 'w') as file:
                json.dump(th_list, file)
            if (temperature >= 23):
                print(f"MAGGIORE >20 {temperature}")
                ser.write(b"light\n")
            else:
                print(f"MINORE <20 {temperature}")
                ser.write(b"off\n")
        else:
            print("non connesso")
