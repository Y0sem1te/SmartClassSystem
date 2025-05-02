import torch
from torchvision.models import resnet101
from torchvision import transforms
# from pipeline_module.face_detection_module import FaceDetectionModule
import numpy as np
from PIL import Image
from face_recog.models.face_boxes_location import FaceBoxesLocation
class SentimentDetector:
    def __init__(self):
        self.model = resnet101(pretrained=False).to('cuda')
        self.model.fc = torch.nn.Linear(2048, 8).to('cuda')
        self.model.load_state_dict(torch.load(r"weights/sentiment.pth"))
        self.model.eval()
        self.face_detection = FaceBoxesLocation()
        self.sentiment=['Neutral','Happy','Sad','Surprise','Fear','Disgust','Anger','Contempt']

        self.tfm = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet 标准化
        ])

    def detect(self,img):
        face_locations = self.face_detection.face_location(img)
        sentiment_number={}
        for x1,y1,x2,y2 in face_locations:
            face_crop = img[int(y1):int(y2),int(x1):int(x2)]
            face_crop = Image.fromarray(face_crop)
            res=self.model(self.tfm(face_crop).unsqueeze(0).to('cuda'))
            output = res.argmax(dim=1).item()
            sentiment_number[self.sentiment[output]] = sentiment_number.get(self.sentiment[output], 0) + 1
        return sentiment_number

        