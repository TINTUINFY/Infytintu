import speech_recognition as sr

class RecognizeGoogleAPI:
    def Speech_to_text_converter(self, audio_file):
        a = sr.Recognizer() # initialize the recognize
        with sr.AudioFile(audio_file) as source:
            audio_data = a.record(source) # load audio to memory
            text = a.recognize_google(audio_data) # convert from speech to text
            return text