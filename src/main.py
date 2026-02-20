import network
import urequests
import ujson
import utime
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# ---------------- CONFIG ----------------

CONFIG_FILE = "config.json"
WEATHER_INTERVAL = 600  # 10 minut (600 sekund)

# LCD nastavení (uprav podle adresy)
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# ---------------- LOAD CONFIG ----------------

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    except Exception as e:
        print("Error loading config:", e)
        return None

config = load_config()
if not config:
    raise Exception("Config file missing or invalid!")

SSID = config["wifi_ssid"]
PASSWORD = config["wifi_password"]
API_KEY = config["openweather_api_key"]

# ---------------- LCD INIT ----------------

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# ---------------- WIFI ----------------

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_wifi():
    lcd.clear()
    lcd.putstr("Connecting to")
    lcd.move_to(0, 1)
    lcd.putstr("WiFi...")
    
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        
        timeout = 15
        while timeout > 0:
            if wlan.isconnected():
                break
            utime.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("Connected:", wlan.ifconfig())
        return True
    else:
        print("WiFi connection failed")
        return False

# ---------------- GEOLOCATION ----------------

def get_location():
    try:
        response = urequests.get("http://ip-api.com/json")
        data = response.json()
        response.close()

        lat = data["lat"]
        lon = data["lon"]
        return lat, lon
    except Exception as e:
        print("Location error:", e)
        return None, None

# ---------------- WEATHER ----------------

def get_weather(lat, lon):
    try:
        url = (
            "http://api.openweathermap.org/data/2.5/weather?"
            + "lat=" + str(lat)
            + "&lon=" + str(lon)
            + "&appid=" + API_KEY
            + "&units=metric"
        )

        response = urequests.get(url)
        data = response.json()
        response.close()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["main"]

        return temp, humidity, description

    except Exception as e:
        print("Weather API error:", e)
        return None

# ---------------- MAIN ----------------

def show_coordinates(lat, lon):
    lcd.clear()
    lcd.putstr("Lat: {:.2f}".format(lat))
    lcd.move_to(0, 1)
    lcd.putstr("Lon: {:.2f}".format(lon))
    utime.sleep(3)

def show_weather(temp, humidity, desc):
    lcd.clear()
    lcd.putstr("{}C {}".format(temp, desc[:7]))
    lcd.move_to(0, 1)
    lcd.putstr("Hum:{}%".format(humidity))

# Program start
while True:

    # Ensure WiFi
    if not wlan.isconnected():
        if not connect_wifi():
            utime.sleep(5)
            continue

    lat, lon = get_location()
    if lat is None:
        lcd.clear()
        lcd.putstr("Loc error")
        utime.sleep(10)
        continue

    show_coordinates(lat, lon)

    weather = get_weather(lat, lon)
    if weather:
        temp, humidity, desc = weather
        show_weather(temp, humidity, desc)
    else:
        lcd.clear()
        lcd.putstr("Weather error")

    # čekání 10 minut
    for _ in range(WEATHER_INTERVAL):
        if not wlan.isconnected():
            break
        utime.sleep(1)