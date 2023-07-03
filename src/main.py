# main.py -- put your code here!
import sensors as s
from secrets import secrets
import time
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Conversions between binary data and various encodings
import machine                # Interfaces with hardware components
import micropython    

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = secrets["aio_user"]
AIO_KEY = secrets["aio_key"]
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_RAWLIGHT1_FEED = "tomenqvist/feeds/rawlight1"
AIO_RAWLIGHT2_FEED = "tomenqvist/feeds/rawlight2"
AIO_TEMP_FEED = "tomenqvist/feeds/temp"
AIO_HUMIDITY_FEED = "tomenqvist/feeds/hum"
AIO_RELDARK_FEED = "tomenqvist/feeds/reldark"
AIO_MEANLIGHT_FEED = "tomenqvist/feeds/meanlight"
# END SETTINGS

# PICO SETTINGS
update_rate = 15

def send_data(raw_light1, raw_light2, temp, hum, rel_dark, mean_light):

    print("\nPublishing: TEMP {0} to {1}... ".format(temp,  AIO_TEMP_FEED), end='')
    print("\nPublishing: HUMIDITY {0} to {1}... ".format(hum,  AIO_HUMIDITY_FEED), end='')
    print("\nPublishing: RAW LIGHT 1 {0} to {1}... ".format(raw_light1, AIO_RAWLIGHT1_FEED), end='')
    print("\nPublishing: RAW LIGHT 2 {0} to {1}... ".format(raw_light2, AIO_RAWLIGHT2_FEED), end='')
    print("\nPublishing: RELATIVE DARKNESS {0} to {1}... ".format(rel_dark, AIO_RELDARK_FEED), end='')
    print("\nPublishing: MEAN LIGHT {0} to {1}... ".format(mean_light, AIO_MEANLIGHT_FEED), end='')
    try:
        client.publish(topic=AIO_TEMP_FEED, msg=str(temp))
        client.publish(topic=AIO_HUMIDITY_FEED, msg=str(hum))
        client.publish(topic=AIO_RAWLIGHT1_FEED, msg=str(raw_light1))
        client.publish(topic=AIO_RAWLIGHT2_FEED, msg=str(raw_light2))
        client.publish(topic=AIO_RELDARK_FEED, msg=str(rel_dark))
        client.publish(topic=AIO_MEANLIGHT_FEED, msg=str(mean_light))
        print("DONE")
    except Exception as e:
        print("FAILED: ", e)
    finally:
        print("Data sent!")

client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
client.connect()
print(client)

try:

    while True:
        try:
            temp, hum = s.readTemp()
            raw_light1, raw_light2, maxLight, minLight, mean_light, relative_darkness = s.readLight(update_rate)

            print("\nTemperature: {}C, Humidity: {}%".format(temp, hum))
            print("Raw light 1 value: {}".format(raw_light1))
            print("Raw Light 2 value: {}".format(raw_light2))
            print("Mean light value: {}".format(mean_light))
            print("Relative darkness: {}".format(relative_darkness))
            print("Max light value: {}".format(maxLight))
            print("Min light value: {}".format(minLight))
            print("TEMP: ", temp)
            print("HUM: ", hum)
            send_data(raw_light1, raw_light2, temp, hum, relative_darkness, mean_light)
        except Exception as error:
            print("Exception occurred", error)
        time.sleep(update_rate)
finally:
    client.disconnect()
    client = None


