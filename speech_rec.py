##########################################################################################

__author__ = "Roger Truchero Visa"
__copyright__ = "GNU GENERAL PUBLIC LICENSE"
__credits__ = ["Joseph Delgadillo"]
__license__ = "GPL"
__version__ = ""
__maintainer__ = "Roger Truchero Visa"
__email__ = "truchero.roger@gmail.com"
__status__ = "development"

##########################################################################################

import subprocess
import os
import pyaudio
import wave
import speech_recognition as sr

##########################################################################################

class Commander:
    def __init__(self):
        self.confirm = ["Yes", "affirmative", "si", "sure", "do it", "yeah", "ok", "confirm"]
        self.cancel = ["No, negative", "don't", "wait", "stop", "cancel"]
    
    def discover(self, text):
        if "what" in text and "your name" in text:
            if "my" in text:
                self.respond("You haven't told me your name yet")
            else:
                self.respond("My name is pie commander. How are you?")
        # Syntax: launch pycharm
        if "launch" or "open" in text:
            app = text.split(" ", 1)[-1] # app: pycharm
            self.respond("Opening " + app)
            os.system(app)
    
    def respond(self, response):
        print(response)
        subprocess.call("say " + response, shell=True)


class SpeechRecognition():
    def __init__(self):
        self.running = True

    def init_speech(self, r):
        def play_audio(filename):
            chunk = 1024
            wf = wave.open(filename)
            pa = pyaudio.PyAudio()
            stream = pa.open(
                format = pa.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True
            )
            data_stream = wf.readframes(chunk) 
            while data_stream:
                stream.write(data_stream)
                data_stream = wf.readframes(chunk)
            stream.close()
            pa.terminate()

        def say(text):
            subprocess.call("say " + text, shell=True)

        print("Listening...")
        play_audio("audios/audio_init.wav")   
        with sr.Microphone() as source:
            say("Say something")
            audio = r.listen(source)      
        play_audio("audios/audio_end.wav")

        command = ""  
        try:
            # bing, google, google_cloud, houndify, ibm, sphinx, wit, ...
            command = r.recognize_google(audio)
            command = command.lower().encode("utf-8")
        except:        
            say("I couldn't understand you")
        
        print("You said:", command)
        print(command)
        if command in ["quit", "exit", "bye", "goodbye"]:            
                self.running = False
                say("Goodbye mate")          
        cmd.discover(command)

# Main call
if __name__ == "__main__":
    r = sr.Recognizer()
    s = SpeechRecognition()
    cmd = Commander()
    
    while s.running == True:
        s.init_speech(r)
