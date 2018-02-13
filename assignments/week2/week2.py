from neo import Gpio # import Gpio library
from time import sleep # import sleep to wait for blinks

neo = Gpio() #create new Neo object

pinTwo = 2 #pin to use

neo.pinMode(pinTwo, neo.OUTPUT)# Use innerbank pin 2 and set it as output either 0 (neo.INPUT) or 1 (neo.OUTPUT)

#Blink example
for a in range(0, 5): #Do for five times
	neo.digitalWrite(pinTwo,neo.HIGH) #write high value to pin
	sleep(1)# wait one second
	neo.digitalWrite(pinTwo,neo.LOW) #write low value to pin
	sleep(1)# wait one second

