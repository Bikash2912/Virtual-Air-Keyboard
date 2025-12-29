# virtual_keyboard.py
import cv2


class Key:
    def __init__(self, x, y, w, h, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label

    def is_hovered(self, px, py):
        return self.x < px < self.x + self.w and self.y < py < self.y + self.h

frame_width = 1600  # same as camera width
keyboard_width = (10 * 60) + (9 * 10)  # keys + gaps

start_x = (frame_width - keyboard_width) // 2
start_y = 120

class VirtualKeyboard:
    def __init__(self, start_x=200, start_y=120, key_w=60, key_h=60, gap=10):
        self.keys = []
        self._create_keys(start_x, start_y, key_w, key_h, gap)

    def _create_keys(self, x, y, w, h, gap):
        rows = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        # Row 1
        for i, key in enumerate(rows[0]):
            self.keys.append(Key(x + i*(w+gap), y, w, h, key))

        # Row 2 (slightly indented)
        y2 = y + h + gap
        x2 = x + w//2
        for i, key in enumerate(rows[1]):
            self.keys.append(Key(x2 + i*(w+gap), y2, w, h, key))

        # Row 3 (more indented)
        y3 = y2 + h + gap
        x3 = x + w
        for i, key in enumerate(rows[2]):
            self.keys.append(Key(x3 + i*(w+gap), y3, w, h, key))

        # SPACE bar (wide)
        self.keys.append(
            Key(x3 + 2*(w+gap), y3 + h + gap, w*4, h, "SPACE")
        )

        # BACKSPACE
        self.keys.append(
            Key(x3 + 2*(w+gap) + w*4 + gap, y3 + h + gap, w*2, h, "Back")
        )


    def draw(self, frame, hover_key=None):
        for key in self.keys:
            color = (0, 255, 0) if key == hover_key else (200, 200, 200)

            cv2.rectangle(
                frame,
                (key.x, key.y),
                (key.x + key.w, key.y + key.h),
                color,
                -1
            )

            cv2.rectangle(
                frame,
                (key.x, key.y),
                (key.x + key.w, key.y + key.h),
                (0, 0, 0),
                2
            )
            label = key.label
            font_scale = 0.8 if len(label) > 1 else 1
            text_x = key.x + (key.w // 2) - 20
            text_y = key.y + (key.h // 2) + 10

            cv2.putText(
                frame,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (0, 0, 0),
                2
            )

        return frame

    def get_hovered_key(self, px, py):
        for key in self.keys:
            if key.is_hovered(px, py):
                return key
        return None
