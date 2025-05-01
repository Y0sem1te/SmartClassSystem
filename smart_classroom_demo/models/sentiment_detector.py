import torch
from torchvision.models import resnet101
from torchvision import transforms
class SentimentDetector:
    def __init__(self):
        self.model = resnet101(pretrained=False).to('cuda')
        self.model.fc = torch.nn.Linear(2048, 8).to('cuda')
        self.model.load_state_dict(torch.load(r"../weights/39_model_reach_0.60225.pth"))
        self.model.eval()

        self.tfm = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet 标准化
        ])

    def detect(self,img):
        res=self.model(self.tfm(img))
        