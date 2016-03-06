import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json, time
import mraa
import inspect

from itertools import count

pin19 = mraa.Pwm(19)
pin0 = mraa.Gpio(0)
pin0.dir(mraa.DIR_OUT)

pin1 = mraa.Gpio(1)
pin1.dir(mraa.DIR_OUT)

def on():
        i = 0
        z = int(tiempo)
        y = int(dir)
        global count
        publish_mqtt("Order Received : " + str(z))
        pin1 = mraa.Gpio(1)
        pin1.dir(mraa.DIR_OUT)
        pin1.write(y)
        pin19.enable(True)
        pin19.period_us(1000)
        pin19.write(0.25)
        while True:
         pin0.write(0)
         i += 1
         time.sleep(0.01)
         if i == z:
                pin0.write(1)
                break
        count = 0

def loop():
        i = 0
        z = int(tiempo)
        y = int(dir)
        global count
        publish_mqtt("loop!!")
        pin0.write(0)
        pin1 = mraa.Gpio(1)
        pin1.dir(mraa.DIR_OUT)
        pin1.write(y)
        pin19.enable(True)
        pin19.period_us(1000)
        pin19.write(0.25)
        count = 0
                                               
def off():                                        
        global count                              
        pin0.write(1)                             
        publish_mqtt('Motor Stopped')             
        count = 0                                 
                                                  
                                                  
def on_connect(client, userdata, flags, rc):      
        print("Connected with result code "+str(rc))
        client.subscribe("/test")                   
        publish_mqtt("Connected Motor OK!")         
                                                    
def on_message(client, userdata, msg):              
        print("recieved: "+msg.topic+" "+str(msg.payload))
        words = msg.payload.split(',')                    
        if words[0] == 'run':                             
                global tiempo                             
                global dir                                
                tiempo = words[2]                         
                dir = words[3]                            
                globals()[words[1]]()                     
                                                          
def publish_mqtt(payload):                                
    topic = '/test'                                       
    try:                                                  
        publish.single(topic, payload, hostname='190.97.169.126', port=1883, retain=False, qos=0)
    except Exception as err:                                                                     
            print "Couldn't publish :" + str(err)                                                
            pass                                                                                 
                                                                                                 
client = mqtt.Client()                                                                           
client.on_connect = on_connect                                                                   
client.on_message = on_message                                                                   
client.connect("190.97.169.126")                                                                 
client.loop_start()                                                                              
                                                                                                 
while True:                                                                                      
    time.sleep(10)                                                                               
                         
