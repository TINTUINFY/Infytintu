from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
import logging
import smtplib
import maskpass
import os
from email.message import EmailMessage


class MissingFilesEmailReporter(Bot):

    def execute(self,context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            list=[]
            txt_file=context.get("Path_of_TxtFile")
            source_file = context.get("Path_of_SourceFile")
            if os.path.exists(txt_file) == False or os.path.exists(source_file) == False:
                raise Exception("directiry does not exist")
            txt_file = open(txt_file)
            file_contents = txt_file.read()
            file_names = file_contents.splitlines()
            if file_names =='':
                raise Exception("There are no file names in the given txt file")
            
            for file in file_names:
                file_name= source_file+"/"+file
                if os.path.exists(file_name) == False:
                    list.append(file)
            if not list:
                raise Exception("There are no missing files in the source folder")
            From_mail = context.get("From_mail")
            To_mail = context.get("To_mail")
            Password = context.get("Password") 
            if (From_mail == '') or (To_mail == ''):
                raise Exception("one of the expected input is not entered. please check")
            msg = EmailMessage()
            msg['Subject'] = 'Missing File Names!'
            msg['From'] = From_mail
            msg['To'] = To_mail
            message = """Hi there! \n\nplease find the missing files: """
            files = "\r\n".join(list)
            msg.set_content(message +"\n"+ files)
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
        e = {"Path_of_TxtFile":["string","None","Enter the path of the Text file"],"Path_of_SourceFile":["string","None","Enter the path of the source folder"],"To_mail":["string","None","Enter To_mail id"],"From_mail":["string","None","Enter From_mail id"],"Password":["string","None","Enter the password"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d
    
    def notes(self):
        d = "Every weekend a text file will be recieved from Client with list of files that are sent from their end. Bot will check if all the files mentioned in the text files are available in our source location and the files are matching specific naming pattern or not.This Bot will send an email with list of missing files which will be used to follow up with Client to get the files ."
        return d

if __name__ == "__main__":
    t = MissingFilesEmailReporter()
    print(t.notes())
    context = {"Path_of_TxtFile":"D:\datascience project\client.txt","Path_of_SourceFile":"D:\datascience project\Test Folder","To_mail":"dhanu.kotaa@gmail.com","From_mail":"dhanu.kotaa@gmail.com","Password": maskpass.askpass(prompt="Password:", mask="#")}
    print(t.execute(context))
   
