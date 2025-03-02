import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage
speak("Hello, how can I help you?")