import mss
import pytesseract
from PIL import Image
import requests
import time
import win32api, win32con

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

x_pad = 50
y_pad = 900
chat_w = 300
chat_h = 400

def screengrab():
    box = (x_pad, y_pad, x_pad+chat_w, y_pad+chat_h)
    return mss.grab(box)

def get_text(img):
    pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGR")
    text = pytesseract.image_to_string(pil, lang='rus+eng')
    return text.strip()

AI_URL = "http://localhost:1234/v1/chat/completions"

def ask_ai(prompt):
    try:
        resp = requests.post(AI_URL, json={
            "model": "llama3",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50
        }, timeout=15)
        return resp.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка: {e}"

def type_text(text):
    for char in text:
        code = ord(char)
        win32api.keybd_event(code, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)

def send():
    win32api.keybd_event(0x0D, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)

print("=" * 40)
print("ЧАТ-БОТ")
print("=" * 40)
print("1. Запусти Ollama: ollama serve")
print("2. В игре открой чат")
print("3. Напиши что-нибудь")
print("")
print("Для выхода: Ctrl+C")

last_msg = ""

while True:
    img = screengrab()
    text = get_text(img)
    
    if text and text != last_msg and len(text) > 3:
        print(f"\Новое: {text[:80]}")
        
        answer = ask_ai(text)
        print(f"AI: {answer}")
        
        type_text(answer)
        send()
        
        last_msg = text
    
    time.sleep(3)