import pyautogui
import time

time.sleep(3)

for i in range(10):
    pyautogui.moveTo(x=610, y=980, duration=0.4)
    pyautogui.click()
    pyautogui.moveTo(x=720, y=730, duration=0.4)
    pyautogui.click()
    pyautogui.moveTo(x=1855, y=980, duration=0.4)
    pyautogui.click()
