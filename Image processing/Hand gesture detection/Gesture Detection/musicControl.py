import pyautogui

class musicControl:

    def play(self) -> None:
        pyautogui.press('playpause')
    def pause(self) -> None:
        pyautogui.press('pause')
    def next(self) -> None:
        pyautogui.press('nexttrack')
    def prev(self) -> None:
        pyautogui.press('prevtrack')
    def volup(self) -> None:
        pyautogui.press('volumeup')
    def voldown(self) -> None:
        pyautogui.press('volumedown')
