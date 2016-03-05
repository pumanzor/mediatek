import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json, time
import inspect

from itertools import count

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):                                   
        print("Connected with result code "+str(rc))                           
        # Subscribing in on_connect() means that if we lose the connection and 
        # reconnect then subscriptions will be renewed.                        
        client.subscribe("/test")                                              
                                                                               
# The callback for when a message is received from the server.                 
def on_message(client, userdata, msg):                                         
        print("recieved: "+msg.topic+" "+str(msg.payload))   
	char = str(msg.payload)                  
        words = msg.payload.split(',')        
        if words[0] == 'run': #  If 'run' is the first word of the message  
		publish_mqtt("Recibido :" + str(words[0]))
       		global tiempo 
		tiempo = words[2]
                globals()[words[1]]()
                                                                               
def publish_mqtt(payload):                                                     
    """                                                                        
    Send an MQTT mesage to javaScript client                                   
    """                                                                                          
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



def on():
        i = 0
	z = int(tiempo)
        global count
        publish_mqtt("ingresa a def on" + str(z))
        while True:
         if i <= z:
          time.sleep(1)
          publish_mqtt("publicando en el loop valor : " +str(tiempo))
          time.sleep(1)
          i += 1
         else:
	  break
        count = 0


def off():
        global count
        publish_mqtt('I heard you!')
        count = 0




                                                                                                 
#Start Loop                                                                                      
client.loop_start()                                                                              
                                                                                                 
count = 0                                                                                        
tiempo = 0                                                                                       
try:                                                                                             
        while True:                                                                              
                publish_mqtt("message number " + str(count) )                                    
                count += 1                                                                       
                time.sleep(2)                                                                    
except Exception as err:                                                                         
    print 'Error: ', err                                                                         
finally:                                                                                         
        print ''                                                                                 
        print 'Cleaning up'                                                                      
        client.loop_stop() 
