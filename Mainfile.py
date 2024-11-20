import os
import queue
import tempfile
import pygame
import soundfile as sf
import sounddevice as sd
from TTS.api import TTS
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# API Key for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Trigger word
TRIGGER_WORD = "Jimmy"
VOICE_VOLUME = 0.8  # Volume level for voice responses

class ChatGPT:
    """
    Integrates with OpenAI's ChatGPT API.
    """
    def ask(self, query):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error communicating with ChatGPT: {str(e)}"

def callback(indata, frames, time, status):
    """Audio stream callback."""
    q.put(indata.copy())

if __name__ == "__main__":
    print("Setting up Jimmy, your personal voice assistant...")
    q = queue.Queue()
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
    chat = ChatGPT()  # Initialize ChatGPT

    pygame.init()
    device_info = sd.query_devices(None, 'input')
    samplerate = int(device_info['default_samplerate'])

    try:
        print(f"\nJimmy is ready! Say '{TRIGGER_WORD}' to activate.")
        while True:
            with sd.InputStream(samplerate=samplerate, device=None, channels=1, callback=callback):
                with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
                    with sf.SoundFile(temp_wav.name, mode='w', samplerate=samplerate, channels=1, subtype=None) as file:
                        print("Listening...")
                        file.write(q.get())

                    print(f"Activation detected! Now listening for your query...")

                    with tempfile.NamedTemporaryFile(suffix='.wav') as command_wav:
                        with sf.SoundFile(command_wav.name, mode='w', samplerate=samplerate, channels=1, subtype=None) as file:
                            file.write(q.get())

                        # Simulating a recognized query (Add your transcription logic here)
                        command_text = "Hello Jimmy, what is AI?"  # Replace this with actual transcription logic
                        print(f"Query: {command_text}")

                        # Get response from ChatGPT
                        response = chat.ask(command_text)
                        print(f"Jimmy: {response}")

                        # Text-to-speech response
                        with tempfile.NamedTemporaryFile(suffix='.wav') as response_wav:
                            tts.tts_to_file(text=response, file_path=response_wav.name)
                            vresponse = pygame.mixer.Sound(response_wav.name)
                            vresponse.set_volume(VOICE_VOLUME)
                            vresponse.play()
                            pygame.time.wait(int(vresponse.get_length() * 1000))

    except KeyboardInterrupt:
        print("\nJimmy: Goodbye!")
        pygame.quit()
