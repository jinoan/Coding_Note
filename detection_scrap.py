import cv2
import os
import shutil

import sys
sys.path.append("/home/noah/Desktop/darknet")
import darknet

# darknet
DARKNET = '../../darknet'
WEIGHT_FILE = './darknet_files/yolov4.weights'
CONFIG_FILE = './darknet_files/yolov4.cfg'
DATA_FILE = './darknet_files/etri.data'
THRESHOLD = .7

# custom class_colors
CLASS_COLORS = {'Red_fire_extinguisher': (67, 138, 237),
                'Silver_fire_extinguisher': (36, 159, 27),
                'exit_sign': (147, 158, 81),
                'fire_detector': (110, 45, 14),
                'fireplug': (61, 75, 139)}

IMG_SHAPE = (640, 480)

class DarknetParameters:
    def __init__(self, darknet, config_file, data_file, weight_file, threshold=0.7, **kwargs):
        self.network, self.class_names, self.class_colors = darknet.load_network(os.path.abspath(config_file), os.path.abspath(data_file), os.path.abspath(weight_file), batch_size=1)
        self.width = darknet.network_width(self.network)
        self.height = darknet.network_height(self.network)
        self.darknet_image = darknet.make_image(self.width, self.height, 3)
        self.threshold = threshold
        self.__dict__.update(kwargs)


class VideoScrap:
    def __init__(self, video_path, scrap_name, tmp_path, darknet_parameters):
        self.caps = [cv2.VideoCapture(os.path.join(video_path, f)) for f in sorted(os.listdir(video_path))]
        self.scrap_name = scrap_name
        self.tmp_path = tmp_path
        self.dn = darknet_parameters

    def ready(self):
        count = 0
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        else:
            shutil.rmtree(self.tmp_path)
            os.mkdir(self.tmp_path)

        print("preparing frames ...")
        for cap in self.caps:
            while True:
                ret, img = cap.read()
                if not ret: break
                img = cv2.resize(img, IMG_SHAPE)
                frame = darknet.draw_boxes(self.reshape_detection(self.detect(img)), img, self.dn.class_colors)
                cv2.imwrite(os.path.join(self.tmp_path, f"{str(count).zfill(8)}.jpg"), frame)
                count += 1
        print("ready")
        return count

    def detect(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(img, (self.dn.width, self.dn.height))
        darknet.copy_image_from_bytes(self.dn.darknet_image, frame.tobytes())
        detections = darknet.detect_image(self.dn.network, self.dn.class_names, self.dn.darknet_image, thresh=self.dn.threshold)
        return detections

    def reshape_detection(self, dtt):
        def reshape(obj):
            x = obj[2][0] * IMG_SHAPE[0] / self.dn.width
            y = obj[2][1] * IMG_SHAPE[1] / self.dn.height
            w = obj[2][2] * IMG_SHAPE[0] / self.dn.width
            h = obj[2][3] * IMG_SHAPE[1] / self.dn.height
            return (obj[0], obj[1], (x, y, w, h))
        return list(map(reshape, dtt))

    def run(self):
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fps = self.caps[0].get(cv2.CAP_PROP_FPS)
        delay = round(30/fps)
        out = cv2.VideoWriter(self.scrap_name, fourcc, fps, IMG_SHAPE)

        for img_file in sorted(os.listdir(self.tmp_path)):
            img = cv2.imread(os.path.join(self.tmp_path, img_file))
            frame = cv2.resize(img, IMG_SHAPE)
            # frame = darknet.draw_boxes(self.reshape_detection(self.detect(img)), img, self.dn.class_colors)
            cv2.imshow("frame", frame)
            out.write(frame)
            if cv2.waitKey(10) == 27:
                break
    
        cv2.destroyAllWindows()
        out.release()


if __name__ == "__main__":
    # main('test_videos/1.mp4', 'test_videos/1_.mp4', './tmp/')
    darknet_parameters = DarknetParameters(darknet, CONFIG_FILE, DATA_FILE, WEIGHT_FILE, class_colors=CLASS_COLORS)
    vs = VideoScrap('test_videos', 'scrap.mp4', 'tmp', darknet_parameters)
    # vs.ready()
    vs.run()