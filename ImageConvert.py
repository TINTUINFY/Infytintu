import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Interface.abstract_bot import Bot
from Common.Library.ConfigurationSettings import GetTempFile
from PIL import Image

class ImageConvert(Bot):
    """The bot converts one image from one format to another"""
    __version__ = "1.0.0"
    def execute(self, context: dict):
        returncontext = super().execute(context)
        try:
            self.register_variables(context)
            if os.path.exists(self.imagepath):
                im = Image.open(self.imagepath).convert("RGB")
                newpath = GetTempFile(os.path.splitext(os.path.basename(self.imagepath))[0]+"."+self.format)
                im.save(newpath)
                returncontext["outputpath"] = newpath
            else:
                raise Exception("Incorrect Path")
            return returncontext
        except Exception as e:
            return self.errorcontext({}, e)
        
    def inputs(self):
        inputs = {
            "imagepath": ["path", "None", "Path of the input file"],
            "format": ["string", "jpg", "output format like jpg, bmp, png"]
        }
        return inputs | super().inputs()

    def outputs(self):
        d = {
            "outpath": ["path", "Path of the output file"]
        }
        return d | super().outputs()

    def helpers(self):
        h= super().helpers()
        h["errors"] = ""
        h["keywords"] = "image, jpg, webg, bmp, settings"
        h["configuration"] = ""
        h["notes"] = "This bot can be used for converting from one format to another"
        return h

if __name__ == "__main__":
    f=os.path.join(os.path.dirname(__file__),r"sample\image.webp")
    context = {"imagepath":f}
    print(ImageConvert().execute(context=context))