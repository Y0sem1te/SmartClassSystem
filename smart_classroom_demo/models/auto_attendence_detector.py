import numpy as np
from PIL import Image
from face_recog.models.face_boxes_location import FaceBoxesLocation
from face_recog.models import face_recog
import os
import cv2
class AttendenceDetector:
    def __init__(self):
        self.face_detection = FaceBoxesLocation()
        self.face_bank_dir   = "resource/face_bank"

        # 已加载人脸库
        self.known_ids       = []
        self.known_names     = []
        self.known_encodings = np.empty((0, 128), dtype=np.float32)
        self.face_imgs       = []
        self._load_face_bank()

    def _load_face_bank(self):
        """扫描 face_bank_dir，读取所有 id/name/encoding"""
        encs, ids, names = [], [], []
        for sid in os.listdir(self.face_bank_dir):
            folder = os.path.join(self.face_bank_dir, sid)
            enc_file = os.path.join(folder, "encoding.txt")
            if os.path.isdir(folder) and os.path.exists(enc_file):
                arr = np.array(eval(open(enc_file).read()), dtype=np.float32)
                encs.append(arr); ids.append(sid)
                # 取文件夹中第一个 jpg 作为姓名
                for f in os.listdir(folder):
                    if f.endswith(".jpg") and not f.startswith(sid):
                        img = cv2.imread(os.path.join(folder, f), cv2.IMREAD_COLOR_RGB)
                        self.face_imgs.append(img)
                        names.append(os.path.splitext(f)[0])
                        break
        if encs:
            self.known_encodings = np.vstack(encs)
        self.known_ids   = ids
        self.known_names = names


    def register(self,img,id,name):
        # —— 改为：返回（是否成功, 提示信息）
        locs = self.face_detection.face_location(img)[0]
        if not len(locs):
            return False, "未检测到人脸，请重试。"
        x1,y1,x2,y2 = locs
        enc = face_recog.face_encodings(img, [locs])[0]
        folder = os.path.join(self.face_bank_dir, str(id))
        if os.path.exists(folder):
            return False, "学号已存在，无法重复注册。"
        os.makedirs(folder)
        # 写入特征向量
        with open(os.path.join(folder,"encoding.txt"),"w") as f:
            f.write(str(enc.tolist()))
        # 裁剪并保存头像
        face_img = img[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite(os.path.join(folder, f"{name}.jpg"), face_img)
        # 重新加载人脸库
        self._load_face_bank()
        return True, "注册成功。"


    def sign_in(self, img, threshold=0.6):
        """检测所有人脸，返回所有匹配成功的学号列表"""
        locs = self.face_detection.face_location(img)
        if not len(locs):
            return []
        encs = face_recog.face_encodings(img, locs)
        recognized = []
        for e in encs:
            dists = face_recog.face_distance(self.known_encodings, e)
            if len(dists)>0:
                idx = np.argmin(dists)
                if dists[idx] < threshold:
                    recognized.append(self.known_ids[idx])
        return recognized

        