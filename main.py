import Adafruit_DHT
import time
import smbus
from time import sleep
import RPi.GPIO as GPIO
from pijuice import PiJuice

pijuice = PiJuice(1,0x14)

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
TEMP = 0x41
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

LED_PIN = 17
on = False
def light():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT)
	if(on):
		GPIO.output(LED_PIN, GPIO.LOW)
		on = False
	else:
		GPIO.output(LED_PIN, GPIO.HIGH)
		on = True
	GPIO.cleanup()

def light2(go):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT)
	if(go):
		GPIO.output(LED_PIN, GPIO.LOW)
	else:
		GPIO.output(LED_PIN, GPIO.HIGH)
	GPIO.cleanup()
	
def checkValue(val):
    val = val['data'] if val['error'] == 'NO_ERROR' else val['error']
    return val
	
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def imuData():
  acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	tem = read_raw_data(TEMP) 
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	
	t = tem/340 + 35
  return Ax,Ay,Az,Gx,Gy,Gz

def humidityData():
  humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
  if humidity is not None and temperature is not None:
    return temperature,humidity
  else:
    print("Sensor failure. Check wiring.");

time = 0;
while True:
	if(time % 1 == 0):
		light()
	if(checkValue(pijuice.status.GetChargeLevel()) < 15):
		light2(True)
	else:
		light2(False)
	
	time.sleep(0.5)
	time += 0.5
