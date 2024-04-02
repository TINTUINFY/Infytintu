import sys,os;sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Library.CustomException import CustomException
from Common.Interface.abstract_bot import Bot
from Common.WebUtilities.WebRequest import WebRequest

class ApiCall(Bot):
    """The bot is intend to make api request and get json output"""
    
    def execute(self, context: dict):
        try:
            url = context['url']
            reqType = context.get('reqType','get')
            params = context.get('params', None)
            auth = context.get('auth', None)
            headers = context.get('headers', None)
            json = context.get('json', None)
            data = context.get('data', None)
            result, status = WebRequest(url=url,reqType=reqType, params=params, auth=auth, headers=headers,json=json,data=data)
            return {'result': result, 'status': status}
        except Exception as e:
            return self.errorcontext({}, e)
    def inputs(self):
        inputs = {
            "url": ['String', "None", "The url of the request"],
            "reqType": ['String', "Get", "Type of request either Get/Post"],
            "params": ['dict,list of tuples,bytes', "None", "Tto send a query string to specified url"],
            "auth": ['tuple', "None", "A tuple to enable a certain HTTP authentication"],
            "headers": ['dict', "None", "A dictionary of HTTP headers to send to the specified url"],
            "json": ['dict', "None", "A json object to send to specified post url"],
            "data": ['dict,list of tuples,bytes,file object', "None", "any data send to the specified url"]
        }
        return inputs | super().inputs()
    
    def outputs(self):
        d = {"result": ["dict", "returns result json output"],
            "status": ["boolean", "returns status of request"]
            }
        return d | super().outputs()

if __name__ == "__main__":
    context = {'url': "http://127.0.0.1:8000/"}
    print(ApiCall().execute(context=context))
