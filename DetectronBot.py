import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.ConfigurationSettings import GetApplicationDirectory
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, random
import cv2
import matplotlib.pyplot as plt
from detectron2.utils.visualizer import ColorMode

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog


class DetectronBot(Bot):
    
    def execute(self, context: dict):
        
        try:
            path=GetApplicationDirectory()
            if os.path.exists(os.path.join(path,'output','model_final.pth')):
                trained=1
            if trained==1:
                
                cfg = get_cfg()
                # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
                cfg.merge_from_file(os.path.join(path,'output','model_config.yaml'))
                cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # set threshold for this model
                # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
                #cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
                cfg.MODEL.WEIGHTS=os.path.join(path,'output','model_final.pth')
                cfg.MODEL.DEVICE = 'cpu'
                predictor = DefaultPredictor(cfg)
                img_file = context['img']
                if os.path.exists(img_file) == False:
                    raise Exception("directiry does not exist")
                im = cv2.imread(img_file)
                outputs = predictor(im)  # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
                v = Visualizer(im[:, :, ::-1], 
                                scale=0.5, 
                                instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
                )
                print(outputs["instances"])
                out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

                plt.rcParams["figure.figsize"] = (20,6)
                plt.imshow(out.get_image()[:, :, ::-1])
                plt.show()
            else:
                train_json = context['train_json']
                val_json = context['val_json']
                train_path = context['train_path']
                val_path = context['val_path']
                thing_classes = context['thing_classes']
                Data_Resister_training="app_train"
                Data_Resister_valid="app_valid"
                from detectron2.data.datasets import register_coco_instances

                register_coco_instances(Data_Resister_training,{}, train_json, train_path)
                register_coco_instances(Data_Resister_valid,{},val_json, val_path)

                    
                MetadataCatalog.get(Data_Resister_training).set(thing_classes=thing_classes)
                MetadataCatalog.get(Data_Resister_valid).set(thing_classes=thing_classes)
                metadata = MetadataCatalog.get(Data_Resister_training)

                dataset_train = DatasetCatalog.get(Data_Resister_training)
                dataset_valid = DatasetCatalog.get(Data_Resister_valid)

                from detectron2.engine import DefaultTrainer

                cfg = get_cfg()
                cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
                cfg.DATASETS.TRAIN = (Data_Resister_training,)
                cfg.DATASETS.TEST = ()
                cfg.DATALOADER.NUM_WORKERS = 2
                #cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
                cfg.MODEL.WEIGHTS=os.path.join(path,'model_final_f10217.pkl') #Download weight from https://dl.fbaipublicfiles.com/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl
                cfg.SOLVER.IMS_PER_BATCH = 2  # This is the real "batch size" commonly known to deep learning people
                cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
                cfg.SOLVER.MAX_ITER = 1000
                cfg.SOLVER.STEPS = []        # do not decay learning rate
                cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
                cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
                # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
                cfg.MODEL.RETINANET.NUM_CLASSES=3
                cfg.OUTPUT_DIR=os.path.join(path,'output')
                os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
                trainer = DefaultTrainer(cfg) 
                trainer.resume_or_load(resume=False)
                trainer.train()

                with open(os.path.join(path,'output','model_config.yaml'), 'w') as conf:
                    conf.write(cfg.dump())

        except Exception as e:
            return self.errorcontext({}, e)
    def inputs(self) -> InputParam:
        d = super().inputs()
        return d

    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d

if __name__ == "__main__":
    bot_obj=DetectronBot()
    bot_obj.bot_init()

    img=r"C:\Users\vikas33\Desktop\Project\TitleExtraction\dataset\val\Capture44.JPG"
    train_json=r"C:\Users\vikas33\Desktop\Project\TitleExtraction\dataset\train\train.json"
    val_json=r"C:\Users\vikas33\Desktop\Project\TitleExtraction\dataset\val\val.json"
    train_path=r"C:\Users\vikas33\Desktop\Project\TitleExtraction\dataset\train"
    val_path=r"C:\Users\vikas33\Desktop\Project\TitleExtraction\dataset\val"
    thing_classes=["Title","Menu","Ribbon"]

    context = {'train_json': train_json,'val_json':val_json,'train_path':train_path,'val_path':val_path,'thing_classes':thing_classes,'img': img}
    bot_obj.execute(context=context)