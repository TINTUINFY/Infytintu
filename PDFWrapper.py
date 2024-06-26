import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

class PDFWrapper():
    
    def __init__(self, file):
        self.file = file
        
    def read_pdf_resume(self):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(self.file, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True,check_extractable=True):           
                page_interpreter.process_page(page)     
            text = fake_file_handle.getvalue() 
        # close open handles      
        converter.close() 
        fake_file_handle.close() 
        if text:     
            return text
            