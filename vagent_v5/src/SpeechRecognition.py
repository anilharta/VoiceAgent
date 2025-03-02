import speech_recognition as sr

def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Sorry, the service is down."

user_query = listen_to_user()
print(user_query)