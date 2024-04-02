import os,sys;sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import requests
import json
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
import logging

#TODO: This doesn't seem a good class. ticket generation adn acknowldgement both? Needs to be corrected
class TicketGenerationAckbot(Bot):

    def execute(self,context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            url = context.get("url")
            user = context.get("User")
            pwd = context.get("Password")
            headers = { "Accept": "application/json","Content.Type": "application/json"}
            payload = {"short_description":context.get("short_description"),
            "impact":context.get("Impact"),
            "urgency":context.get("Urgency"),
            "category":context.get("Category"),
            "state":"In Progress",
            "comments" : "Hi, You have reached to service desk queue. we will look into the incident as soon as we can"}
            response= requests.post(url,auth=(user,pwd),headers=headers,data=json.dumps(payload))
            if response.status_code != 201: 
               raise Exception("User not authenticated")
            result = {}
            return self.passcontext(result)
        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"url":["string","None","Enter service now URL"],
        "User":["string","None","enter the username to login to service now"],
        "Password":["string","None","Enter the password"],
        "short_description":["string","None","give short description of the issue "],
        "Category":["string","None","Enter one from these a.Inquiry/help , b.Software , c.Hardware, d.Network, e.Database"],
        "Impact":["string","None","select one option from these 1. 1-High , 2. 2-Medium , 3. 3-Low"],
        "Urgency":["string","None","select one option from these 1. 1-High , 2. 2-Medium , 3. 3-Low"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d
    
    def helpers(self):
        d = super().helpers()
        d["notes"] = "This Bot generates an incident with the given inputs for the fields in service now and acknowledge it."
        return d

if __name__ == "__main__":
    import maskpass
    t = TicketGenerationAckbot()
    url= "" #"https://dev85417.service-now.com/api/now/table/incident"
    context = {"url":url,"User":"admin","Password": maskpass.askpass(prompt="Password:", mask="#"),"short_description":"Generated ticket from python script",
            "Category":"Software","Impact":"1","Urgency":"2"}
    print(t.execute(context))
   
