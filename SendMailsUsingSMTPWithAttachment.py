from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
import logging
import smtplib
from email.message import EmailMessage
import maskpass
import os



class SendMailsUsingSMTPWithAttachment(Bot):

    def execute(self,context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            To_mail = context.get("To_mail")
            From_mail = context.get("From_mail")
            Password = context.get("Password") 
            if (From_mail == '') or (To_mail == ''):
                raise Exception("one of the expected input is not entered. please check")
            msg = EmailMessage()
            msg['Subject'] = 'SendMailsUsingSMTPWithAttachment Bot'
            msg['From'] = From_mail
            msg['To'] = To_mail
            body = """Hi there! \n\nplease find the Attcahments: """
            msg.set_content(body)
            path = context.get("Attachments_dirpath")
            if os.path.exists(path) == False:
                raise Exception("directiry does not exist")
            files = context.get("Attachments_list")
            for f in files:
                filepath = os.path.join(path,f)
                subtype = os.path.splitext(filepath)[1][1:]
                with open(filepath, "rb") as file:
                  msg.add_attachment(file.read(),maintype ="application",subtype=subtype,filename=f)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(From_mail,Password)
                smtp.send_message(msg)
            result = {}
            return self.passcontext(result)
        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"Attchments_dirpath":["string","None","Enter the directory path of the attachments"],"Attachments_list":["list","None","Enter the attachment names"],"To_mail":["string","None","Enter To_mail id"],"From_mail":["string","None","Enter From_mail id"],"Password":["string","None","Enter the password"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d
    
    def helpers(self):
        d = "This bots Sends mail using SMTP Server activity with attachment"
        return d

if __name__ == "__main__":
    t = SendMailsUsingSMTPWithAttachment()
    print(t.helpers())
    context = {"Attachments_dirpath":"D:\datascience project","Attachments_list":['client.txt','bot.py'],"To_mail":"dhanu.kotaa@gmail.com,nagasiva.sri@gmail.com","From_mail":"dhanu.kotaa@gmail.com","Password": maskpass.askpass(prompt="Password:", mask="#")}
    print(t.execute(context))
