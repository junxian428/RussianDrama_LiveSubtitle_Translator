import cv2
import numpy as np
import pytesseract
from googletrans import Translator
import mss
from screeninfo import get_monitors
import tkinter as tk
from tkinter import messagebox
import time

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

translator = Translator()

def start_translation(monitor_index):
    monitors = get_monitors()
    if monitor_index >= len(monitors):
        messagebox.showerror("Error", "Selected screen not found.")
        return

    monitor = monitors[monitor_index]

    region = {
        "top": monitor.y + monitor.height - 350,
        "left": monitor.x,
        "width": monitor.width,
        "height": 200
    }

    print(f"Capturing subtitles from Screen {monitor_index + 1} in region {region}")
    messagebox.showinfo("Started", f"Capturing subtitles from Screen {monitor_index + 1}. Press 'q' to quit.")

    last_text = ""
    last_translation = ""

    with mss.mss() as sct:
        while True:
            # Fast capture
            img = np.array(sct.grab(region))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Preprocess
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

            # OCR
            config = "--psm 6"
            russian_text = pytesseract.image_to_string(thresh, lang='rus', config=config).strip()

            # Skip redundant translation
            if russian_text and russian_text != last_text:
                try:
                    last_translation = translator.translate(russian_text, src='ru', dest='en').text
                except Exception:
                    last_translation = "[Translation Error]"
                last_text = russian_text

            if not russian_text:
                last_translation = "[No text]"

            # Overlay
            cv2.putText(frame, last_translation.strip(), (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            # Display
            cv2.imshow(f"Subtitle Translation - Screen {monitor_index + 1}", frame)
            print("OCR (RU):", russian_text)
            print("Translation (EN):", last_translation)
            print("-" * 30)

            # Exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Slight delay to reduce CPU (tune as needed)
            time.sleep(0.05)

        cv2.destroyAllWindows()

# GUI
root = tk.Tk()
root.title("Subtitle Translator")
root.geometry("300x160")

tk.Label(root, text="Select screen to translate subtitles from:").pack(pady=10)

tk.Button(root, text="Translate from Screen 1", width=30, command=lambda: start_translation(0)).pack(pady=5)
tk.Button(root, text="Translate from Screen 2", width=30, command=lambda: start_translation(1)).pack(pady=5)

tk.Label(root, text="Press 'q' in video window to stop").pack(pady=10)

root.mainloop()
