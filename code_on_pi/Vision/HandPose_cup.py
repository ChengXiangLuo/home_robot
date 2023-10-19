import mediapipe as mp
import cv2

mpHands = mp.solutions.hands

class handPose(mpHands.Hands):
    def pose(self,img): 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.process(imgRGB)    
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # 获取手指关节的坐标
                thumb_tip = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
                index_finger_tip = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_mcp = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
                index_finger_pip = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP]
                middle_finger_tip = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_finger_mcp = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_MCP]
                ring_finger_tip =  handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP]
                ring_finger_mcp =  handLms.landmark[mpHands.HandLandmark.RING_FINGER_MCP]
                pinky_tip =  handLms.landmark[mpHands.HandLandmark.PINKY_TIP]
                pinky_mcp =  handLms.landmark[mpHands.HandLandmark.PINKY_MCP]
                
                if (thumb_tip.x > index_finger_mcp.x and
                    index_finger_tip.y < index_finger_mcp.y and 
                    middle_finger_tip.y < middle_finger_mcp.y and
                    ring_finger_tip.y > ring_finger_mcp.y and
                    pinky_tip.y > pinky_mcp.y):
                    gesture = "Scissors"
                elif (thumb_tip.x > index_finger_pip.x and
                    index_finger_tip.y > index_finger_mcp.y and 
                    middle_finger_tip.y > middle_finger_mcp.y and
                    ring_finger_tip.y > ring_finger_mcp.y and
                    pinky_tip.y > pinky_mcp.y):
                    gesture = "Fist"
                elif (thumb_tip.x < index_finger_mcp.x and
                    index_finger_tip.y < index_finger_mcp.y and 
                    middle_finger_tip.y < middle_finger_mcp.y and
                    ring_finger_tip.y < ring_finger_mcp.y and
                    pinky_tip.y < pinky_mcp.y):
                    gesture = "Cloth"
                else:   
                    gesture = "Other"
            
            return gesture


if __name__== "__main__":
    cap = cv2.VideoCapture(0)
    handpose = handPose(max_num_hands=1,model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.3)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img,1)
        if ret:
            gesture = handpose.pose(img=img)
            cv2.putText(img, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Hand Gesture Recognition', img)

        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()