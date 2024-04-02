import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam
from Common.Library.CustomException import CustomException
from Common.GoogleAPI.RecognizeGoogleAPI import RecognizeGoogleAPI
from Common.Library.ConfigurationSettings import GetTempFile
from pathvalidate import ValidationError, validate_filename
import speech_recognition, os

class SpeechRecognitionBot(Bot):
    def execute(self, context: dict):
        returncontext = super().execute(context)
        print("Inside Execute")

        audio_file = context.get("path")
        if audio_file is not None:
            if os.path.splitext(audio_file)[1].lower() != ".wav":
                raise CustomException("Please enter a audio file in wav format")

            try:
                # Call API class 
                api = RecognizeGoogleAPI()          
                text = api.Speech_to_text_converter(audio_file)

                # File name validation    
                try:
                    validate_filename(context.get("filename")) 
                except ValidationError:
                    raise CustomException("Invalid file name") 

                # Write to text file    
                f = GetTempFile(context.get("filename"))
                with open(f, "w") as file:
                    print("Saving to text file")
                    file.write(text)

            except FileNotFoundError:
                raise CustomException("File not found")
            except speech_recognition.UnknownValueError:
                raise CustomException("Invalid audio data")
        else:
            raise CustomException("Please specify the path")
            
        returncontext["status"] = "success"  
        return returncontext

    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"path": ["string", "None", "Valid path for audio file in wav format. The audio file should contain english speech."],
                "filename": ["string", "None", "Text file name. File name should not be empty. File name should not contain any special charters(- and _ are allowed)"]}
        return d | e

    def notes(self):
        return """This is a speech to text converter bot. The input to this bot is an wav audio file with english speech, 
        the bot converts the audio into text and saves it in a txt file at temporary location.
        WARNING: The data will be passed to Google API for conversion.
        """

if __name__ == "__main__":
    filename = "sample\\machine-learning_speech-recognition_7601-291468-0006.wav"
    path = os.path.join(os.path.dirname(__file__),filename)
    context = {"path": path,
                "filename":"Audio_1.txt"}
    r = SpeechRecognitionBot()
    r.bot_init()
    print(r.execute(context))
