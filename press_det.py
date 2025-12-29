# press_detector.py
import time
import math


class PressDetector:
    def __init__(self, pinch_threshold=0.06, debounce_time=0.35):
        self.pinch_threshold = pinch_threshold
        self.debounce_time = debounce_time
        self.last_press_time = 0
        self.pinch_active = False

    def is_pinch(self, hand_landmarks):
        wrist = hand_landmarks.landmark[0]
        middle_mcp = hand_landmarks.landmark[9]
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]

        palm_size = math.sqrt(
            (wrist.x - middle_mcp.x) ** 2 +
            (wrist.y - middle_mcp.y) ** 2
        )

        distance = math.sqrt(
            (thumb.x - index.x) ** 2 +
            (thumb.y - index.y) ** 2
        )

        return (distance / palm_size) < 0.4

    def detect_press(self, hand_landmarks, hovered_key):
        """
        Returns the pressed key ONCE per pinch.
        """
        if hovered_key is None:
            self.pinch_active = False
            return None

        pinch = self.is_pinch(hand_landmarks)
        current_time = time.time()

        if pinch and not self.pinch_active:
            if current_time - self.last_press_time > self.debounce_time:
                self.pinch_active = True
                self.last_press_time = current_time
                return hovered_key

        if not pinch:
            self.pinch_active = False

        return None
