import network
import BlynkLib
from machine import Pin
import time
from neopixel import NeoPixel

# Wi-Fi Credentials
SSID = 'GALAXXY A107BCB'
PASSWORD = 'yuvx7525'

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi:", wifi.ifconfig())

# Blynk Authentication Token
BLYNK_AUTH = 'JfIxfDPhfSOXSrkv2Gi-Juauqw4-6Atg'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# NeoPixel Setup
PIN_NUM = 48  # Define the GPIO pin for NeoPixel
led_pin = Pin(PIN_NUM, Pin.OUT)
led = NeoPixel(led_pin, 1)

# Track LED states
led_state = {'red': 0, 'green': 0, 'blue': 0}

@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(1, 2, 3)  # Sync virtual pins on connection

def update_led():
    """Update NeoPixel LED based on stored states."""
    led[0] = (led_state['red'], led_state['green'], led_state['blue'])
    led.write()

@blynk.on('V1')  # Green LED
def green_led(value):
    led_state['green'] = int(value[0]) * 255
    update_led()

@blynk.on('V2')  # Red LED
def red_led(value):
    led_state['red'] = int(value[0]) * 255
    update_led()

@blynk.on('V3')  # Blue LED
def blue_led(value):
    led_state['blue'] = int(value[0]) * 255
    update_led()

# Main Loop
print("🚀 Blynk Running...")
while True:
    blynk.run()
    time.sleep(0.1)
