import math
import time


class GestureDetection:
    def __init__(self, stability_time=0.35):
        self.stability_time = stability_time
        self.last_valid_time = 0
        self.stable_state = False

    def _distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def _finger_extended(self, tip, mcp, palm_size):
        """
        Finger is considered extended if its length
        is significant relative to palm size.
        """
        return self._distance(tip, mcp) > 0.45 * palm_size

    def is_typing_mode(self, hand_landmarks):
        """
        Typing mode:
        - Thumb extended
        - Index extended
        - Middle, Ring, Pinky NOT extended
        - Must be stable for a short duration
        """

        wrist = hand_landmarks.landmark[0]
        middle_mcp = hand_landmarks.landmark[9]

        palm_size = self._distance(wrist, middle_mcp)

        thumb = self._finger_extended(
            hand_landmarks.landmark[4],
            hand_landmarks.landmark[2],
            palm_size
        )

        index = self._finger_extended(
            hand_landmarks.landmark[8],
            hand_landmarks.landmark[5],
            palm_size
        )

        middle = self._finger_extended(
            hand_landmarks.landmark[12],
            hand_landmarks.landmark[9],
            palm_size
        )

        ring = self._finger_extended(
            hand_landmarks.landmark[16],
            hand_landmarks.landmark[13],
            palm_size
        )

        pinky = self._finger_extended(
            hand_landmarks.landmark[20],
            hand_landmarks.landmark[17],
            palm_size
        )

        current_state = (
            thumb and index and
            not middle and not ring and not pinky
        )

        current_time = time.time()

        if current_state:
            if current_time - self.last_valid_time > self.stability_time:
                self.stable_state = True
        else:
            self.last_valid_time = current_time
            self.stable_state = False

        return self.stable_state
# 
