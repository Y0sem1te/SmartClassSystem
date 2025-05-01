from pipeline_module.core.base_module import BaseModule, TASK_DATA_OK
import torch
from torchvision import transforms
from PIL import Image
from torchvision.models import resnet101
import cv2

class SentimentModule(BaseModule):
    def __init__(self, model_path, device='cpu'):
        super(SentimentModule, self).__init__()
        self.device = device
        self.model = resnet101(pretrained=False) # 使用ResNet101模型
        self.model.fc = torch.nn.Linear(2048, 8)
        self.model.load_state_dict(torch.load(model_path,weights_only=True, map_location=self.device))
        self.model.to(self.device)
        

    def process_data(self, data):
        self.model.eval()
        sentiment = ["neural", "happy", "sadness", "surprise", "fear", "disgust", "anger", "contempt"]
        frame = data.frame
        # if not face_locations:
        #     return TASK_DATA_OK
        face_locations = data.face_locations  # 获取人脸位置
        faces = []
        h, w = frame.shape[:2]
        for x1,y1,x2,y2 in face_locations:
            # 1) 规范化 & 限制到图像范围内
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(w, int(x2)), min(h, int(y2))
            # 2) 排除无效框
            if x2 <= x1 or y2 <= y1:
                continue
            roi = frame[y1:y2, x1:x2]
            # 3) 再次排除空数据
            if roi is None or roi.size == 0:
                continue
            # 4) 只有有效 roi 才 preprocess
            faces.append(self.preprocess(roi))

        #faces = [self.preprocess(frame[int(y1):int(y2),int(x1):int(x2)]) for x1,y1,x2,y2 in face_locations]
        # input_tensor = self.preprocess(frame)  # 数据预处理
        with torch.no_grad():
            outputs = [self.model(face) for face in faces]
            # output = self.model(input_tensor)  # 模型推理
            outputs = [output.argmax(dim=1).item() for output in outputs]
            # output = output.argmax(dim=1).item()  # 获取预测结果
            # output=sentiment[output]  # 获取预测结果
            outputs = [sentiment[i] for i in outputs]
        data.sentiments = outputs  # 将结果存储到 `data` 中
        data.detections = torch.rand((1,6))
        data.keypoints = torch.rand((1, 136, 1))
        data.keypoints_scores =torch.ones((1,136,2))
        return outputs

    def preprocess(self, frame):
        train_tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet 标准化
        ])
        # 将帧转换为模型输入格式
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = train_tfm(Image.fromarray(frame))
        input_tensor=input_tensor.unsqueeze(0).float().to(self.device)
        return input_tensor
    
    def open(self):
        super(SentimentModule, self).open()
        pass