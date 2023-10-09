import cv2
import os
import pyaudio
import wave
import speech_recognition as sr

# Define constants
PHRASE_FILE = "voice_capture_phrase.wav"
IMAGE_OUTPUT_PATH = "captured_image.jpg"

# Function to capture voice input and save it as a WAV file
def record_voice():
    audio = pyaudio.PyAudio()
    
    # Record audio
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
    
    print("Please say the capture command...")
    input("Press Enter to start recording...")
    
    frames = []
    
    for _ in range(0, int(44100 / 1024 * 5)):  # Adjust recording duration as needed
        data = stream.read(1024)
        frames.append(data)
    
    print("Recording complete.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save recorded audio to a WAV file
    with wave.open(PHRASE_FILE, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(frames))

# Function to recognize the voice command
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.AudioFile(PHRASE_FILE) as source:
        audio = recognizer.record(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return None

# Function to capture a picture from the laptop camera
def capture_picture():
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Camera not found.")
        return
    
    ret, frame = camera.read()
    
    if ret:
        cv2.imwrite(IMAGE_OUTPUT_PATH, frame)
        print("Image captured and saved as '{}'.".format(IMAGE_OUTPUT_PATH))
    else:
        print("Failed to capture an image.")
    
    camera.release()

if __name__ == "__main__":
    record_voice()
    command = recognize_voice()
    
    if command and "capture" in command.lower():
        capture_picture()
    else:
        print("Voice command not recognized or does not contain 'capture'.")
