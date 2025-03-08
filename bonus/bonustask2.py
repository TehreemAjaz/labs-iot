import network
import time
import BlynkLib
import dht
from machine import Pin

# WiFi Credentials
WIFI_SSID = "GALAXY A107BCB"
WIFI_PASS = "yuvx7525"

# Blynk Authentication Token
BLYNK_AUTH = "JfIxfDPhfSOXSrkv2Gi-Juauqw4-6Atg"

# Connect to WiFi Function
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASS)

    print("Connecting to WiFi...", end="")
    timeout = 10  # Max wait time
    while not wifi.isconnected() and timeout > 0:
        time.sleep(1)
        print(".", end="")
        timeout -= 1

    if wifi.isconnected():
        print("\nWiFi connected:", wifi.ifconfig())
    else:
        print("\nWiFi connection failed!")
    
    return wifi

# Initialize WiFi
wifi = connect_wifi()

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Initialize DHT11 Sensor on GPIO 4
dht_sensor = dht.DHT11(Pin(4))

# Function to Read and Send Data
def send_sensor_data():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()  # Get Temperature
        hum = dht_sensor.humidity()  # Get Humidity
        
        print(f"Temperature: {temp}°C, Humidity: {hum}%")
        
        # Send Data to Blynk
        blynk.virtual_write(0, temp)  # Send Temp to V0
        blynk.virtual_write(1, hum)   # Send Hum to V1
    except Exception as e:
        print("Error reading sensor:", e)

# Run Blynk Loop
while True:
    blynk.run()
    send_sensor_data()
    time.sleep(5)  # Wait 5 seconds before next update

    if not wifi.isconnected():  # Check if WiFi is still connected
        print("WiFi disconnected! Reconnecting...")
        wifi = connect_wifi()  # Reconnect WiFi
