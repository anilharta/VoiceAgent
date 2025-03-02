import os
import PyPDF2
import speech_recognition as sr
import pyttsx3
import re
import google.generativeai as genai

import google.generativeai as genai

  
# Step 1: Set up Gemini
GEMINI_API_KEY = "AIzaSyCKg1EU1ztypcdv35WVxD0b4Ox7n9cWWLc"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-8b')

# Step 2: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# Step 3: Ask Gemini
def ask_ai(question, context):
    #input_text = f"Context: {context}\nQuestion: {question}\nAnswer:"
    input_text = f"Context: {context}\nQuestion: {question}\nAnswer: Generate a list of headings extracted from the provided PDF document. Include only the headings without any additional explanations or details."
    response = model.generate_content(input_text)
    return response.text

# Step 4: Speech-to-Text
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
       # audio = recognizer.listen(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text} ")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Sorry, the service is down."

# Step 5: Text-to-Speech
def speak(text):
    try:
        # Remove special characters
        clean_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        engine = pyttsx3.init()
        
         # Set properties before adding anything to speak
        rate = engine.getProperty('rate')   # Get current speaking rate
        engine.setProperty('rate', rate - 50)  # Decrease the rate by 50 (adjust as needed)
       
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

# Main loop
pdf_text = extract_text_from_pdf('D:/Core App Development/Voice Agent/vagent/src/document.pdf')
speak("Hello, how can I help you?")

while True:
    user_query = listen_to_user()    
    if user_query.lower() in ["exit", "quit", "stop", "thank"]:
        speak("Happy to assist you.. Goodbye!")
        break
    
    # Split the PDF text into smaller sections
    sections = pdf_text.split('\n\n')
    
    # Find the most relevant section based on the user's query
    relevant_section = ''
    for section in sections:
        if user_query.lower() in section.lower():
            relevant_section = section
            break
    
    # If no relevant section is found, use the entire PDF text as context
    if not relevant_section:
        relevant_section = pdf_text
    
    answer = ask_ai(user_query, relevant_section)
    speak(answer)
    
    # Ask if the user has any other questions
    speak("Anything else you want to know?")
    follow_up_query = listen_to_user()
    if follow_up_query.lower() in ["no", "no thank you", "no thanks"]:
        speak("Happy to assist you.. Goodbye!")
        break
    
     
