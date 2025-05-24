from Bard import Chatbot
from playsound import playsound
from faster_whisper import WhisperModel
import speech_recognition as sr
from os import system
import warnings
import sys
import winsound
import pyttsx3

# For Beep:
frequency = 1000  # In hertz
duration = 500  # In milliseconds (1 second)
# Paste your Bard Token (check README.md for where to find yours) 
token = 'bggAlS82qpv3cv3gsGAF9KMEFOEvQhIlhLnVfpNUWdSUGeV5zbFhWvlSwHB-o16h-42tcg.'
ts_token = 'sidts-CjEB3e41hXkL6fa8DAa5io_-vjQxb-3lV0bo2lP4eT9sO7yEdAIGdNVaKyFxpZu0T5c1EAA'
# Initialize Google Bard API
chatbot = Chatbot(token,ts_token)
# Initialize speech recognition
r = sr.Recognizer()
# Initialize Whisper model
tiny_model = WhisperModel('tiny.en',compute_type='int8')
base_model = WhisperModel('base.en',compute_type='int8')

speech_engine = pyttsx3.init()
speech_rate = speech_engine.getProperty('rate')
speech_engine.setProperty('rate', speech_rate-50)

FIXED_PROMPTS = [
    ("summary", "Gaganyaan is a crewed orbital spacecraft built in India that is meant to serve as the foundation for the Indian Human Spaceflight Program. It is the first project to demonstrate human space flight capability in India. The spacecraft is designed to carry a crew of three members to space for a period of five to seven days and safely return them to Earth. The first uncrewed test flight is planned for 2023, with a second uncrewed test flight and the first crewed flight planned for 2024. The Indian Navy has also set up a water survival training facility for the Gaganyaan crew."),
    ("difference between", "IVA suits are designed to be worn inside a pressurized spacecraft during mission-critical stages such as launch, entry, docking, and engine burn. They are lighter and more comfortable than EVA suits, as they do not require the same level of protection from the harsh conditions of space. EVA suits, on the other hand, are designed for use outside the spacecraft, either in microgravity or on a planetary surface. They are more complex and require more protection from the harsh conditions of space, such as micrometeoroids and extreme temperature changes. I hope this helps!"),
    ("new technologies", "The major new technologies required for Gaganyaan programme are as follows: Human rated launch vehicle, Crew escape systems, Habitable orbital module, Life support system, Crew selection, training and associated crew management activities."),
    ("collaborating", "Major collaborating partners for Gaganyaan include:Indian Armed Forces, Defence Research Development organisation, Indian maritime agencies - Indian Navy, Indian Coast Guard, Shipping corporation of India, National institute of Oceanography, National Institute of Ocean Technology, Indian Meteorological Department ,CSIR Labs, Academic institutes, Industry partners"),
    ("objective", "The Gaganyaan Programme envisages undertaking the demonstration of human spaceflight to Low Earth Orbit (LEO) in the short-term and will lay the foundation for a sustained Indian human space exploration programme in the long run. The objective of Gaganyaan programme is to demonstrate indigenous capability to undertake human space flight mission to LEO. As part of this programme, two unmanned missions and one manned mission are approved by Government of India"),
]

def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']

def speak(text):
    print('VyomanautAI: ', text)
    speech_engine.say(text)
    speech_engine.runAndWait()

def wait_for_wake_word(source):
    # Continuously listens for wake word locally
    while True:
        try:
            winsound.Beep(frequency, duration)
            print('\nSay "Hello" to wake me up. \n')
            audio = r.listen(source, None, 2)
            print("DEBUG: listen() completed")
            with open("wake_detect.wav", "wb") as f:
                f.write(audio.get_wav_data())
            print("DEBUG: write() completed")
            # Transcribe wake word using whisper tiny model
            segments, _ = tiny_model.transcribe('wake_detect.wav')
            print("DEBUG: transcribe() completed")
            text_input = ''.join(segment.text for segment in segments)
            # If wake word is found, break out of loop
            if 'hello' in text_input.lower().strip():
                break
            else:
                print("No wake word found. Try again.")
        except Exception as e:
            print("Error transcribing audio: ", e)
            continue

def handle_prompt(source):
    try:
        # Record prompt
        audio = r.listen(source,None,8)
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        # Transcribe prompt using whisper base model
        segments, _ = base_model.transcribe('prompt.wav')
        prompt_text = ''.join(segment.text for segment in segments)
        print("Sending to VyomanautAI:", prompt_text, '\n')
        # If prompt is empty, start listening for wake word again
        if len(prompt_text.strip()) == 0:
            speak("Empty prompt. Please speak again.")
            return
    except Exception as e:
        print("Error transcribing audio: ", e)
        return
    
    # Use fixed answers when the right words are detected.
    for keyword, response in FIXED_PROMPTS:
        if keyword in prompt_text.strip().lower():
            speak(response)
            break
    else:
        response = prompt_bard(prompt_text+". Reply under 40 words.")
        speak(response)

def main():
    prompt_bard("From now onwards pretend you are an AI called 'Vyomanaut AI'. Your purpose is to explain about ISRO and its contribution to space and technology. Keep all answers simple and short. Your creators are Tejassh Tharayil from class 12C and Alwin Promod from class 12A. Remember to keep all answers short!")
    # Initialize microphone object
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # Runs program indefinitely
        while True:
            wait_for_wake_word(source)
            playsound('wake_detected.wav')
            print("Wake word detected. Please speak your prompt to VyomanautAI.")
            handle_prompt(source)
            
if __name__ == '__main__':
    main()
