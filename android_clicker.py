# Простой способ запустить на Android:

## Вариант 1: Pydroid (рекомендую)
1. Скачай **Pydroid 3** с Play Market
2. Внутри нажми 📁 и открой этот файл
3. Нажми зеленую кнопку запуска

## Вариант 2: Терминал
1. Скачай **Termux** с Play Market
2. Введи:
```
pip install pyautogui pillow
```

## Код для Android:
"""

import os
import time
from pathlib import Path

# Для Android используй pydroid или termux
# Этот кодработает на Windows/LDPlayer:

def main():
    print("Image Clicker")
    print("=" * 30)
    print("1. Старт")
    print("2. Стоп")
    print("3. Пауза")
    print("4. Выход")
    
    running = False
    
    while True:
        cmd = input("\n> ").strip()
        
        if cmd == "1":
            running = True
            print("✓ Старт!")
        elif cmd == "2":
            running = False
            print("✓ Стоп")
        elif cmd == "3":
            print("✓ Пауза")
        elif cmd == "4":
            break
        
        if running:
            print("Ищу картинку...")
            # Здесь будет поиск

if __name__ == "__main__":
    main()