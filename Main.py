import cv2
import numpy as np
import pytesseract
from googletrans import Translator
import pyautogui
import time

# Set path to Tesseract executable (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# For Linux/macOS, make sure tesseract is in PATH

# Initialize translator
translator = Translator()

# Define the region of the screen to capture (left, top, width, height)
region = (100, 100, 640, 200)  # Change this as needed

while True:
    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # OCR to extract Russian text
    russian_text = pytesseract.image_to_string(frame, lang='rus')

    # Translate to English
    translated = translator.translate(russian_text, src='ru', dest='en').text

    # Show the frame and translation
    cv2.imshow("Captured Region", frame)
    print("Detected (RU):", russian_text.strip())
    print("Translated (EN):", translated.strip())
    print("-" * 40)

    # Exit on 'q'
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
