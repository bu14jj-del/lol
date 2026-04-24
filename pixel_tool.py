import sys
import mss
import pygetwindow as gw
import ctypes
from ctypes import wintypes, windll
import time

def get_game_window():
    windows = gw.getWindowsWithTitle("TilesSurvive")
    if not windows:
        windows = gw.getWindowsWithTitle("Tiles Survive")
    if not windows:
        windows = gw.getWindowsWithTitle("Roblox")
    if not windows:
        print("Окно игры не найдено! Открой TilesSurvive и попробуй снова.")
        return None
    return windows[0]

def get_cursor_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]
    
    point = POINT()
    windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def click_at(x, y):
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    
    user32 = ctypes.windll.user32
    user32.SetCursorPos(x, y)
    time.sleep(0.02)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.02)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def get_pixel_color(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        screenshot = sct.grab(monitor)
        pixel = screenshot.pixel(0, 0)
        return pixel

def get_window_info():
    window = get_game_window()
    if not window:
        return
    
    rect = window.left, window.top, window.width, window.height
    title = window.title
    
    print(f"\n{'='*50}")
    print(f"Окно: {title}")
    print(f"X: {rect[0]}")
    print(f"Y: {rect[1]}")
    print(f"Width: {rect[2]}")
    print(f"Height: {rect[3]}")
    print(f"{'='*50}\n")
    
    return rect

def pick_color():
    window = get_game_window()
    if not window:
        return
    
    print("\nЧерез 3 секунды кликни в нужном месте...")
    print("Наведи курсор и кликни ЛЕВОЙ кнопкой мыши")
    time.sleep(3)
    
    x, y = get_cursor_pos()
    color = get_pixel_color(x, y)
    
    hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
    
    print(f"\nКоординаты: X={x}, Y={y}")
    print(f"Цвет (RGB): {color}")
    print(f"Цвет (HEX): {hex_color}")
    
    return x, y, color, hex_color

def get_screen_region():
    window = get_game_window()
    if not window:
        return None
    
    rect = window.left, window.top, window.width, window.height
    return {
        "left": rect[0],
        "top": rect[1],
        "width": rect[2],
        "height": rect[3]
    }

def scan_region_for_color(target_color, tolerance=30):
    region = get_screen_region()
    if not region:
        return None
    
    print(f"Сканирование области {region['width']}x{region['height']}...")
    print(f"Ищем цвет {target_color} с tolerance={tolerance}")
    
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        
        for y in range(screenshot.height):
            for x in range(screenshot.width):
                pixel = screenshot.pixel(x, y)
                
                if (abs(pixel[0] - target_color[0]) <= tolerance and
                    abs(pixel[1] - target_color[1]) <= tolerance and
                    abs(pixel[2] - target_color[2]) <= tolerance):
                    
                    screen_x = region["left"] + x
                    screen_y = region["top"] + y
                    
                    print(f"\nНАЙДЕНО!")
                    print(f"X: {screen_x}, Y: {screen_y}")
                    print(f"Цвет: {pixel}")
                    
                    return screen_x, screen_y, pixel
    
    print("Цвет не найден")
    return None

if __name__ == "__main__":
    while True:
        print("\n=== Pixel Tool ===")
        print("1. Получить информацию об окне")
        print("2. Взять цвет пикселя (кликни)")
        print("3. Сканировать область")
        print("4. Выйти")
        
        choice = input("\nВыбор: ").strip()
        
        if choice == "1":
            get_window_info()
        elif choice == "2":
            pick_color()
        elif choice == "3":
            color = input("Цвет (R,G,B): ").strip()
            try:
                r, g, b = map(int, color.split(","))
                scan_region_for_color((r, g, b))
            except:
                print("Неверный формат")
        elif choice == "4":
            break