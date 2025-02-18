# Primus - AI Voice Assistant

## 🚀 Overview
Primus is a smart AI voice assistant built using Python. It recognizes user voice commands, responds intelligently, and performs various tasks like opening applications, searching the web, setting alarms, controlling system volume, and even answering queries using Google's Gemini AI. With both male and female voice options, Primus provides a smooth and interactive experience for users.

---

## 🧠 AI Voice Assistant Logic

### 1. **Speech Recognition & Voice Input Handling**
```python
import speech_recognition as sr

def take_command():
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
```
- Uses Google Speech Recognition to convert speech to text.
- Handles unknown inputs and network errors gracefully.

### 2. **Text-to-Speech Conversion**
```python
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # Change to voices[1].id for female voice
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
```
- Converts text responses into speech output.
- Offers a male or female voice option.

### 3. **AI-Powered Responses using Gemini API**
```python
import google.generativeai as genai

def get_gemini_response(query):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(query)
    return response.text.strip()
```
- Uses Google's Gemini API to generate AI-based responses.

---

## ⚡ Features & Their Logic

### 1. **Web Navigation (Google, YouTube, LinkedIn, Instagram, etc.)**
```python
import webbrowser

elif "open google" in query:
    webbrowser.open("https://www.google.com")
    speak("Opening Google")
```
- Opens specified websites via voice command.

### 2. **Desktop App Control (Calculator, Notepad, etc.)**
```python
import os

elif "open calculator" in query:
    os.system("calc")
    speak("Opening Calculator")
```
- Uses `os.system()` to launch desktop applications.

### 3. **Time & Date Retrieval**
```python
import datetime

elif "time" in query:
    time_now = datetime.datetime.now().strftime("%H:%M %p")
    speak(f"The current time is {time_now}")
```
- Retrieves and announces the current system time and date.

### 4. **Alarm & Reminder System**
```python
import time, winsound

def set_alarm(alarm_time):
    while datetime.datetime.now().strftime("%H:%M") != alarm_time:
        time.sleep(10)
    for _ in range(5):
        winsound.Beep(1000, 1000)
    speak("Alarm ringing! Wake up!")
```
- Sets alarms and rings at the specified time.

### 5. **System Control (Volume, Shutdown, Restart, Lock PC)**
```python
import pyautogui

elif "increase volume" in query:
    pyautogui.press("volumeup")
    speak("Volume increased")
```
- Controls system volume and power functions.

### 6. **File Management (Create, Rename, Delete Files)**
```python
import os

elif "create file" in query:
    with open("newfile.txt", "w") as f:
        f.write("This is a new file.")
    speak("File created successfully.")
```
- Performs basic file operations via voice commands.

### 7. **Google Maps Location & Navigation**
```python
elif "show location of" in query:
    location = query.replace("show location of", "").strip()
    webbrowser.open(f"https://www.google.com/maps/search/{location.replace(' ', '+')}")
    speak(f"Showing location of {location} on Google Maps.")
```
- Opens locations on Google Maps based on user input.

---

## 🛠️ Code Breakdown & Execution Flow
1. The assistant **listens** to the user's command using the microphone.
2. Converts **speech to text** using Google's Speech Recognition API.
3. **Processes the command** to check for relevant tasks.
4. Executes **predefined tasks** (like opening apps, setting alarms, etc.).
5. If no predefined task matches, the **Gemini AI API** generates a response.
6. The assistant **speaks out** the response and displays it as text.

---

## 📌 Requirements & Installation Guide
### 🔹 Requirements:
- Python 3.8+
- Libraries: `speech_recognition`, `pyttsx3`, `datetime`, `wikipedia`, `webbrowser`, `pyautogui`, `google.generativeai`

### 🔹 Installation Steps:
```bash
# Clone the repository
git clone https://github.com/debanganghosh08/AI-voice-assistant-.git
cd AI-voice-assistant-

# Install dependencies
pip install -r requirements.txt

# Run the assistant
python assistant.py
```
---

## 🚀 Future Improvements
- Integration with ChatGPT for enhanced AI responses.
- Adding support for multi-language voice recognition.
- Expanding file management functionalities.

---

## 📌 Contribution & Support
Feel free to contribute or suggest new features! If you encounter any issues, drop a comment or open an issue on GitHub. 😊🚀

