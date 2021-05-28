import time
import mss
import cv2
import numpy as np
import pyautogui

import pytesseract
from fuzzywuzzy import fuzz

from utils import queryMousePosition
import rods

# 1024x768 windowed on 1920x1080 monitor
# mon = {"top": 156, "left": 448, "width": 1024, "height": 768}


class FishingBot:
    title = "Fishing Bot"
    sct = None
    config = None
    rod = "Wood Fishing Pole"

    ocr = {
        "enabled": True,
        "exclude": False,
        "list": []
    }

    active = False
    last_catch_time = 0
    last_sonar_time = 0

    def __init__(self, config):
        self.config = config
        self.sct = mss.mss()

    def lmb_click(self):
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()

    def start(self):
        print(f"Starting bot after {self.config.bot.start_after} seconds.")
        print(f"Selected rod: {self.rod}")
        print(f"Please adjust your rod!")

        if not self.ocr["enabled"]:
            time.sleep(self.config.bot.start_after)
            self.lmb_click()
            print("Rod dropped!")
            self.last_catch_time = time.time()

        else:
            time.sleep(self.config.bot.start_after / 2)

        self.active = True
        self.wait()

    def stop(self):
        self.active = False

    def wait(self):
        if self.ocr["enabled"]:
            # OCR filtering
            while self.active:
                # minimum catch interval
                if time.time() - self.last_catch_time < self.config.bot.last_catch_interval:
                    continue

                # create the box shot of sonar label
                cur = queryMousePosition()
                mon = {
                    "left": cur['x'] - 200,
                    "top": cur['y'] - 75,
                    "width": 400,
                    "height": 50
                }
                img = np.array(self.sct.grab(mon))

                self.show(self.title, img)

                # create RGB for tesseract
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # read psm 6 & 7
                psm6 = pytesseract.image_to_string(
                    rgb, lang='eng', config='--psm 6')
                psm7 = pytesseract.image_to_string(
                    rgb, lang='eng', config='--psm 7')

                # catch only crates
                if ((fuzz.ratio(psm6.lower(), "crate") > 50 or fuzz.ratio(psm7.lower(), "crate") > 50)
                        or ("crate" in psm6.lower() or "crate" in psm7.lower())):
                    print("This is a crate!")
                    self.catch(True)

                else:
                    print("Nope...")

        else:
            # catch everything
            while self.active:
                # minimum catch interval
                if time.time() - self.last_catch_time < self.config.bot.last_catch_interval:
                    continue

                # create the box shot of cursor
                cur = queryMousePosition()
                mon = {
                    "left": cur['x'] - int(self.config.bot.box_height / 2),
                    "top": cur['y'] - int(self.config.bot.box_width / 2),
                    "width": self.config.bot.box_width,
                    "height": self.config.bot.box_height
                }
                img = np.asarray(self.sct.grab(mon))

                self.show(self.title, img)

                # create hsv
                hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                # get a mask by rod
                mask = rods.wood_fishing_pole.getMask(hsvFrame, np, cv2)

                # check for the color
                has_fish = np.sum(mask)
                if has_fish:
                    pass
                else:
                    self.catch()

    def catch(self, asap=False):
        print("Catch!")

        if not asap:
            time.sleep(0.3)

        self.lmb_click()

        time.sleep(1.0)
        print("New rod dropped!")
        self.lmb_click()

        # reset last catch time
        self.last_catch_time = time.time()

    def show(self, title, img):
        cv2.imshow(title, img)

        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            quit()
