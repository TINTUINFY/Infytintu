from posixpath import split
import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam, OutputParam
from Common.Library.CustomException import CustomException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import pandas as pd
from pathlib import Path
from configparser import ConfigParser
configur = ConfigParser()
configur.read(r'C:\Bot repo\PythonBots\bots\WebCrawling\config.ini')

class WebCrawl(Bot):
    """The bot is indented to create CSV files with desired attributes

    Args:
        Bot (Abstract Class): Abstract class
    """
    def execute(self, context: dict):
        returncontext = super().execute(context)
        url = context.get("website")
        output_folder = context.get("output_folder")
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options, executable_path=configur.get('INSTALLATION','chromepath'))
        driver.set_window_size(1920, 1080)
        driver.get(url)

        try:
            content=driver.page_source
            dom = etree.HTML(content)
            tree = etree.ElementTree(dom)
            xpath_string = '//*'
            elements = tree.xpath(xpath_string)
            values_list = []
            for element in elements:
                if element.tag not in ["script", "style"]:
                    html_text = element.text
                else:
                    html_text = ""
                xpath = tree.getpath(element)
                parent_tag = elements.index(element.getparent()) if element.getparent() else None
                values_dict = {
                "tag": element.tag,
                "text":  html_text, 
                "class": element.get('class'), 
                "id_value": element.get('id'),
                "name": element.get('name'),
                "value": element.get('value'),
                "src": element.get('src'),
                "alt": element.get('alt'),
                "href": element.get('href'),
                "tooltip": element.get('title'),
                "xpath": xpath,
                "parent_tag": parent_tag}
                values_list.append(values_dict)
            df = pd.DataFrame.from_dict(values_list)
            filename = Path(output_folder)/(url.split('//')[-1].replace('/','_')+'.csv')
            df.to_csv(filename , index=True, index_label='ID')
            returncontext["status"] = "success"           
            return returncontext

        except Exception as A:
            raise CustomException(A)
        
        finally:
            driver.close()

    def input(self) -> InputParam:
        d = super().input()
        e = {"website": ["string", "None", "Full website URL. Cannot be empty."],
            "output_folder": ["string", "None", "Valid Path to output folder. Cannot be empty."]}
        return d | e        

    def output(self) -> OutputParam:
        d = super().output()
        e = {"success": ["string", "None", "The CSV file successfully generated or not."]}
        return d | e 
            
    def notes(self):
        return """This bot creates a CSV file for desired attributes"""

if __name__ == "__main__":
    context = {"website": "https://www.python.org/",
                "output_folder": r"C:\Bot repo\PythonBots\bots\WebCrawling\test_websites"}
    bot = WebCrawl()
    bot.bot_init()
    output = bot.execute(context)
    print(output)
    