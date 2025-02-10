import cv2
import mediapipe as mp
import math

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.lmList = []  # Initialize the landmark list here
        self.bbox = []  # Initialize the bounding box here

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        self.bbox = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            h, w, c = img.shape
            for id, lm in enumerate(myHand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if id == 0:
                    self.bbox = [cx, cy, cx, cy]
                else:
                    self.bbox[0] = min(self.bbox[0], cx)
                    self.bbox[1] = min(self.bbox[1], cy)
                    self.bbox[2] = max(self.bbox[2], cx)
                    self.bbox[3] = max(self.bbox[3], cy)
            if draw:
                cv2.rectangle(img, (self.bbox[0] - 20, self.bbox[1] - 20), (self.bbox[2] + 20, self.bbox[3] + 20), (0, 255, 0), 2)
        return self.lmList, self.bbox

    def findDistance(self, p1, p2, img, draw=True):
        if self.lmList:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, img, [x1, y1, x2, y2, cx, cy]
        return 0, img, [0, 0, 0, 0, 0, 0]

    def fingersUp(self):
        fingers = []
        if self.lmList:
            # Thumb
            if self.lmList[4][1] > self.lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[id * 4][2] < self.lmList[id * 4 - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
