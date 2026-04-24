import pyautogui
import time
import threading

pyautogui.FAILSAFE = True

class ImageClicker:
    def __init__(self):
        self.running = False
        self.paused = False
        self.click_count = 0
        self.confidence = 0.8
        self.delay = 0.5
        
        self.images = {
            "hend": "image/hend.png",
            "heal": "image/heal.png"
        }
    
    def find_click(self, image_path):
        try:
            pos = pyautogui.locateCenterOnScreen(image_path, confidence=self.confidence)
            if pos:
                pyautogui.click(pos)
                self.click_count += 1
                print(f"Клик #{self.click_count} по {image_path}")
                return True
        except Exception as e:
            pass
        return False
    
    def click_loop(self):
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            
            found = False
            for name, img_path in self.images.items():
                if self.find_click(img_path):
                    found = True
                    break
            
            time.sleep(self.delay)
    
    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            threading.Thread(target=self.click_loop, daemon=True).start()
            print("Старт!")
    
    def stop(self):
        self.running = False
        print("Стоп!")
    
    def pause(self):
        self.paused = not self.paused
        if self.paused:
            print("Пауза")
        else:
            print("Продолжаем")

def main():
    bot = ImageClicker()
    
    print("Бот кликер по картинкам")
    print("========================")
    print("1. Старт")
    print("2. Стоп")
    print("3. Пауза")
    print("4. Выход")
    
    while True:
        cmd = input("\n> ").strip()
        
        if cmd == "1":
            bot.start()
        elif cmd == "2":
            bot.stop()
        elif cmd == "3":
            bot.pause()
        elif cmd == "4":
            bot.stop()
            break

if __name__ == "__main__":
    main()