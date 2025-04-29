from ultralytics import YOLO
import supervision as sv

class BehaviorDectector:
    def __init__(self, img, pad_ratio=0.25, pad_pixels=10):
        self.img = img
        self.model = YOLO("../weights/class_behavior.pt").to('cuda')
        self.pad_ratio = pad_ratio
        self.pad_pixels = pad_pixels
    def detect(self):
        res=self.model(self.img)[0]
        img_cpy = self.img.copy()
        detections = sv.Detections.from_ultralytics(res)
        h_img, w_img = self.img.shape[:2]
        crops = {label: [] for label in set(detections['class_name'])}
        for (x1,y1,x2,y2), cls in zip(detections.xyxy, detections['class_name']):
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            x1_p = x1 - self.pad_pixels
            y1_p = y1 - self.pad_pixels
            x2_p = x2 + self.pad_pixels
            y2_p = y2 + self.pad_pixels

            w_box = x2 - x1
            h_box = y2 - y1
            x1_p = min(x1_p, x1 - int(w_box * self.pad_ratio))
            y1_p = min(y1_p, y1 - int(h_box * self.pad_ratio))
            x2_p = max(x2_p, x2 + int(w_box * self.pad_ratio))
            y2_p = max(y2_p, y2 + int(h_box * self.pad_ratio))
            x1_p = max(0, x1_p)
            y1_p = max(0, y1_p)
            x2_p = min(w_img, x2_p)
            y2_p = min(h_img, y2_p)

            crop = self.img[int(y1_p):int(y2_p), int(x1_p):int(x2_p)]
            crops[cls].append(crop)
        return img_cpy, crops