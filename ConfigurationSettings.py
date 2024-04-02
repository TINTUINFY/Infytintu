import configparser
import os, tempfile
import appdirs

from Common.Library.CommonFunctions import get_callerfuncpath, movetoparent
from shutil import copy
import zipfile
import pickle

DEFAULTFOLDER = ""

def GetApplicationDirectory():
    p = appdirs.user_data_dir("bots","Infosys")
    if DEFAULTFOLDER:
        p = os.path.join(p,DEFAULTFOLDER)
    if not os.path.isdir(p):
        os.makedirs(p)
    return p

def GetApplicationTempDirectory():
    p = os.path.join(tempfile.gettempdir(),"Infosys","bots", DEFAULTFOLDER)
    if not os.path.isdir(p):
        os.makedirs(p)
    return p

def GetBotDirectory():
    return os.path.join(os.path.dirname(__file__),"../../")

def GetEnvironmentVariable(variable:str):
    return os.environ[variable]

def GetTempFile(filename):
    return os.path.join(GetApplicationTempDirectory(), filename)

def SavePickle(filename, object):
    with open(filename, 'wb') as fh:
        pickle.dump(object, fh)

def LoadPickle(filename):
    with open(filename, 'rb') as fh:
        return pickle.load(fh)

def GetModel(section, name, modelname):
    m = ReadFromConfigFile(section, name, modelname)
    path = GetAppFile(m)
    if os.path.exists(path):
        WriteToConfigFile(section,name, m)
        return path
    else:
        p = get_callerfuncpath(real=True, level=2)
        d = os.path.dirname(p)
        mpath = os.path.join(d, m)
        if os.path.exists(mpath):
            copy(mpath, path)
        elif os.path.exists(mpath +".zip"):
            with zipfile.ZipFile(mpath +".zip", 'r') as zip_ref:
                zip_ref.extractall(path)
            if(os.path.exists(os.path.join(path, m))):
                movetoparent(os.path.join(path, m), path)
        elif os.path.exists(os.path.join(GetBotDirectory(),"..","PretrainedModels",m +".zip")):
            with zipfile.ZipFile(os.path.join(GetBotDirectory(),"..","PretrainedModels",m +".zip"), 'r') as zip_ref:
                zip_ref.extractall(path)
            if(os.path.exists(os.path.join(path, m))):
                movetoparent(os.path.join(path, m), path)
        else:
            return ""
        WriteToConfigFile(section,name, m)
        return path

def GetAppFile(filename):
    return os.path.join(GetApplicationDirectory(), filename)

def GetConfigFile():
    d = GetApplicationDirectory()
    fname = os.path.join(d,"InfosysBotConfig.ini")
    return fname

def ReadFromConfigFile(section,attribute, default=""):
    config = configparser.ConfigParser()
    configfile = GetConfigFile()
    if os.path.isfile(configfile):
        config.read(configfile)
        return config.get(section,attribute,fallback=default)
    return default
    
def WriteToConfigFile(section, attribute, value):
    config = configparser.ConfigParser()
    configfile = GetConfigFile()
    if os.path.isfile(configfile):
        config.read(configfile)
    if section not in config:
        config[section] = {}
    config[section][attribute] = value
    with open(configfile, "w") as fp:
        config.write(fp)
    
def GetAppFolder(foldername):
    Cache_directory = os.path.join(GetApplicationDirectory(), foldername)
    if not os.path.isdir(Cache_directory):
        os.makedirs(Cache_directory)
    return Cache_directory