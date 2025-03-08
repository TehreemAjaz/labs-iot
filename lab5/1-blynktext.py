import network
import BlynkLib
from machine import Pin
import time
from neopixel import NeoPixel

# Wi-Fi Credentials
SSID = "Galaxy A107BCB"
PASSWORD = "yuvx7525"
BLYNK_AUTH = "QBljAckguL3e6mbafoZBV0a341ox8ZcN"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi:", wifi.ifconfig())

# Blynk Authentication Token

blynk = BlynkLib.Blynk(BLYNK_AUTH)

# NeoPixel Setup
PIN = Pin(48, Pin.OUT)
led = NeoPixel(PIN, 1)

# Track LED states
led_state = {'red': 0, 'green': 0, 'blue': 0}

@blynk.on("connected")
def blynk_connected():
    print("✅ Blynk Connected!")

# Function to update LED color
def update_led():
    led[0] = (led_state['red'], led_state['green'], led_state['blue'])
    led.write()
    print(f"LED Updated: {led_state}")  # Debugging info

# Blynk Virtual Pin Handlers
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

# Main loop
print("🚀 Blynk Running...")
while True:
    blynk.run()
    time.sleep(0.1)
