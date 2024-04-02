

import os
import inspect
from shutil import rmtree, move

def movetoparent(src, dest):
    m = os.walk(src)
    root, dir, files = next(m)
    for d in dir:
        move(os.path.join(root, d), dest)
    for f in files:
        move(os.path.join(root, f), dest)
    rmtree(src)



def get_callerfuncpath(real: bool = False, level=1) -> str:
    """Return caller's current file path."""
    frame = inspect.stack()[level]
    p = frame[0].f_code.co_filename
    if real:
        return os.path.realpath(p)
    return p

def convert_to_respective_type(inputParamValue):
        if inputParamValue.lower() == "true":
            return True
        if inputParamValue.lower() == "none":
            return None
        if inputParamValue.lower() == "false":
            return False
        if inputParamValue[0] == '[':
            return eval(inputParamValue)
            
        if inputParamValue[0] == '{':
            return eval(inputParamValue)
        if inputParamValue[0].isdigit():
            return eval(inputParamValue)
        if inputParamValue[0] == "'" or inputParamValue[0]=='"':
            return inputParamValue[1:-1]
        return inputParamValue #"'" + inputParamValue + "'"

class bcolors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    EMPTY = ''
    @staticmethod
    def dictdata(ifformat):
        d={}
        if ifformat:
            d["m"] = bcolors.MAGENTA
            d["e"] = bcolors.ENDC
            d["i"] = bcolors.ITALIC
            d["r"] = bcolors.RED
            d["c"] = bcolors.CYAN
            d["y"] = bcolors.YELLOW
            d["b"] = bcolors.BLUE
            d["g"] = bcolors.GREEN
            d["u"] = bcolors.UNDERLINE
            d["w"] = bcolors.BOLD
        else:
            d["m"] = bcolors.EMPTY
            d["e"] = bcolors.EMPTY
            d["i"] = bcolors.EMPTY
            d["r"] = bcolors.EMPTY
            d["c"] = bcolors.EMPTY
            d["y"] = bcolors.EMPTY
            d["b"] = bcolors.EMPTY
            d["g"] = bcolors.EMPTY
            d["u"] = bcolors.EMPTY
            d["w"] = bcolors.EMPTY
        return d
