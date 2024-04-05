# import required libraries
from flask import Flask, request, render_template, redirect, url_for
import os
import requests
import json
import openai
from openai import OpenAI

# initiate flas app
app = Flask(__name__)

# declare environmental variables and path
DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen?model=nova-2&diarize=true&punctuate=true&utterances=true"
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/engines/davinci/sentiment"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 


@app.route('/')
def home():
    # load upload.html when the app runs
    return render_template('upload.html')

@app.route("/upload", methods=["GET","POST"])
def index():
    # function the obtain audio file from upload.html
    if request.method == "POST":
        # Get the uploaded file
        file = request.files['file']
        if file:
            transcription = transcribe_audio(file) 
            sentiment_results = analyze_sentiment(transcription)
            insights = extract_insights(transcription)
            return render_template("results.html", transcription=transcription, sentiment_results = sentiment_results, insights=insights)
    return render_template("upload.html")

def transcribe_audio(filename):
    # Make a POST request to Deepgram API and extract transcription

    # Read the audio file
    audio_data = file.read()

    # Create headers with the API key
    headers = {
    	"Authorization": f"Token {DEEPGRAM_API_KEY}",
    	"Content-Type": "audio/wav"
    }

    # Send a POST request to Deepgram API for transcription
    response = requests.post(DEEPGRAM_API_URL, data=audio_data, headers=headers)

    # Parse the response
    if response.status_code == 200:
        utterances = json.loads(response.content)["results"]["utterances"]
        formatted_transcriptions = []
        for utterance in utterances:
            speaker = utterance["speaker"]
            transcript = utterance["transcript"]
            formatted_transcriptions.append(f"Speaker {speaker}: {transcript}")
        return "\n".join(formatted_transcriptions)
    else:
        return f"Error: {response.status_code} - {response.content.decode('utf-8')}"

def analyze_sentiment(transcription):
   # function to obtain sentiment from the transcription.
   # first declare the OPENAI_API_KEY
   openai.api_key = os.environ.get("OPENAI_API_KEY")

   # declare the messages to be sent as a prompt to chatgpt
   messages = [
            {"role": "system", "content": "You are an AI language model trained to analyze and detect the sentiment of conversations."},
            {"role": "user", "content": f"Analyze the following conversation to determine if the sentiment is positive, negative or neutral for each Speaker and elaborate: {transcription}"}
        ] 

   # obtain response from chatgpt
   response = openai.chat.completions.create(
        model= "gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["\n"]
     )

   # parse the response to obtain only the message (sentiment analysis) to be displayed
   sentiment = response.choices[0].message.content.strip() 
   return sentiment

def extract_insights(transcription):
   # Generate insights about speakers based on sentiment results
   openai.api_key = os.environ.get("OPENAI_API_KEY")

   # declare the messages to be sent as a prompt to chatgpt
   messages = [
            {"role": "system", "content": "You are an AI language model trained to generate useful insights from conversations."},
            {"role": "user", "content": f"Analyze the following conversation to determine likings, interests, personality traits for each Speaker and provide general psychological insight into the attitude and personality of each Speaker: {transcription}"}
        ]

   # obtain response from chatgpt
   response = openai.chat.completions.create(
        model= "gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["\n"]
     )

   # parse the response to obtain only the message (insights into the personality of the speakers) to be displayed
   insights = response.choices[0].message.content.strip() 
   return insights


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 
