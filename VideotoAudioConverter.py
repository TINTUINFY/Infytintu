import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Interface.abstract_bot import Bot
from Common.Library.ConfigurationSettings import GetTempFile
import moviepy.editor as mp

class VideoConverter(Bot):
    """This bot converts video to audio"""
    __version__ = "1.0.0"
    def execute(self, context: dict):
        returncontext = super().execute(context)
        try:
            self.register_variables(context)
            with mp.VideoFileClip(self.filepath) as clip:
                audio_path = GetTempFile("audio.wav")
                clip.audio.write_audiofile(audio_path, codec='pcm_s16le',logger=None, ffmpeg_params=["-ac", "1"])
            returncontext["audio_path"] = audio_path
            return returncontext
        except Exception as e:
            return self.errorcontext({}, e)
        
    def inputs(self):
        inputs = {
            "filepath": ["path", "None", "Path for the video file"]
        }
        return inputs | super().inputs()

    def outputs(self):
        d = {
            "audio_path": ["path", "path of the audio file generated"]
        }
        return d | super().outputs()

    def helpers(self):
        h= super().helpers()
        h["errors"] = ""
        h["keywords"] = "video, audio, converter"
        h["notes"] = ""
        return h

if __name__ == "__main__":
    context = {}
    print(VideoConverter().execute(context=context))