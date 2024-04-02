import os
import shutil

CURRDIR=""

class FilePath():
    '''
    classdocs
    '''


    def __init__(self, file):
        '''
        Constructor
        '''
        if not os.path.isabs(file):
            if CURRDIR == "":
                file = os.path.abspath(file)
            else:
                file = os.path.abspath(os.path.join(CURRDIR,file))
        self.path = file

    def moveto(self, dest_path):
        shutil.move(self.path, dest_path)
        self.path = dest_path
        
    def ext(self):
        return os.path.splitext(self.path)[1].lower()
    
    def is_excel(self):
        return (self.ext() in (".xls",".xlsx",".xlsm",".xlsb"))
            
    def is_csv(self):
        return (self.ext() in (".csv",".txt"))
    
    def is_ppt(self):
        return (self.ext() in (".pptx", ".pptm", ".pptb"))
    
    def is_text(self):
        return (self.ext() in (".csv",".txt"))

    def is_video(self):
        return (self.ext() in (".mp4",".3gpp",".webm", ".avi",".wmv", ".3gp"))
    
    def first_line(self):
        if(self.is_text()):
            f=open(self.path, encoding='utf-8')
            m = f.readline()
            f.close()
            return m
        else:
            return ""
        
    def get_text(self):
        fp = open(self.path,"r", errors="ignore")
        txt = fp.read()
        fp.close()
        return txt
    
