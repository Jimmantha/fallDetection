import adxl345 #import the ADXL345 module
import time #import the time module
import RPi.GPIO as GPIO

#initalise
ADDRESS=0x53

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) #set GPIO 18 as output for buzzer
GPIO.setup(25,GPIO.OUT) #GPIO25 as Trig
GPIO.setup(27,GPIO.IN) #GPIO27 as Echo

acc=adxl345.ADXL345(i2c_port=1,address=ADDRESS) #instantiate
acc.load_calib_value() #load calib. values in accel_calib
acc.set_data_rate(data_rate=adxl345.DataRate.R_100) #see datasheet 
acc.set_range(g_range=adxl345.Range.G_16, full_res=True) # .. range set to 16g
acc.measure_start()
#acc.calibrate() #calibrate only one time

def measure_distance():
    GPIO.output(25, False)
    while(GPIO.input(27) == 0):
        pulse_start = time.time()
    pulse_end = time.time()
    distance = (pulse_end - pulse_start) * 17150
    return distance
    
def fallDetection():
    x,y,z=acc.get_3_axis_adjusted() 
    return(x,y,z)
    

def buzzer():
   GPIO.output(18,1) #output logic high/'1'
   time.sleep(0.1) #delay 100ms
   GPIO.output(18,0) #output logic low/'0'
   time.sleep(0.1) #delay 100ms
   
def telegram():
    return 0

while(True):
    x,y,z = fallDetection()
    print(x,y,z)
    distance = measure_distance()
    if distance < 10:
        buzzer()
    