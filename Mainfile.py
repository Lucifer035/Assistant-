import speech_recognition as sr
import pyttsx3
import os
import webbrowser

# Text-to-Speech engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed
engine.setProperty('volume', 0.9)  # Volume

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Recognize user voice
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except Exception as e:
            print("Could not understand. Please say again.")
            return None
    return query.lower()

# Main function
def jimmy_assistant():
    speak("Jimmy is ready to assist you.")
    while True:
        command = take_command()
        if command is None:
            continue
        if "jimmy" in command:
            if "open notepad" in command:
                speak("Opening Notepad.")
                os.system("notepad")
            elif "open calculator" in command:
                speak("Opening Calculator.")
                os.system("calc")
            elif "open browser" in command:
                speak("Opening your default web browser.")
                webbrowser.open("https://www.google.com")
            elif "open folder" in command:
                speak("Opening a specific folder.")
                folder_path = "C:\\Users\\YourUsername\\Documents"  # Change this to your desired folder path
                os.startfile(folder_path)
            elif "stop" in command or "bye" in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("I am sorry, I didn't understand the command.")

# Start the assistant
if __name__ == "__main__":
    jimmy_assistant()
