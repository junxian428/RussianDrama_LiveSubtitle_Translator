import mss
import cv2
import numpy as np
import pytesseract
from googletrans import Translator
import cv2
import numpy as np
import pytesseract
from googletrans import Translator
import pyautogui
from screeninfo import get_monitors
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pytesseract
from googletrans import Translator
import pyautogui
from screeninfo import get_monitors
import tkinter as tk
from tkinter import messagebox

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

translator = Translator()

def start_translation(monitor_index):
    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor_index + 1 >= len(monitors):
            print("Error", "Selected screen not found.")
            return

        mon = monitors[monitor_index + 1]  # mss uses 1-based indexing
        region = {
            "top": mon["top"] + mon["height"] - 350,
            "left": mon["left"],
            "width": mon["width"],
            "height": 200
        }

        print(f"Capturing from monitor {monitor_index + 1}: {region}")
        print("Started", f"Capturing subtitles from monitor {monitor_index + 1}")

        while True:
            img = np.array(sct.grab(region))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # OCR preprocessing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

            config = "--psm 6"  # Assume a uniform block of text
            russian_text = pytesseract.image_to_string(thresh, lang='rus', config=config)

            translation = "[No text]"
            if russian_text.strip():
                try:
                    translation = translator.translate(russian_text.strip(), src='ru', dest='en').text
                except:
                    translation = "[Translation Error]"

            # Overlay translated text
            cv2.putText(frame, translation.strip(), (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow(f"Subtitle Translation - Monitor {monitor_index + 1}", frame)
            print("Detected:", russian_text.strip())
            print("Translated:", translation.strip())
            print("-" * 30)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


# ---------------------------
# GUI
# ---------------------------
root = tk.Tk()
root.title("Subtitle Translator")
root.geometry("300x160")

tk.Label(root, text="Select screen to translate subtitles from:").pack(pady=10)

tk.Button(root, text="Translate from Screen 1", width=30, command=lambda: start_translation(0)).pack(pady=5)
tk.Button(root, text="Translate from Screen 2", width=30, command=lambda: start_translation(1)).pack(pady=5)

tk.Label(root, text="Press 'q' in video window to stop").pack(pady=10)

root.mainloop()

