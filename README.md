# Conversation-Sentiment
This project is done as a test for Alindor Corp as a part of their hiring process for ML Engineer.
As much as it is a test, I have learned a lot through this process and I am absolutely grateful to Alindor Corp. for giving me this opportunity to explore technologies that I have not explored before.

## Project description: 
In this project I am required create a scalable app that is hosted on a server where I can upload an audio file of conversation between two or more people, obtain the diarized transcription of the audio file using Deepgram API, then obtain sentiment analysis of the transcribed text using OpenAI API. The response from OpenAI chatgpt needs to be descriptive and not only reflect the sentiment of the conversation but also provide more indepth information about the speakers. 

## Project link: 
https://speech-sentiment-analyzer.ue.r.appspot.com

## How I aproached the project: 
I decided to develop the app locally and then deploy it to the cloud services. I decided to go with Google App Engine due to its scalability and easy no-code approach to setup. I first split the project into 4 steps. 
1) First, I created the html pages for uploading the audio file, for displaying the results and a third one for error handling. Next, I ensured that I was able to successfully upload the audio file to an upload folder
2) In the second step, I collected the audio file from the local folder and obtained the transcription from Deepgram API
3) In the third step, I passed the transcribed text to OpenAI API to get chatgpt responses. The prompts are of great importance here so we can obtain the desired result. I observed that the responses were limited to sentimental analysis when requested to do so, even with a request for elaboration. So, I developed another prompt that was meant to obtain the descriptive personality analysis of each speaker based on the conversation.
4) Finally, the fourth step was deployment of the app to Google App Engine.

## Observed performance issues:
1) I have observed that Deepgram API is not very consistent with its diarization. There are times it identifies a separate male and female voices as a single speaker. After reading the documentation shared by Alindor corp, I realized that they had observed similar issues
2) OpenAI responses are inconsistent for shorter conversations. When the conversations were only a minute long and have less content, I observed that OpenAI does not return any sentiment analysis. We get more consistent results with personality traits prompt than sentiment analysis prompt. Also, I have tried the same audio a couple of times to get the best result.
3) As the time for response from OpenAI increases, the accuracy and completeness of required information also increases. I have attached a sample response in pdf format in this repository.

## Challenges faced:
Almost all of the technologies I have used for this project are new to me. I had to learn using APIs in python, parsing reponses in json, and prompting through a python file. But having a good understanding and strong foundation of python and Machine Learning concepts, made this an easy task. There was not much struggle in this aspect of the project. The biggest challenge for me was deployment onto the cloud. This is my first Google Cloud Services deployment (though I do have a basic knowledge of AWS ML deployment), but trouble shooting and making it all work together was my biggest challenge and biggest learning curve in this assignment. The sense of achievement and satisfaction felt at the end ... just cannot be described in words....

## Future development plans:
1) The app provides not only summary, sentiment analysis, it also rates personality traits. Hence, I would like to set up API queries for important traits to get more descriptive information for each trait with justification based on the transcript.
2) Exploring other APIs for better performance of diarization is also a possibility, I would like to look at.
3) I would love to explore options using OpenAI API, where I can have multiple queries for a given transcript in a single request and then receive a single response, parse it to separate out the responses to individual queries for each personality trait and present it in the app in organized manner. This will reduce the lag time added by the repeated process of request and response.
