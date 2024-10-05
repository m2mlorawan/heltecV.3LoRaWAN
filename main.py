import time
import base64
import bme280
import machine,ubinascii, ssd1306, time
import LoRaWANHandler
from LoRaConfig import LoRaConfig
from machine import Pin,SoftI2C
from cayennelpp import CayenneLPP

temp = 0
pa = 0
hum = 0
pin21 = machine.Pin(21, machine.Pin.OUT)
pin21.value(1)
def blink(count, delay):
    for ind in range(count):
        led.on()
        time.sleep(2)
        led.off()
        time.sleep(2)

print("This is the LoRa temperature and humidity measurement application.")
LoRaWANHandler.getBoardID()
LED_PIN = const(35)
led = machine.Pin(LED_PIN, machine.Pin.OUT)
i2c0 = machine.SoftI2C(scl=machine.Pin(18), sda=machine.Pin(17), freq=20000) #heltec V3
i2c = machine.SoftI2C(scl=machine.Pin(45), sda=machine.Pin(46), freq=20000) #heltec V3
oled=ssd1306.SSD1306_I2C(128,64,i2c0,60)
oled.text("LoRaWAN Thailand",0,0)
oled.show()
lh = LoRaWANHandler.LoRaWANHandler(LoRaConfig)
blink(3, 1000)
lh.otaa()
blink(3, 1000)
#time.sleep(5)
count=0
while(True):
    bme = bme280.BME280(i2c=i2c)
    temp,pa,hum = bme.values 
    print("Temp:",temp)
    print("Hum:",hum)
    print("Pa:",pa)
    print('temp:', temp, ' Hum:', hum , 'PA:', pa)
    oled.fill(0)
    oled.text("LoRaWAN Thailand",0,0)
    oled.text("Temp. "+temp, 0, 10)
    oled.text("PA "+pa, 0, 20)
    oled.text("Hum. "+hum, 0, 30)
    oled.text("Count "+str(count), 0, 50)
    oled.show()
    c = CayenneLPP()
    c.addTemperature(1, float(temp)) 
    c.addRelativeHumidity(3, float(hum))
    d=list(c.getBuffer())
    msg=bytes(d)
    count=count+1
    lh.send(msg, False)
    blink(2, 2000)


