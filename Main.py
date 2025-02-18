import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import sys
import google.generativeai as genai
import os
import time
import pyautogui
import subprocess
import winsound  # For Windows alarm sound


# Set up Google Gemini API key
GEMINI_API_KEY = "Enter_your_API_KEY"  #Gemini API key #erase it when used in LinkedIn or GitHub
genai.configure(api_key=GEMINI_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(text):
    """Convert text to speech and print output."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Recognizes user speech and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=10)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return "none"
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return "none"
        except sr.WaitTimeoutError:
            speak("You were silent for too long. Please try again.")
            return "none"

def get_gemini_response(query, short_response=True):
    """Fetch AI-generated response from Google Gemini API with short or full response"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)

        full_answer = response.text.strip()
        short_answer = full_answer.split(".")[0] + "."  # Only take the first sentence

        return short_answer if short_response else full_answer

    except Exception as e:
        return f"Error: {str(e)}"

def show_location_on_maps(location):
    """Opens Google Maps with the given location"""
    maps_url = f"https://www.google.com/maps/search/{location.replace(' ', '+')}"
    webbrowser.open(maps_url)
    speak(f"Showing location of {location} on Google Maps.")

def navigate_to_location(destination):
    """Opens Google Maps in navigation mode"""
    maps_url = f"https://www.google.com/maps/dir//{destination.replace(' ', '+')}"
    webbrowser.open(maps_url)
    speak(f"Starting navigation to {destination}.")

def set_alarm(alarm_time):
    """Sets an alarm at the specified time (HH:MM AM/PM or HH:MM 24-hour format)."""
    try:
        # Convert input time into 24-hour format
        alarm_time = alarm_time.strip().lower()
        now = datetime.datetime.now()

        # Handling 12-hour format with AM/PM
        if "am" in alarm_time or "pm" in alarm_time:
            alarm_time_obj = datetime.datetime.strptime(alarm_time, "%I:%M %p").time()
        else:
            alarm_time_obj = datetime.datetime.strptime(alarm_time, "%H:%M").time()

        # Combine with today's date
        alarm_datetime = datetime.datetime.combine(now.date(), alarm_time_obj)

        # If the time has already passed, set for the next day
        if alarm_datetime <= now:
            alarm_datetime += datetime.timedelta(days=1)

        speak(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')}.")

        # Wait until the alarm time
        while datetime.datetime.now() < alarm_datetime:
            time.sleep(10)

        # Play alarm sound
        for _ in range(5):  # Repeat 5 times
            winsound.Beep(1000, 1000)  # 1000 Hz frequency, 1000 ms duration
        speak("Alarm ringing! Wake up!")

    except ValueError:
        speak("Invalid time format. Please say a time like '7 AM' or '19:30'.")

def process_command(query):
    """Processes user query for system commands and Gemini AI responses"""
    if "hello" in query or "hi" in query:
        speak("Hello! I am Primus, How can I assist you today?")

    elif "your name" in query:
        speak("I am your AI assistant.")

    elif "time" in query:
        time_now = datetime.datetime.now().strftime("%H:%M %p")
        speak(f"The current time is {time_now}")

    elif "date" in query:
        date_today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {date_today}")

    elif "set alarm for" in query:
        alarm_time = query.replace("set alarm for", "").strip()
        set_alarm(alarm_time)

    elif "open instagram" in query:
        speak("Opening your Instagram page")
        webbrowser.open("https://www.instagram.com/techwithdebangan/")

    elif "open linkedin" in query:
        speak("Opening your Linkedin")
        webbrowser.open("https://www.linkedin.com/in/debangan-ghosh/")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("No Wikipedia page found for this topic.")

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "show location of" in query:
        location = query.replace("show location of", "").strip()
        show_location_on_maps(location)

    elif "navigate to" in query:
        destination = query.replace("navigate to", "").strip()
        navigate_to_location(destination)

    elif "increase volume" in query:
        pyautogui.press("volumeup")
        speak("Volume increased")

    elif "decrease volume" in query:
        pyautogui.press("volumedown")
        speak("Volume decreased")

    elif "mute volume" in query:
        pyautogui.press("volumemute")
        speak("Volume muted")

    elif "shutdown" in query:
        speak("Shutting down the system in 5 seconds.")
        time.sleep(5)
        os.system("shutdown /s /t 1")

    elif "restart" in query:
        speak("Restarting the system in 5 seconds.")
        time.sleep(5)
        os.system("shutdown /r /t 1")

    elif "lock the pc" in query:
        speak("Locking the system.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "exit" in query or "stop" in query:
        speak("Goodbye! Have a great day.")
        sys.exit()

    else:
        speak("Thinking...")
        short_answer = get_gemini_response(query, short_response=True)
        speak(short_answer)

        speak("Do you want to hear more?")
        response = take_command()

        if "yes" in response:
            full_answer = get_gemini_response(query, short_response=False)
            speak(full_answer)

        speak("Do you need any more help?")
        next_task = take_command()
        if "no" in next_task or "stop" in next_task:
            speak("Okay! Have a great day.")
            sys.exit()

# Run assistant in loop
if __name__ == "__main__":
    speak("Hello, I am Primus. How can I assist you?")
    while True:
        command = take_command()
        if command != "none":
            process_command(command)
