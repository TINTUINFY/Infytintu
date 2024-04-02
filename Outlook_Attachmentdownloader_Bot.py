import sys, os
import tempfile
from Common.Office.outlook import Outlook as O
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
import logging
import datetime

class OutlookAttachmentDownloader(Bot):

    def execute(self,context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            attachment_list = []
            Input_Email_Sender_List = context.get("Email_Sender_List")
            if(Input_Email_Sender_List == []):
                raise Exception("Email sender is required to proceed")
            Input_Attachment_List = context.get("Attachment_List")
            messages = O.Outlook_Connection()
            today = datetime.date.today()
            sender = ''
            messages = messages.Restrict("[ReceivedTime] >= today")
            if messages.count == 0:
               raise Exception("No mails for today date")
            for message in messages:
                if(message.SenderEmailType == "EX"):
                    sender = message.Sender.GetExchangeUser().PrimarySmtpAddress
                else:
                    sender = message.SenderEmailAddress
                if sender in Input_Email_Sender_List:
                    if message.Attachments.count != 0:
                        attachments = message.Attachments
                        attachment_list.append(attachments)
                       
            if (attachment_list == []):
                raise Exception("no attachments or mails from the user to download")
        
            for attachments in attachment_list:
                for attachment in attachments:
                    if (Input_Attachment_List == []) or (str(attachment) in Input_Attachment_List):
                        attachment.SaveAsFile(os.path.join(tempfile.gettempdir(), str(attachment)))
            result = {}
            return self.passcontext(result)
        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"Email_Sender_List": ["list", "None", "Please provide Emil_sender_list"],
            "Attachment_List":["list","None","list of attachments that needs to be downloaded (optional)"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d
        
    def helpers(self):
        d = "This bot uses outlook class to connect to outlook and get the inbox mails.It saves the attachments of outlook current date inbox mails for the provided emailsender in temp directory.This bot saves only current date inbox mail attachment.If attachment_name(optional parameter) is NOT given then downloads all the attachments else downloads required attachments based on the attachement name passed as input parameter"
        return d


if __name__ == "__main__":
    t = OutlookAttachmentDownloader()
    print(t.helpers())
    context = {"Email_Sender_List":['anirudh.v01@infosys.com'],"Attachment_List":[]}
    print(t.execute(context))
    
