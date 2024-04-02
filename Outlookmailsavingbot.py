import tempfile
from Common.Office.outlook import Outlook as O
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
import logging
import datetime
import re

class OutlookMailSavingBot(Bot):

    def execute(self,context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            messages_List=[]
            messages = O.Outlook_Connection()
            today = datetime.date.today()
            if(context.get("Input")=="GetLastMessage"):
                messages_List.append(messages.GetLast())
            if(context.get("Input")=="TodayMessages"):
                messages = messages.Restrict("[ReceivedTime] >= today")
                if messages.count == 0:
                    raise Exception("No mails for today date")
                for message in messages:
                    messages_List.append(message)
            for message in messages_List:
                name = str(message.subject)
                #to eliminate any special charecters in the name
                name = re.sub('[^A-Za-z0-9]+', '', name)+'.msg'
                #to save in the temp directory
                message.SaveAs(tempfile.gettempdir()+'//'+name)
            result = {}
            return self.passcontext(result)
        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"Input":["string","GetLastMessage","type GetLastMessage or TodayMessages as input for bot"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d
    
    def helpers(self):
        d = "This bot uses outlook class to connect to outlook and get the inbox mail. It saves outlook inbox mails in temp directory. This bot saves current date inbox mails or last recieved mail based on the user input"
        return d

if __name__ == "__main__":
    t = OutlookMailSavingBot()
    print(t.helpers())
    context = {"Input":"GetLastMessage"}
    print(t.execute(context))
   
