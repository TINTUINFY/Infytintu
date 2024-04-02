import win32com.client

class Outlook():
    
    def Outlook_Connection():
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        if (outlook == None):
            raise Exception("Outlook is not installed in this system")
        inbox = outlook.GetDefaultFolder(6)
        messages = inbox.Items 
        if len(messages) == 0:
             raise Exception("No messages or mails found") 
        return messages
                
  
         
        
            
   
        


        
        
        
        


        