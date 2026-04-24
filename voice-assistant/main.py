import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        return ""

def run_assistant():
    command = take_command()

    if "hello" in command:
        speak("Hello! How can I help you?")
    
    elif "time" in command:
        time = datetime.datetime.now().strftime('%H:%M')
        speak(f"The time is {time}")
    
    elif "date" in command:
        date = datetime.date.today()
        speak(f"Today's date is {date}")
    
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

while True:
    run_assistant()