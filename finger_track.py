# finger_tracker.py
class FingerTracker:
    def __init__(self, smoothing=0.7):
        self.smoothing = smoothing
        self.prev_x = None
        self.prev_y = None

    def get_fingertip_position(self, hand_landmarks, frame_shape):
        """
        Returns smoothed (x, y) fingertip position in pixel coordinates.
        """
        h, w, _ = frame_shape

        index_tip = hand_landmarks.landmark[8]
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)

        if self.prev_x is None:
            self.prev_x, self.prev_y = x, y
            return x, y

        # Exponential Moving Average for smoothing
        smooth_x = int(self.prev_x * self.smoothing + x * (1 - self.smoothing))
        smooth_y = int(self.prev_y * self.smoothing + y * (1 - self.smoothing))

        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
