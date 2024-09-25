from flask import Flask, request, render_template, redirect, url_for
import os
import requests
import json
import openai

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen?model=nova-2&diarize=true&punctuate=true&utterances=true"
DEEPGRAM_API_KEY = "b3f433bf98b0d5d1f5f77f246638b04843a3f115"
OPENAI_API_URL = "https://api.openai.com/v1/engines/davinci/sentiment"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 


@app.route('/')
def home():
    return render_template('upload.html')

@app.route("/upload", methods=["GET","POST"])
def index():
    if request.method == "POST":
        # Get the uploaded file
        file = request.files['file']
        if file:
            # Save the file to the upload folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
        transcription = transcribe_audio(filename)
        sentiment_results = analyze_sentiment(transcription)
        insights = extract_insights(transcription)
        return render_template("results.html", transcription=transcription, sentiment_results = sentiment_results, insights=insights)
    return render_template("upload.html")

def transcribe_audio(filename):
    # Make a POST request to Deepgram API and extract transcription

    # Read the audio file
    with open(filename, "rb") as audio_file:
       audio_data = audio_file.read()

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
   openai.api_key = ("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")

   messages = [
            {"role": "system", "content": "You are an AI language model trained to analyze and detect the sentiment of conversations."},
            {"role": "user", "content": f"Analyze the following conversation to determine if the sentiment is positive, negative or neutral for each Speaker and elaborate: {transcription}"}
        ] 
 
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

   sentiment = response.choices[0].message.content.strip() 
   return sentiment

def extract_insights(transcription):
   # Generate insights about speakers based on sentiment results
   openai.api_key = ("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")

   messages = [
            {"role": "system", "content": "You are an AI language model trained to generate useful insights from conversations."},
            {"role": "user", "content": f"Analyze the following conversation to determine likings, interests, personality traits for each Speaker and provide general psychological insight into the attitude and personality of each Speaker: {transcription}"}
        ]
 
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

   insights = response.choices[0].message.content.strip() 
   return insights


if __name__ == '__main__':
    app.run(debug=True) 