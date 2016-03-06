import mraa
#pin = mraa.Pwm(18)
pin19 = mraa.Pwm(19)

pin1 = mraa.Gpio(1)
pin1.dir(mraa.DIR_OUT)

pin0 = mraa.Gpio(0)
pin0.dir(mraa.DIR_OUT)

number = 0

while True:
	pin0.write(0)
	pin1 = mraa.Gpio(1)
	pin1.dir(mraa.DIR_OUT)
	pin1.write(1)
	pin19.period_us(400)      
	pin19.enable(True)
	pin19.write(0.5)  
	number += 1
	if number == 1000:
	        break
