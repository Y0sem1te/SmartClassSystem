from ultralytics import YOLO
import supervision as sv

class SentimentDetector:
    def __init__(self):
        self.model = YOLO("../weights/sentiment.pth").to('cuda')
    def detect(self,img):
        res=self.model(img)
        