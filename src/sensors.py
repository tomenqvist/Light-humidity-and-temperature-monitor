import dht
import machine
from machine import ADC, Pin
import time

tempSensor1 = dht.DHT11(Pin(17))
tempSensor2 = dht.DHT11(Pin(16))
ldr1 = ADC(Pin(27))
ldr2 = ADC(Pin(26))
led = Pin("LED", Pin.OUT)

# Queues for storing sensor values
ldr1_q = []
ldr2_q = []
hum_q = []
temp_q = []

# Queues for storing max and min light values
maxLight_q = [0]
minLight_q = [65535]

# Fill queues with 0's
for i in range(9):
    ldr1_q.append(0)
    ldr2_q.append(0)
    hum_q.append(0)
    temp_q.append(0)

def readTemp():
    try:
        tempSensor1.measure()
        tempSensor2.measure()
        temp1 = tempSensor1.temperature()
        temp2 = tempSensor2.temperature()
        hum2 = tempSensor2.humidity()
        hum1 = tempSensor1.humidity()
        Enqueue(temp_q, (temp1+temp2)/2)
        Enqueue(hum_q, (hum1+hum2)/2)
        Dequeue(temp_q)
        Dequeue(hum_q)
        sorted_temp = sorted(temp_q)
        sorted_hum = sorted(hum_q)
        temp = sum(sorted_temp[2:7]) / 5
        hum = sum(sorted_hum[2:7]) / 5

    except Exception as error:
        print("Failed to read temperature and humidity", error)
        temp = None
        hum = None
    return (temp, hum)

seconds_passed = 0

def readLight(update_rate):
    try:
        global ldr1_q, ldr2_q, maxLight_q, minLight_q, seconds_passed

        # If 24 hours have passed, add another element to the max and min light queues
        if(seconds_passed >= 86400):
            if(len(maxLight_q) < 7):
                Enqueue(maxLight_q, 0)
            else:
                Dequeue(maxLight_q)
                Enqueue(maxLight_q, 0)
            if(len(minLight_q) < 7):
                Enqueue(minLight_q, 65535)
            else:
                Dequeue(minLight_q)
                Enqueue(minLight_q, 65535)
            seconds_passed = 0
        
        raw_light1 = ldr1.read_u16()
        raw_light2 = ldr2.read_u16()
        Dequeue(ldr2_q)
        Dequeue(ldr1_q)
        Enqueue(ldr1_q, raw_light1)
        Enqueue(ldr2_q, raw_light2)
        sorted1_q = sorted(ldr1_q)
        sorted2_q = sorted(ldr2_q)
        mean_ldr1 = sum(sorted1_q[2:7]) / 5
        mean_ldr2 = sum(sorted2_q[2:7]) / 5
        print(sorted1_q[2:7])
        print(mean_ldr1)
        print(sorted2_q[2:7])
        print(mean_ldr2)
        mean_light = (mean_ldr1 + mean_ldr2) / 2
        
        print("Seconds passed: ", seconds_passed)
        if mean_light > maxLight_q[len(maxLight_q) - 1] and seconds_passed >= (update_rate * len(ldr1_q)):
            maxLight_q[len(maxLight_q) - 1] = mean_light
            print("Updated maxLight")
        if mean_light < minLight_q[len(minLight_q) - 1] and seconds_passed >= (update_rate * len(ldr1_q)):
            minLight_q[len(minLight_q) - 1] = mean_light
            print("Updated minLight")
        print("MIN queue", minLight_q)
        print("MAX queue",maxLight_q)
        seconds_passed += update_rate
        
        # update max and min light in this iteration for use when calculating relative darkness
        maxLight = max(maxLight_q)
        minLight = min(minLight_q)

        # Calculate relative light
        if mean_light > maxLight:
            relative_darkness = 100
        elif maxLight > 0 and (mean_light - minLight) > 0:
            relative_darkness = round((mean_light - minLight) / (maxLight - minLight) * 100, 2)
        else:
            relative_darkness = 0

        
        if relative_darkness >= 70:
            led.on()
        else:
            led.off()
    except Exception as error:
        print("Failed to read light", error)
    
    
    return raw_light1, raw_light2, maxLight, minLight, mean_light, relative_darkness



# Queue implmentation
def Enqueue(queue, item):
    queue.append(item)

def Dequeue(queue):
    return queue.pop(0)