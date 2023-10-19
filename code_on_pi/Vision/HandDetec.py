import cv2
import mediapipe as mp

class HandDetection:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        # 初始化手部检测器
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, 
                                          max_num_hands=1, model_complexity=0)

    def detect_hand(self,image):
        # 转换为 RGB 格式
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 运行手部检测器
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            # 获取第一个检测到的手的关键点坐标
            hand_landmarks = results.multi_hand_landmarks[0]

            # 获取手的中心位置
            hand_center_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * image.shape[1])
            hand_center_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * image.shape[0])

            # 在图像中绘制手的中心位置
            cv2.circle(image, (hand_center_x, hand_center_y), 10, (255, 0, 0), -1)
            # x0-600 y480-0
            return hand_center_x, hand_center_y
        else:
            return None
        
       


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    hand_detection = HandDetection()
    while True:
        ret, img=cap.read()
        if ret:    
            hand_position = hand_detection.detect_hand(img)
            if hand_position is not None:
                x, y = hand_position
                print(f"手的中心位置：({x}, {y})")
            else:
                print("没有检测到手")