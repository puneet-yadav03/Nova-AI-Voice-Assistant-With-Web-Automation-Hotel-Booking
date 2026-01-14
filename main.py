from sys import exception
import speech_recognition as sr
import webbrowser
import time
import google.generativeai as genai
from gtts import gTTS
import pygame
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
import threading

# Gemini API
genai.configure(api_key="AIzaSyAtqvZdlly40dzpJ1jf3u3bgIUcevt94_M")
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize pygame mixer once at startup
pygame.mixer.init()

# OPTIMIZED SPEAK FUNCTION - Faster, Louder
def speak(text):
    try:
        print("Nova:", text)
        tts = gTTS(text=text, lang='en', slow=False, tld='com')  # Use .com for faster speech
        tts.save("voice.mp3")
        
        # Load and increase volume
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.set_volume(1.0)  # Maximum volume
        pygame.mixer.music.play()
        
        # Faster checking interval
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)  # Reduced from 0.2 to 0.05
        
        pygame.mixer.music.unload()
        os.remove("voice.mp3")
    except Exception as e:
        print("Speech Error:", e)

# OPTIMIZED LISTEN FUNCTION - Faster recognition
def listen(prompt=None):
    recognizer = sr.Recognizer()
    # Increase energy threshold for louder activation
    recognizer.energy_threshold = 4000  # Higher = requires louder speech
    recognizer.dynamic_energy_threshold = False  # Disable auto-adjustment for consistency
    
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        
        # Reduced ambient noise adjustment time
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Reduced from 0.3
        print("Listening...")
        
        # Shorter phrase time limit for faster responses
        audio = recognizer.listen(source, phrase_time_limit=5)  # Reduced from 8
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except:
            speak("Say again")  # Shorter error message
            return ""

# PARSE DATE
def parse_date(spoken):
    month_map = {
        "january":1, "february":2, "march":3, "april":4, "may":5, "june":6,
        "july":7, "august":8, "september":9, "october":10, "november":11, "december":12
    }
    spoken = spoken.lower()
    pattern = r"(\d{1,2})\s*(st|nd|rd|th)?\s*(january|february|march|april|may|june|july|august|september|october|november|december)"
    m = re.search(pattern, spoken)
    if m:
        day = int(m.group(1))
        month = month_map[m.group(3)]
        year = datetime.now().year
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except:
            return None
    return None

# OPTIMIZED GET LAT LONG FROM GEMINI
def get_lat_long(city):
    try:
        prompt = f"Return ONLY latitude and longitude of '{city}', India. Format: lat:12.9716, long:77.5946"
        response = model.generate_content(prompt)
        text = response.text.strip()

        lat_match = re.search(r'lat[:\s]*([0-9\.\-]+)', text, re.I | re.M)
        lon_match = re.search(r'long[:\s]*([0-9\.\-]+)', text, re.I | re.M)
        
        if lat_match and lon_match:
            lat = float(lat_match.group(1))
            lon = float(lon_match.group(1))
            return lat, lon
    except Exception as e:
        print(f"Gemini error: {e}")
    return None

