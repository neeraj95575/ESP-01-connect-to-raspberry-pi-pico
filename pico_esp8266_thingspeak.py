from machine import Pin, I2C, UART
import time
import utime

    
WiFi_SSID='write_wifi_name'              # Wifi_SSID
WiFi_password = 'write_wifi_password'      # WiFi Password
TCP_ServerIP = "184.106.153.149"   # Thingspeak IP address
Port = '80'                        # Thingspeak port
API_KEY = "write_your_API_keys"       # API Key

uart = UART(0, 115200)           # Default Baud rate

ir_sensor = Pin(6,Pin.OUT)

trigger = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)

def sendAT(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = time.ticks_ms()
    while (time.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode("utf-8")
            print(s)
            if(s.find(ack) >= 0):
                return True
    return False


def send_data(ir_value,dis):    
    data="GET /update?key="+API_KEY+"&field1=%s&field2=%s"%(ir_value,dis)+"\r\n";
    final=len(data)
    reading=0
    sendAT("AT+CIPSTART=\"TCP\",\""+TCP_ServerIP+"\","+Port,"OK",5000)
    sendAT("AT+CIPSEND="+str(final)+"\r\n","OK")
    time.sleep(0.5)
    uart.write(data)
    print(data)
    sendAT('AT+CIPCLOSE'+'\r\n',"OK")
    
 
def ultrasonic():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    
    while echo.value() == 0:
       signaloff = utime.ticks_us()
    while echo.value() == 1:
       signalon = utime.ticks_us()
       
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance
    #print("The distance from object is ",distance,"cm")

 
sendAT("AT","OK")
sendAT("AT+CWMODE=1","OK")
sendAT("AT+CWJAP=\""+WiFi_SSID+"\",\""+WiFi_password+"\"","OK",20000)
sendAT("AT+CIFSR","OK")

while True:
        ir_value = str(ir_sensor.value())
        print("infrarad values = ",ir_value)
        dis = ultrasonic()
        send_data(ir_value,dis)
        time.sleep(2)#delay of 2 second
        


