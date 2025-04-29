import copy
import time
from abc import abstractmethod
from queue import Empty

import cv2
import numpy as np
import torch
from PIL import ImageFont, Image, ImageDraw
from PyQt5.QtGui import QPixmap, QImage

from models.concentration_evaluator import ConcentrationEvaluation, ConcentrationEvaluator
from pipeline_module.core.base_module import BaseModule, TASK_DATA_OK, DictData
from utils.vis import draw_keypoints136

class DataDealerModule(BaseModule):
    def __init__(self, push_frame_func, interval=0.06, skippable=False):
        super(DataDealerModule, self).__init__(skippable=skippable)
        self.last_time = time.time()
        self.push_frame_func = push_frame_func
        self.last_data = None
        self.interval = interval
        self.size_waiting = True

        #
        self.queue_threshold = 10

    @abstractmethod
    def deal_skipped_data(self, data: DictData, last_data: DictData) -> DictData:
        pass

    @abstractmethod
    def draw_frame(self, data, fps):
        pass

    def process_data(self, data):
        if hasattr(data, 'skipped') and self.last_data is not None:
            data = self.deal_skipped_data(data, copy.copy(self.last_data))
        else:
            self.last_data = data
        current_time = time.time()
        interval = (current_time - self.last_time)
        fps = 1 / interval
        data.fps = fps
        self.draw_frame(data, fps=fps)
        data.interval = interval
        self.last_time = current_time  # 更新时间
        self.push_frame_func(data)
        if hasattr(data, 'source_fps'):
            time.sleep(1 / data.source_fps * (1 + self.self_balance_factor()))
        else:
            time.sleep(self.interval)
        return TASK_DATA_OK

    def self_balance_factor(self):
        factor = max(-0.999, (self.queue.qsize() / 20 - 0.5) / -0.5)
        # print(factor)
        return factor

    def product_task_data(self):
        # print(self.queue.qsize(), self.size_waiting)
        if self.queue.qsize() == 0:
            self.size_waiting = True
        if self.queue.qsize() > self.queue_threshold or not self.size_waiting:
            self.size_waiting = False
            try:
                task_data = self.queue.get(block=True, timeout=1)
                return task_data
            except Empty:
                return self.ignore_task_data
        else:
            time.sleep(1)
            return self.ignore_task_data

    def put_task_data(self, task_data):
        self.queue.put(task_data)

    def open(self):
        super(DataDealerModule, self).open()
        pass

class SentimentEmojiModule(DataDealerModule):

    def __init__(self, push_frame_func, known_names, interval=0.06, skippable=False):
        super(SentimentEmojiModule, self).__init__(push_frame_func, interval, skippable)
        self.known_names = known_names

    def deal_skipped_data(self, data: DictData, last_data: DictData) -> DictData:
        frame = data.frame
        data = last_data
        data.frame = frame
        data.face_locations = np.copy(data.face_locations)
        # 添加抖动
        data.face_locations[:, :4] += np.random.rand(*data.face_locations[:, :4].shape) * 3
        return data

    def draw_frame(self, data, fps):
        def opt_draw_frame(show_raw, show_locations, threshold, data=data, self=self):
            frame = data.frame.copy()
            face_locations = data.face_locations
            raw_face_labels = data.raw_face_labels
            raw_face_probs = data.raw_face_probs
            face_labels = data.face_labels
            face_probs = data.face_probs
            sentiments = data.sentiments
            #
            frame_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pil)  # 创建画板
            if show_locations:
                for (x1, y1, x2, y2), \
                    face_label, face_prob, \
                    raw_face_label, raw_face_prob,sentiment in zip(face_locations,
                                                         face_labels, face_probs,
                                                         raw_face_labels,
                                                         raw_face_probs,
                                                         sentiments):
                    color = (0, 0, 255) if face_prob > threshold else (255, 0, 0)
                    # 把人脸框出来标号
                    draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)

                    fontText = ImageFont.truetype("resource/font/NotoSansCJKkr-Black.otf",
                                                  int(40 * (min(x2 - x1, y2 - y1)) / 200),
                                                  encoding="utf-8")
                    # 显示处理冲突后的检测结果
                    if face_prob < threshold:
                        label_name = f'{self.known_names[face_label]}:{sentiment}'
                    else:
                        label_name = '请正视摄像头'
                    # f_w, f_h = fontText.getsize(label_name)
                    le,to, ri,bo = fontText.getbbox(label_name)
                    f_w = ri - le
                    f_h = bo - to
                    draw.rectangle([(x1, y1 - f_h), (x2, y1)], color)
                    draw.text((x1, y1 - f_h), label_name, (255, 255, 255), font=fontText)

                    # 显示原始检测结果
                    if show_raw:
                        raw_label_name = f'{self.known_names[raw_face_label]}:{(1 - raw_face_prob) * 100:8.2f}%'
                        # f_w_2, f_h_2 = fontText.getsize(raw_label_name)
                        le,to, ri,bo = fontText.getbbox(raw_label_name)
                        f_w_2 = ri - le
                        f_h_2 = bo - to
                        draw.rectangle([(x1, y1 - f_h_2 - f_h), (x2, y1 - f_h)], (0, 200, 200))
                        draw.text((x1, y1 - f_h_2 - f_h), raw_label_name, (255, 255, 255), font=fontText)
            return np.array(frame_pil)

        data.get_draw_frame = lambda show_raw=True, show_locations=True, threshold=0.25: opt_draw_frame(show_raw,
                                                                                                        show_locations,
                                                                                                        threshold)
