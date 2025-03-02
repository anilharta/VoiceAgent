from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import speech_recognition as sr
import pyttsx3
import re
import google.generativeai as genai
from config import Config

import sys
print(f'Path: {sys.path}')
app = Flask(__name__)

# Step 1: Set up Gemini
#.configure(api_key=os.getenv('GEMINI_API_KEY'))
genai.configure(api_key=Config.GEMINI_API_KEY)
#genai.configure(api_key='AIzaSyCKg1EU1ztypcdv35WVxD0b4Ox7n9cWWLc') 
model = genai.GenerativeModel('models/gemini-1.5-flash-8b')

# Global flag to indicate whether the process should be stopped
stop_process = False

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
    global stop_process
    if stop_process:
        return "Process stopped by user."
    
    input_text = f"""Context: {context}\nQuestion: {question}
    \nAnswer: 
    give an one liner summary from the pdf of the query being asked. 
    Generate a list of headings extracted from the provided PDF document. Include only the headings without any additional explanations or details.
    """
    response = model.generate_content(input_text)
    return response.text

# Step 5: Text-to-Speech
def speak(text):
    global stop_process
    if stop_process:
        return
    
    try:
        clean_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

pdf_text = extract_text_from_pdf('D:/Core App Development/Voice Agent/vagent/src/document.pdf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global stop_process
    stop_process = False  # Reset the stop flag
    
    user_query = request.json.get('query')
    if user_query.lower() in ["exit", "quit", "stop", "thank"]:
        response = "Happy to assist you.. Goodbye!"
        return jsonify({'response': response, 'end': True})
    
    sections = pdf_text.split('\n\n')
    relevant_section = ''
    for section in sections:
        if user_query.lower() in section.lower():
            relevant_section = section
            break
    
    if not relevant_section:
        relevant_section = pdf_text
    
    answer = ask_ai(user_query, relevant_section)
    speak(answer)
    return jsonify({'response': answer, 'end': False})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_process
    stop_process = True
    return jsonify({'response': 'Process stopped by user.', 'end': True})

if __name__ == '__main__':
    app.run(debug=True)