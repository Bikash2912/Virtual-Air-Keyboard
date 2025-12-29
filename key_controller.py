import pyautogui

pyautogui.FAILSAFE = True


class KeyboardController:
    def __init__(self):
        pass

    def type_character(self, char):
        """
        Types a single character using the OS keyboard.
        """
        pyautogui.write(char)

    def backspace(self):
        pyautogui.press("backspace")

    def space(self):
        pyautogui.press("space")

    def enter(self):
        pyautogui.press("enter")

