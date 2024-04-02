import sys,os;sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Library.CustomException import CustomException
from Interface.iOCR import iOCR
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

class DoctrOCR(iOCR):
    def imageToText(self, imageFilePath):
        """image to text conversion method using doctr OCR

        Args:
            ImgFilePath (String): Path of input image file
            
        Returns:
            dict: Details related to image
        """
        try:
            model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
            doc = DocumentFile.from_images(imageFilePath)
            result = model(doc)
            json_output = result.export()
            return json_output
        except Exception as e:
            raise CustomException(e)

if __name__ == "__main__":
    imageFileName = "messageBox.jpg"
    imageFilePath = os.path.join(os.path.dirname(__file__),"sample",imageFileName)
    Bobj = DoctrOCR()
    output = Bobj.imageToText(imageFilePath=imageFilePath)
    print(output)