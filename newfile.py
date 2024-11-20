import os
import pygame
import speech_recognition as sr
from googlesearch import search

# Trigger word
TRIGGER_WORD = "Jimmy"
VOICE_VOLUME = 0.8  # Volume level for voice responses


def google_search(query):
    """Perform Google search and return results."""
    results = []
    for result in search(query, num_results=3):  # Get top 3 results
        results.append(result)
    return results


def speak_response(response):
    """Speak the response using pygame."""
    pygame.mixer.init()
    tts_file = "response.wav"
    os.system(f"espeak -w {tts_file} '{response}'")  # Uses eSpeak to generate speech
    pygame.mixer.music.load(tts_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    print(f"Say '{TRIGGER_WORD}' to activate...")

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

                if TRIGGER_WORD.lower() in text.lower():
                    print("Jimmy activated!")
                    speak_response("Hello! How can I help you?")
                    print("Listening for your query...")

                    audio = recognizer.listen(source)
                    query = recognizer.recognize_google(audio)
                    print(f"Query: {query}")

                    if "search" in query.lower():
                        search_query = query.replace("search", "").strip()
                        results = google_search(search_query)
                        response = f"Here are the top results I found:\n{results[0]}"
                    else:
                        response = f"You asked: {query}. I'm just a demo assistant!"

                    print(f"Jimmy: {response}")
                    speak_response(response)

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Error: {e}")