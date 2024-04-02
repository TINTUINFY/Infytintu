import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Interface.abstract_bot import Bot
from Common.Library.CustomException import CustomException
import pytesseract
from layoutlm_preprocess import *
from pdf2image import convert_from_path
from torch.nn import CrossEntropyLoss
import cv2
import warnings

warnings.filterwarnings("ignore")

class LayoutlmInvoiceConversion(Bot):
    """This class is a wrapper around LayoutlmInvoiceConversion"""
    __version__ = "1.0.0"
    def execute(self, context: dict):
        # returncontext = super().execute(context)
        # print("executed1")
        try:
            returncontext = super().execute(context)
            tesseractpath = context.get("tesseractpath")
            path = context.get("imagepath")
            labelpath = context.get("labelpath")
            modelparameter = context['modelparameterpath']
            # print(tesseractpath)
            # print(path)
            # print(labelpath)
            # print(modelparameter)

            pytesseract.pytesseract.tesseract_cmd = tesseractpath

            originalinvoice = context['pdfpath']
            # print(originalinvoice)
            if not os.path.exists(originalinvoice):
                print("file not found")
                return CustomException("Input File Not Found")
            else:
                if not os.path.isfile(originalinvoice):
                    print("path not found")
                    return CustomException("Provided input path is not a file")

            pages = convert_from_path(originalinvoice,poppler_path=r"C:\Users\tintu.thomas02\Downloads\Release-22.04.0-0 (1)\poppler-22.04.0\Library\bin")
            print(pages)
            for image in pages:
                # print("executed")
                image.save(path)
                # image.save('output.png')
            
            # TODO: Add your code
            # def get_labels(labelpath):
            #     with open(labelpath, "r") as f:
            #         print("executed1")
            #         labels = f.read().splitlines()
            #     if "O" not in labels:
            #         labels = ["O"] + labels
            #     return labels

            # labels = get_labels(labelpath)
            labels = ['O', 'B-ANSWER', 'B-BILLINGADDRESSDETAILS', 'B-BILLING_ADDRESS_HEADER', 'B-HEADER', 'B-OTHERS', 'B-QUESTION', 'B-SHIPPINGADDRESSDETAILS', 'B-SHIPPINGADDRESSHEADER', 'B-SOLDBYDETAILS', 'B-SOLDBYHEADER', 'E-ANSWER', 'E-BILLINGADDRESSDETAILS', 'E-BILLING_ADDRESS_HEADER', 'E-HEADER', 'E-OTHERS', 'E-QUESTION', 'E-SHIPPINGADDRESSDETAILS', 'E-SHIPPINGADDRESSHEADER', 'E-SOLDBYDETAILS', 'E-SOLDBYHEADER', 'I-ANSWER', 'I-BILLINGADDRESSDETAILS', 'I-BILLING_ADDRESS_HEADER', 'I-HEADER', 'I-OTHERS', 'I-QUESTION', 'I-SHIPPINGADDRESSDETAILS', 'I-SHIPPINGADDRESSHEADER', 'I-SOLDBYDETAILS', 'I-SOLDBYHEADER', 'S-ANSWER', 'S-BILLINGADDRESSDETAILS', 'S-BILLING_ADDRESS_HEADER', 'S-HEADER', 'S-OTHERS', 'S-QUESTION', 'S-SHIPPINGADDRESSDETAILS', 'S-SHIPPINGADDRESSHEADER', 'S-SOLDBYDETAILS', 'S-SOLDBYHEADER']
            # print(labels)
            num_labels = len(labels)
            label_map = {i: label for i, label in enumerate(labels)}
            # Use cross entropy ignore index as padding label id so that only real label ids contribute to the loss later
            pad_token_label_id = CrossEntropyLoss().ignore_index

            # PATH='./layoutlmnew15.pt'
            # print(modelparameter)
            models = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased", num_labels=num_labels)
            models.load_state_dict(torch.load(modelparameter))

            image, words, boxes, actual_boxes = preprocess(path)
            word_level_predictions, final_boxes=convert_to_features(image, words, boxes, actual_boxes, models)
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            def iob_to_label(label):
                if label != 'O':
                    return label[2:]
                else:
                    return ""
            label2color = {'QUESTION':'blue','question':'blue','ANSWER':'green','answer':'green','BILLING_ADDRESS_HEADER':'orange','billing_address_header':'orange','BILLINGADDRESSDETAILS':'violet','billingaddressdetails':'violet','HEADER':'red','SOLDBYHEADER':'black','soldbyheader':'black','SOLDBYDETAILS':'green','soldbydetails':'green','SHIPPINGADDRESSHEADER':'yellow','shippingaddressheader':'yellow','SHIPPINGADDRESSDETAILS':'magenta','shippingaddressdetails':'magenta','OTHERS':'black','':'violet','header':'red','others':'black'}

            for prediction, box in zip(word_level_predictions, final_boxes):
                predicted_label = iob_to_label(label_map[prediction]).lower()
                draw.rectangle(box, outline=label2color[predicted_label])
                draw.text((box[0] + 10, box[1] - 10), text=predicted_label, fill=label2color[predicted_label], font=font)
         
            def bounding_box_img(img,bbox):
                x_min, y_min, x_max, y_max = bbox
                bbox_obj = img[y_min-4:y_max+4, x_min-4:x_max+4]
                return bbox_obj
            
            img = cv2.imread(path)
            address = []
            str1 = " "
            for i in range(len(word_level_predictions)):
                if iob_to_label(label_map[word_level_predictions[i]]).lower() == "billingaddressdetails":
                    cropped_img = bounding_box_img(img,final_boxes[i])
                    text = pytesseract.image_to_string(cropped_img)
                    address.append(text)
                    # print(text)
            s = [i.rstrip('\n') for i in address if i.endswith('\n')]
            # print(s)
            address1 = str1.join(s)
            # print(address)
            print(address1)

        except Exception as e:
            return self.errorcontext({}, e)
        
    def inputs(self):
        inputs = {
            "original_image_path": ['path', "None", "Image file path of original image"],
            "image_to_compare_path": ['path', "None", "Image file path to compare with original"],
            "similarity_threshold": ['int', "50", "Threshold percent value for image similarity"]
        }
        return inputs | super().inputs()

    def outputs(self):
        d = {
            "is_same_size": ["bool", "returns flag based on if image compared are of same size"],
            "similarity_percent": ["double", "percentage of similarity between images"],
            "is_similar": ["bool", "returns status based on whether the images are similar based on the threshold provided"],
        }
        return d | super().outputs()

    def helpers(self):
        h= super().helpers()
        h["errors"] = ""
        h["keywords"] = "configuration, settings"
        h["configuration"] = ""
        h["notes"] = "This bot can be used as workflow setting parameters like login credentials, database, pretrained model path, etc. Note: This needs to be called at start of the workflow and only once"
        return h

if __name__ == "__main__":
    bot_obj=LayoutlmInvoiceConversion()
    bot_obj.bot_init()
    pdfdocument = "invoice.pdf"
    path = os.path.join(os.path.dirname(__file__),pdfdocument)
    context = {"pdfpath": path,
                "labelpath": os.path.join(os.path.dirname(__file__), 'label.txt'),
                "imagepath": os.path.join(os.path.dirname(__file__), 'output.png'),
                "modelparameterpath": os.path.join(os.path.dirname(__file__), 'layoutlmnew15.pt'),
                "tesseractpath": r"C:\Users\tintu.thomas02\AppData/Local\Tesseract-OCR\tesseract.exe",
                "popplerpath": r"C:\Users\tintu.thomas02\Pinnacle Datascience program\MylocalRepo\PythonBots\bots\LayoutlmInvoiceConversion\poppler-22.04.0\Library\bin"}
    bot_obj.execute(context=context)
