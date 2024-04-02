import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import logging
from Common.Library.FilePath import FilePath
from Common.Office.PptWrapper import PptWrapper
from Common.Office.csvWrapper import csvWrapper
from Common.Office.WordWrapper import WordWrapper
from Common.Library.CustomException import CustomException
from Knowledge.SubtitleGenerator import SubtitleGenerator

class TextExtracter():

    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.__file = FilePath(filepath)
            
        if(self.__file.is_csv()):
            text = self.__extract_csv()

        elif(self.__file.is_ppt()):
            text = self.__extract_ppt()
        
        elif(self.__file.is_video()):
            text = self.__extract_video()

        else:
            try:
                text = self.__extract_word()
            except Exception as ex:
                logging.error(ex)
                raise CustomException("File not supported")
        self.text = text


    def __extract_csv(self):
        file= csvWrapper(self.__file.path)
        text = file.read_csv()
        return text

    def __extract_ppt(self):
        file= PptWrapper(self.__file.path)
        text = file.read_ppt() 
        return text
    
    def __extract_word(self):
        file= WordWrapper(self.__file.path)   
        text= file.read_word_resume()
        return text
    
    def __extract_video(self):
        context = {"videofile": self.__file.path, "outputformat":"string"}
        bot = SubtitleGenerator()
        bot.bot_init()
        output = bot.execute(context)
        text= output["subtitles"]
        return text