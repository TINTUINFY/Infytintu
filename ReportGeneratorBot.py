import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam
from Common.Library.CustomException import CustomException
from Common.MachineLearning.DataCleaningBot import DataCleaningBot
from Common.Reporting.DocumentCreation import DocumentCreation
from Common.Library.FilePath import FilePath
from Common.MachineLearning.MLReader import MLReader
from Common.Visualisation.ReportChartsBot import ReportChartsBot
from pathvalidate import ValidationError, validate_filename

class ReportGeneratorBot(Bot):
    def execute(self, context:dict):
        returncontext = super().execute(context)
        print("Inside execute")

        # Reading the file
        user_path = context.get("path")
        f = FilePath(user_path)
        
        if f.is_excel() or f.is_csv():
            mlr = MLReader(user_path)
            file = mlr.data
        else:
            raise CustomException("Please enter a file in Excel format")

        # Store different data types separately
        col = file.columns.to_series().groupby(file.dtypes).groups
        col2 = {k.name: v for k, v in col.items()}
        intcol, floatcol, objectcol, datecol = [], [], [], []
        
        for typ in col2:
            if str(typ).__contains__("int"):
                intcol = col2[typ]
            elif str(typ).__contains__("float"):
                floatcol = col2[typ]
            elif str(typ).__contains__("object"):
                objectcol = col2[typ]
            elif str(typ).__contains__("date"):
                datecol = col2[typ]
        numcols = list(intcol) + list(floatcol)
        catcols = list(objectcol) + list(datecol)
            
        # Call the data_cleaning method from DataCleaning bot
        d = DataCleaningBot()
        file = d.data_cleaning(file, catcols, numcols)

        # Call the creation method from DocumentCreation bot    
        d = DocumentCreation()
        doc = d.creation() 

        # File name validation    
        try:
            validate_filename(context.get("filename")) 
        except ValidationError:
            raise CustomException("Invalid file name") 

        # Title validation
        t = context.get("title")
        if len(t) <= 0 or len(t) > 30 or t.isspace(): # Title validation
            raise CustomException("Invalid Title")

        # Write the first page
        doc.add_heading(t,0)
        doc.add_paragraph(" ")
        doc.add_paragraph("The reports contains various types of plots as mentioned below :")
        doc.add_paragraph("Pie charts showing distribution of categorical data", style='List Bullet')
        doc.add_paragraph("Histogram charts showing distribution of numeric data", style='List Bullet')
        doc.add_paragraph("Bar charts showing comparison of avergae numeric data for every category", style='List Bullet')
        doc.add_paragraph("Donut charts showing percentage of numeric data for every category", style='List Bullet')
        doc.add_page_break()

        # Plotting starts here #
        # Plotting pie chart for categorical variables with levels upto 50
        chart = ReportChartsBot()
        chart.PieCharts(file, catcols, doc)
        chart.Histograms(file, numcols, doc)
        chart.BarplotPiechart(file, catcols, numcols, doc)
                                        
        # Call the saving method from DocumentCreation bot
        d.saving(doc, context.get("filename"))      

        returncontext["status"] = "success"  
        return returncontext

    def input(self) -> InputParam:
        d = super().input()
        e = {"path": ["string", "None", "Valid path for csv or xlsx file"],
                "filename": ["string", "None", "File name should not be empty. File name should not contain any special charters(- and _ are allowed)"],
                "title": ["string", "None", "Title can not be empty. Tilte length should be less than 31 characters"]}
        return d | e

    def notes(self):
        return """This is a Report Generator Bot. The bot takes and excel file as input and generated different plots.
        The report is geberated in word and pdf file format including pie charts, histograms and barplots of the data.
        The report files will be available in the temporary directory.
        """      

if __name__ == "__main__":
    context = {"path": r"C:\Users\pranjal.bhagat\Desktop\Report Genrating Bot\AB_NYC_2019.csv",
                "filename": "Airbnb Business Report",
                "title": "Airbnb Business Statistics"}
    r = ReportGeneratorBot()
    r.bot_init()
    r.execute(context)