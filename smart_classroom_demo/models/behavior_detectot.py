from ultralytics import YOLO
import supervision as sv

class BehaviorDectector:
    def __init__(self,pad_ratio=0.25, pad_pixels=10):
        self.model = YOLO("../weights/class_behavior.pt").to('cuda')
        self.pad_ratio = pad_ratio
        self.pad_pixels = pad_pixels
    # def detect(self,img):
    #     res=self.model(img)[0]
    #     img_cpy = img.copy()
    #     detections = sv.Detections.from_ultralytics(res)
    #     h_img, w_img = img.shape[:2]
    #     crops = {label: [] for label in set(detections['class_name'])}
    #     for (x1,y1,x2,y2), cls in zip(detections.xyxy, detections['class_name']):
    #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
    #         x1_p = x1 - self.pad_pixels
    #         y1_p = y1 - self.pad_pixels
    #         x2_p = x2 + self.pad_pixels
    #         y2_p = y2 + self.pad_pixels

    #         w_box = x2 - x1
    #         h_box = y2 - y1
    #         x1_p = min(x1_p, x1 - int(w_box * self.pad_ratio))
    #         y1_p = min(y1_p, y1 - int(h_box * self.pad_ratio))
    #         x2_p = max(x2_p, x2 + int(w_box * self.pad_ratio))
    #         y2_p = max(y2_p, y2 + int(h_box * self.pad_ratio))
    #         x1_p = max(0, x1_p)
    #         y1_p = max(0, y1_p)
    #         x2_p = min(w_img, x2_p)
    #         y2_p = min(h_img, y2_p)

    #         crop = img[int(y1_p):int(y2_p), int(x1_p):int(x2_p)]
    #         crops[cls].append(crop)
    #     return img_cpy, crops
    def detect(self, img):
        """
        返回：原图副本、所有裁剪图像列表、对应的边界框列表、类别列表
        """
        res = self.model(img)[0]
        detections = sv.Detections.from_ultralytics(res)
        h_img, w_img = img.shape[:2]
        crops = []
        bboxes = []
        labels = []
        for (x1, y1, x2, y2), cls in zip(detections.xyxy, detections['class_name']):
            # 转为 int 并计算 padding
            w_box, h_box = x2 - x1, y2 - y1
            # 绝对与相对 padding
            x1_p = max(0, x1 - self.pad_pixels - int(w_box * self.pad_ratio))
            y1_p = max(0, y1 - self.pad_pixels - int(h_box * self.pad_ratio))
            x2_p = min(w_img, x2 + self.pad_pixels + int(w_box * self.pad_ratio))
            y2_p = min(h_img, y2 + self.pad_pixels + int(h_box * self.pad_ratio))

            # crop = img[y1_p:y2_p, x1_p:x2_p]
            # 强制把边界坐标转换成 int，避免 slice indices must be integers 错误
            crop = img[int(y1_p):int(y2_p), int(x1_p):int(x2_p)]

            crops.append(crop)
            # bboxes.append((x1_p, y1_p, x2_p, y2_p))
            bboxes.append((int(x1_p), int(y1_p), int(x2_p), int(y2_p)))
            labels.append(cls)
  
        return img.copy(), crops, bboxes, labels