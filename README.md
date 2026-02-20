
# I am hacking
🌤️ Weather Station – Raspberry Pi Pico W - Piko z ústí na labem
        .-""""-.
       /        \
      /_        _\
     // \      / \\
     |\__\    /__/|
      \    ||    /
       \        /
        \  __  /
         '.__.'
         /  |  \
        /    |    \
       /      |      \
      /        |        \
     /_________|_________\
         Raspberry Pie 🍰
📌 Popis projektu

Tento projekt je jednoduchá meteostanice vytvořená pro platformu Raspberry Pi Pico W.
Zařízení se připojí k WiFi síti, zjistí svou aktuální geografickou polohu pomocí veřejné IP adresy a každých 10 minut stáhne aktuální počasí z API OpenWeatherMap.

Výsledná data jsou zobrazena na LCD displeji.

⚙️ Jak program funguje
1️⃣ Po zapnutí zařízení:

Na LCD se zobrazí:

Connecting to
WiFi...

Proběhne připojení k WiFi síti.

2️⃣ Po úspěšném připojení:

Program zavolá IP API (ip-api.com) a zjistí:

zeměpisnou šířku

zeměpisnou délku

Souřadnice se na několik sekund zobrazí na LCD.

3️⃣ Následně:

Program zavolá OpenWeatherMap API.

Získá:

teplotu (°C)

vlhkost (%)

základní popis počasí

Data se zobrazí na LCD.

4️⃣ Každých 10 minut:

Proběhne aktualizace počasí.

Pokud vypadne WiFi, zařízení se automaticky pokusí znovu připojit.

Pokud API vrátí chybu, zobrazí se chybová hláška.

🗂️ Struktura projektu
/main.py
/config.json   (ignorován v .gitignore)
/lib/
    lcd_api.py
    i2c_lcd.py
.gitignore
README.md
🔐 config.json

Soubor config.json obsahuje citlivé údaje (WiFi a API klíč).
Nesmí být nahrán na GitHub (je přidán do .gitignore).

Vytvořte soubor config.json se strukturou:

{
  "wifi_ssid": "NAZEV_WIFI",
  "wifi_password": "HESLO_WIFI",
  "openweather_api_key": "VAS_API_KLIC"
}
🌍 Použitá API
📍 IP API

Slouží k získání geografické polohy podle veřejné IP adresy.

Nevyžaduje API klíč.

URL: http://ip-api.com/json

🌦️ OpenWeatherMap API

Slouží ke stažení aktuálního počasí.

Vyžaduje API klíč.

Limit: 1000 požadavků denně (školní klíč).

🖥️ Použitý hardware

Raspberry Pi Pico W

I2C LCD displej (16x2)

Připojení přes I2C:

SDA → GP0

SCL → GP1

VCC → 5V

GND → GND

🚀 Nahrání programu
1️⃣ Nahrajte MicroPython firmware

Stáhněte z:
https://micropython.org/download/rp2-pico-w/

2️⃣ Nahrajte soubory

Pomocí Thonny:

Nahrajte main.py

Nahrajte složku /lib

Vytvořte config.json

3️⃣ Spusťte program

Uložte main.py do zařízení jako hlavní soubor.

Restartujte Pico W.

🛡️ Robustnost programu

Program obsahuje:

Automatické znovupřipojení k WiFi

Ošetření chyb při komunikaci s API

Kontrolu připojení před každou aktualizací

Zobrazení chybové hlášky při problému

👨‍💻 Autor

Vypracováno jako školní projekt – Práce s Git a GitHub.

Pokud chceš, můžu ti ještě:

🔥 udělat verzi README víc „profi GitHub style“

🎯 přidat badge (Python version, platforma, atd.)

📷 udělat ASCII obrázek přímo Raspberry Pi Pico W místo koláče

📝 upravit text tak, aby vypadal víc jako maturitní práce

Stačí říct 🙂
