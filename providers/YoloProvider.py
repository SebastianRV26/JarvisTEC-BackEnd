# pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
# pip install git+https://github.com/baxterisme/pytube
import threading

import cv2
import torch
from pytube import YouTube


class YoloProvider:
    CAPTURE_INTERVAL_MS = 500
    DETECT_MARGIN = (2 * 1000) / CAPTURE_INTERVAL_MS

    __model = None
    __detections = [{"name": "Gun", "last": -1, "total": 0}, {"name": "Fire", "last": -1, "total": 0},
                    {"name": "Rifle", "last": -1, "total": 0}]
    __thread = None

    @staticmethod
    def get_model():
        if YoloProvider.__model is None:
            YoloProvider.__model = torch.hub.load('ultralytics/yolov5', 'custom', './models/yolov5.pt')
        return YoloProvider.__model

    @staticmethod
    def download_from_youtube(url):
        save_path = "./tmp"
        yt = YouTube(url)
        video = yt.streams.get_lowest_resolution()
        video.download(save_path, "video.mp4")

    @staticmethod
    def process_frame(image, count):
        model = YoloProvider.get_model()
        results = model(image, size=412)
        res_df = results.pandas().xyxy[0]
        res_df = res_df[res_df['confidence'] > 0.3]
        for index, row in res_df.groupby(['class']).size().reset_index(name='counts').iterrows():
            if count - YoloProvider.__detections[row['class']]["last"] > YoloProvider.DETECT_MARGIN or \
                    YoloProvider.__detections[row['class']]["last"] == -1:

                YoloProvider.__detections[row['class']]["last"] = count
                YoloProvider.__detections[row['class']]["total"] = \
                    YoloProvider.__detections[row['class']]["total"] + row['counts']
            else:
                YoloProvider.__detections[row['class']]["last"] = count

    @staticmethod
    def process_video():
        YoloProvider.__detections = [{"name": "Gun", "last": -1, "total": 0}, {"name": "Fire", "last": -1, "total": 0},
                                     {"name": "Rifle", "last": -1, "total": 0}]
        video_cap = cv2.VideoCapture("./tmp/video.mp4")
        success, image = video_cap.read()
        count = 0

        while success:
            video_cap.set(cv2.CAP_PROP_POS_MSEC, (count * YoloProvider.CAPTURE_INTERVAL_MS))
            success, image = video_cap.read()
            if image is not None:
                rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                YoloProvider.process_frame(rgb_img, count)
            count = count + 1

    @staticmethod
    def run(video_url):
        YoloProvider.download_from_youtube(video_url)
        YoloProvider.process_video()

    @staticmethod
    def run_thread(video_url):
        YoloProvider.__thread = threading.Thread(target=YoloProvider.run,
                                                 args=(video_url,))
        YoloProvider.__thread.start()

    @staticmethod
    def thread_is_running():
        return YoloProvider.__thread is not None and YoloProvider.__thread.is_alive()

    @staticmethod
    def get_detections():
        results = map(lambda x: {"name": x["name"], "total": str(x["total"])}, YoloProvider.__detections)
        return list(results)
