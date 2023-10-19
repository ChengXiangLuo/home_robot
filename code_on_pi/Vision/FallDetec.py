import cv2
import mediapipe as mp
import time

class FallDetection:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.prev_hip_y = None
        self.prev_time = time.time()
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5, model_complexity=0)

    def detect_fall(self,image):
            # 转换为灰度图像
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 运行姿势检测器
            results = self.pose.process(image_rgb)

            if results.pose_landmarks is not None:
                # 获取髋关节的位置
                hip = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
                # # 检查上一帧是否有髋关节位置
                if (self.prev_hip_y is not None) and (self.prev_hip_y < 1):
                    # 计算髋关节的下降速度
                    current_time = time.time()
                    time_diff = current_time - self.prev_time
                    hip_y_diff = hip.y - self.prev_hip_y
                    velocity = hip_y_diff / time_diff

                    # 如果速度超过阈值，判定为摔倒
                    if velocity > 0.9:  # 你可以根据实际情况调整阈值
                        return True
                    # 更新上一帧的信息
                    self.prev_hip_y = hip.y
                    self.prev_time = current_time
                else:
                    # 第一帧，初始化上一帧信息
                    self.prev_hip_y = hip.y
                    self.prev_time = time.time()

  
if __name__ == "__main__":
    cap = cv2.VideoCapture('E:/vscode _ws/opencv_ws/material/vedios/d66ce561.mp4')
    fall_detection = FallDetection()
    while True:
         ret, img = cap.read()
         if ret:           
            fall_detected = fall_detection.detect_fall(img)
            if fall_detected:
                print("摔倒了！")
                break
