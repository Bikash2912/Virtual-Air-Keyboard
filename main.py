import cv2
import time

from camera import Camera
from hand_track import HandTracker
from finger_track import FingerTracker
from virt_key import VirtualKeyboard
from press_det import PressDetector
from key_controller import KeyboardController
from gest_det import GestureDetection


def main():
    camera = Camera(width=1600, height=900)   # Bigger window
    hand_tracker = HandTracker()
    finger_tracker = FingerTracker(smoothing=0.75)

    KEY_W, KEY_H, GAP = 60, 60, 10
    FRAME_WIDTH = 1600
    KEYBOARD_WIDTH = (10 * KEY_W) + (9 * GAP)
    START_X = (FRAME_WIDTH - KEYBOARD_WIDTH) // 2
    START_Y = 120

    keyboard = VirtualKeyboard(start_x=START_X, start_y=START_Y)
    press_detector = PressDetector()
    kb_controller = KeyboardController()
    gesture = GestureDetection()

    typed_text = ""
    last_type_time = 0
    TYPE_COOLDOWN = 0.35

    while True:
        start_time = time.time()

        frame = camera.get_frame()
        if frame is None:
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        results = hand_tracker.process(frame)
        frame = hand_tracker.draw(frame, results)

        hovered_key = None
        pressed_key = None
        typing_mode = False

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            ix, iy = finger_tracker.get_fingertip_position(
                hand_landmarks, frame.shape
            )
            cv2.circle(frame, (ix, iy), 10, (0, 255, 255), -1)

            # Thumb 
            h, w, _ = frame.shape
            thumb_tip = hand_landmarks.landmark[4]
            tx = int(thumb_tip.x * w)
            ty = int(thumb_tip.y * h)
            cv2.circle(frame, (tx, ty), 10, (255, 0, 255), -1)

            # Hover detection
            hovered_key = keyboard.get_hovered_key(ix, iy)

            # Typing mode detection
            typing_mode = gesture.is_typing_mode(hand_landmarks)

            # Allow press only in typing mode and when hovering a key
            if typing_mode and hovered_key:
                pressed_key = press_detector.detect_press(
                    hand_landmarks, hovered_key
                )

        # Draw keyboard (TOP)
        frame = keyboard.draw(frame, hovered_key)

        current_time = time.time()
        if pressed_key and (current_time - last_type_time > TYPE_COOLDOWN):
            last_type_time = current_time
            label = pressed_key.label

            if label == "SPACE":
                kb_controller.space()
                typed_text += " "
            elif label == "Back":
                kb_controller.backspace()
                typed_text = typed_text[:-1]
            else:
                kb_controller.type_character(label.lower())
                typed_text += label.lower()

        mode_text = "TYPING MODE" if typing_mode else "MOVE MODE"
        mode_color = (0, 255, 0) if typing_mode else (0, 0, 255)

        cv2.rectangle(frame, (20, 10), (300, 60), (0, 0, 0), -1)
        cv2.putText(
            frame,
            mode_text,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            mode_color,
            3
        )

        text_y = START_Y + (4 * KEY_H) + (4 * GAP) + 120

        cv2.rectangle(
            frame,
            (50, text_y - 50),
            (frame.shape[1] - 50, text_y + 20),
            (30, 30, 30),
            -1
        )

        cv2.putText(
            frame,
            typed_text[-60:],
            (60, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            2
        )

        elapsed = time.time() - start_time
        time.sleep(max(1/60 - elapsed, 0))

        cv2.imshow("Virtual Air Keyboard", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    hand_tracker.release()
    camera.release()


if __name__ == "__main__":
    main()