# OPTIMIZED BOOK HOTEL FUNCTION
def book_hotel():
    speak("Let's book a hotel")  # Shorter phrase

    # 1. City
    city_input = listen("Which city?")  # Shorter prompt
    if not city_input: return
    city_slug = re.sub(r'[^a-z0-9\s-]', '', city_input.lower()).strip().replace(' ', '-')

    # 2. Check-in
    checkin_raw = listen("Check-in date? Say like 7th November")
    checkin = parse_date(checkin_raw)
    if not checkin:
        speak("Invalid date")
        return

    # 3. Check-out
    checkout_raw = listen("Check-out date?")
    checkout = parse_date(checkout_raw)
    if not checkout:
        speak("Invalid date")
        return

    # 4. Guests
    guests_raw = listen("How many guests?")
    guests = "2"
    if guests_raw:
        num = re.search(r"\b(\d+)\b", guests_raw)
        if num:
            guests = num.group(1)

    speak("Getting coordinates")
    coords = get_lat_long(city_input.title())
    if not coords:
        lat, lng = 17.4123487, 78.4080455
    else:
        lat, lng = coords

    search_url = (
        f"https://www.fabhotels.com/search?"
        f"city={city_slug}&propertyLatitude={lat}&propertyLongitude={lng}"
        f"&checkIn={checkin}&checkOut={checkout}&guests={guests}"
    )
    speak(f"Opening hotels in {city_input.title()}")
    webbrowser.open(search_url)

    time.sleep(8)  # Reduced from 10

    hotel_name = listen("Which hotel?")
    if not hotel_name:
        speak("No hotel name")
        return

    hotel_slug = re.sub(r'[^a-z0-9\s-]', '', hotel_name.lower()).strip().replace(' ', '-')
    if not hotel_slug.startswith('fabhotel'):
        hotel_slug = f'fabhotel-{hotel_slug}'

    pdp_url = (
        f"https://www.fabhotels.com/hotels-in-{city_slug}/{hotel_slug}.html?"
        f"guests={guests}&checkIn={checkin}&checkOut={checkout}"
        f"&searchTerm={city_slug}&pdpSource=srp&srpType=Regular"
    )

    speak(f"Opening {hotel_name.title()}")
    webbrowser.open(pdp_url)

# OPTIMIZED COMMAND HANDLER   
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif "search on google" in c or "google search" in c:
        query = listen("What to search?")
        if query:
            search_google(query)

    elif "search on youtube" in c or "youtube search" in c:
        query = listen("What to search?")
        if query:
            search_youtube(query)

    elif "book hotel" in c:
        book_hotel()

    else:
        speak("Thinking")  # Shorter phrase
        try:
            answer = model.generate_content(c).text
            speak(answer)
        except Exception as e:
            speak(f"Error occurred")

# OPTIMIZED SELENIUM SEARCH FUNCTIONS
def search_google(query):
    speak(f"Searching {query}")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(query + Keys.RETURN)
    speak("Top results")
    time.sleep(2)  # Reduced from 3
    results = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.text}")
    speak("Say number")
    choice = listen()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(results):
            results[idx].click()
    except:
        speak("Invalid")
    return driver

def search_youtube(query):
    speak(f"Searching {query}")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://www.youtube.com")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_box.send_keys(query + Keys.RETURN)
    speak("Top videos")
    time.sleep(3)  # Reduced from 4
    videos = driver.find_elements(By.ID, "video-title")[:5]
    for i, v in enumerate(videos, 1):
        print(f"{i}. {v.text}")
    speak("Say number")
    choice = listen()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(videos):
            videos[idx].click()
    except:
        speak("Invalid")
    return driver

# OPTIMIZED MAIN LOOP - Continuous mode after activation
if __name__ == "__main__":
    speak("Nova ready")  # Shorter startup message
    recognizer = sr.Recognizer()
    
    # Optimized recognition settings
    recognizer.energy_threshold = 4000  # Higher for louder activation
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.5  # Reduced pause detection

    # Wait for initial activation
    while True:
        print("Listening for 'Nova'...")
        try:
            with sr.Microphone() as source:
                # Faster ambient noise adjustment
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio).lower()

            if word == "nova":
                speak("Activated. Say Nova Stop to exit")
                break  # Exit the activation loop

        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print("Error:", e)

    # Continuous command loop - stays active until "nova stop"
    while True:
        try:
            with sr.Microphone() as source:
                print("Nova listening for commands...")
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, phrase_time_limit=7)
                command = recognizer.recognize_google(audio)
                print("Command:", command)
                
                # Check for stop command
                if "nova stop" in command.lower():
                    speak("Shutting down Nova. Goodbye")
                    break  # Exit the program
                
                # Process normal commands
                processCommand(command)

        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print("Error:", e)