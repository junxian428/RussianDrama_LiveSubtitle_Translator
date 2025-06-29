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

# Google Translator
translator = Translator()

def start_translation(monitor_index):
    monitors = get_monitors()
    if monitor_index >= len(monitors):
        messagebox.showerror("Error", "Selected screen not found.")
        return

    monitor = monitors[monitor_index]

    # ✅ Capture bottom 200px for subtitles
    region = (monitor.x, monitor.y + monitor.height - 350, monitor.width, 200)

    print(f"Starting capture on Screen {monitor_index + 1} in region: {region}")
    messagebox.showinfo("Started", f"Capturing bottom subtitle area of Screen {monitor_index + 1}. Press 'q' to quit.")

    while True:
        # Capture screen region
        screenshot = pyautogui.screenshot(region=region)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # OCR
        russian_text = pytesseract.image_to_string(frame, lang='rus')
        translation = "[No text detected]"

        if russian_text.strip():
            try:
                translation = translator.translate(russian_text, src='ru', dest='en').text
            except Exception as e:
                translation = "[Translation Error]"

        # Overlay translated text on frame
        cv2.putText(frame, translation.strip(), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        # Show frame
        cv2.imshow(f"Subtitle Translation - Screen {monitor_index + 1}", frame)
        print("Detected (RU):", russian_text.strip())
        print("Translated (EN):", translation.strip())
        print("-" * 40)

        # Exit on 'q'
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
