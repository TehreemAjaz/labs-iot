import network
import BlynkLib
from machine import Pin
import time
from neopixel import NeoPixel
import dht

# Wi-Fi Credentials
ssid = "Galaxy A107BCB"
password = "yuvx7525"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi:", wifi.ifconfig())

# Blynk Authentication Token
blynk = BlynkLib.Blynk("JfIxfDPhfSOXSrkv2Gi-Juauqw4-6Atg")

# NeoPixel Setup
led_pin = Pin(48, Pin.OUT)  # Update if needed
led = NeoPixel(led_pin, 1)

# DHT Sensor Setup
dht_pin = Pin(4)  # Adjust GPIO pin if necessary
dht_sensor = dht.DHT11(dht_pin)

@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(4, 5)  # Sync temperature and humidity values

def update_temperature_led(temp):
    """Change LED color based on temperature."""
    if temp < 20:
        print("Cold! Setting LED to Blue")
        led[0] = (0, 0, 255)  # Blue
    elif 20 <= temp <= 30:
        print("Normal Temperature! Setting LED to Green")
        led[0] = (0, 255, 0)  # Green
    else:
        print("Hot! Setting LED to Red")
        led[0] = (255, 0, 0)  # Red
    
    led.write()
    time.sleep(0.1)  # Small delay for stable updates

def send_dht_data():
    """Read and send DHT sensor data to Blynk and update LED color based on temperature."""
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        
        print(f"Temperature: {temp}°C, Humidity: {hum}%")

        # Send data to Blynk
        blynk.virtual_write(4, temp)
        blynk.virtual_write(5, hum)
        
        # Update LED color based on temperature
        update_temperature_led(temp)
    except Exception as e:
        print("DHT sensor error:", e)

while True:
    blynk.run()
    send_dht_data()
    time.sleep(5)  # Update every 5 seconds
