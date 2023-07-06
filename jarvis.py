import openai
import speech_recognition as sr
import pygame
import gtts
from api_secret import API_KEY
import os
import random
import webbrowser
import sys

#Api keyinizi "api_secret.py" dosyasından çeker
openai.api_key = API_KEY
pygame.mixer.init()

## device_index = 1 yazan yere kendicihaz numaranızı girin
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
print(sr.Microphone.list_microphone_names())
conversation = ""
user_name = "Serkan"
while True:
 
    with mic as source:
        print("Dinliyor...")
        r.adjust_for_ambient_noise(source, duration=1.1)
        audio = r.listen(source)
    print("Dinleme beklemede.")
    try:
        user_input = r.recognize_google(audio, language="tr")
        print("Sahibin ifadesi:", user_input)
    except Exception as e:
        print(e)
        continue
    if "serkan" in user_input.lower() and "en sevdiğim şarkı" in user_input.lower():
        webbrowser.open("https://www.youtube.com/watch?v=vNI2bc58BNs")
        sys.exit(0) # programı sonlandır
    prompt = user_name+": "+user_input+"\nBot:"
    conversation += prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        max_tokens=4000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    response_str = response["choices"][0]["text"].strip()
    print(response_str)
    
    rand=random.randint(1,100)
    file= 'ses-'+str(rand)+'.mp3'
    tts = gtts.gTTS(str(response_str), lang="tr")
    tts.save("file.mp3")

    pygame.mixer.music.load("file.mp3")
    pygame.mixer.music.play()
  
    while pygame.mixer.music.get_busy():
        continue
    