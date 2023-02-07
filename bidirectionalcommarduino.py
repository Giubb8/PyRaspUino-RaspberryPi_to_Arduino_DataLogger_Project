import serial
import time
if __name__=="__main__":
    ser=serial.Serial('/dev/ttyACM2',baudrate=9600,timeout=1) #definiamo la connessione seriale con l'arduino sulla porta,con bump 9600 e delay di 1 secondo
    ser.flush() #flushiamo il buffer 
    print("eseguo")
    while(True):
        time.sleep(1)
        if (ser.in_waiting>0):
            #line1=ser.readline().decode("utf-8").rstrip()
            #print(line1)
            temperature=ser.readline().decode("utf-8").rstrip()
            newtemperature=int(float(temperature))
            humidity=ser.readline().decode("utf-8").rstrip()
            newhumidity=int(float(humidity))
            print(f"TEMPERATURE:{newtemperature} HUMIDITY:{newhumidity}%")
            if (newtemperature>=23):
                print(f"MAGGIORE >20 {temperature}")
                ser.write(b"light\n")
            else:
                print(f"MINORE <20 {temperature}")
                ser.write(b"off\n")
           
