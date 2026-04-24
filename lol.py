import tkinter as tk
from tkinter import ttk, scrolledtext
import mss
import pygetwindow as gw
import threading
import time

class ClickerBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Кликер Бот")
        self.is_running = False
        self.is_paused = False
        self.click_count = 0
        self.delay = 1000

        self.game_window = None
        self.last_location = None

        self.village_pixels = [
            {"x": 404, "y": 47, "color": (122, 86, 63)},
            {"x": 596, "y": 45, "color": (166, 96, 68)},
        ]

        self.wildlands_pixels = [
            {"x": 318, "y": 51, "color": (247, 144, 41)},
            {"x": 630, "y": 833, "color": (44, 148, 217)},
        ]

        self.wildlands_search_pixels = [
            {"x": 318, "y": 51, "color": (247, 144, 41)},
            {"x": 630, "y": 833, "color": (44, 148, 217)},
            {"x": 289, "y": 837, "color": (255, 255, 255)},
        ]

        self.attack_pixels = [
            {"x": 301, "y": 413, "color": (123, 215, 77)},
            {"x": 275, "y": 837, "color": (123, 215, 77)},
        ]

        self.attack_demon_pixels = [
            {"x": 305, "y": 396, "color": (123, 215, 77)},
            {"x": 275, "y": 837, "color": (123, 215, 77)},
        ]

        self.location_label = None
        self.check_thread = None
        self.running_check = False

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TFrame', background='#f0f0f0')

        self.create_widgets()
        self.create_menu()

    def get_game_window(self):
        windows = gw.getWindowsWithTitle("TilesSurvive")
        if not windows:
            windows = gw.getWindowsWithTitle("Tiles Survive")
        if not windows:
            windows = gw.getWindowsWithTitle("Roblox")
        return windows[0] if windows else None

    def get_pixel_color(self, x, y):
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            screenshot = sct.grab(monitor)
            pixel = screenshot.pixel(0, 0)
            return pixel

    def check_village(self):
        if not self.game_window:
            self.game_window = self.get_game_window()
            if not self.game_window:
                return False

        offset_x = self.game_window.left
        offset_y = self.game_window.top

        matches = 0
        for pixel_info in self.village_pixels:
            screen_x = offset_x + pixel_info["x"]
            screen_y = offset_y + pixel_info["y"]
            pixel_color = self.get_pixel_color(screen_x, screen_y)

            if (abs(pixel_color[0] - pixel_info["color"][0]) <= 20 and
                abs(pixel_color[1] - pixel_info["color"][1]) <= 20 and
                abs(pixel_color[2] - pixel_info["color"][2]) <= 20):
                matches += 1

        return matches == len(self.village_pixels)

    def check_wildlands(self):
        if not self.game_window:
            self.game_window = self.get_game_window()
            if not self.game_window:
                return False

        offset_x = self.game_window.left
        offset_y = self.game_window.top

        matches = 0
        for pixel_info in self.wildlands_pixels:
            screen_x = offset_x + pixel_info["x"]
            screen_y = offset_y + pixel_info["y"]
            pixel_color = self.get_pixel_color(screen_x, screen_y)

            if (abs(pixel_color[0] - pixel_info["color"][0]) <= 20 and
                abs(pixel_color[1] - pixel_info["color"][1]) <= 20 and
                abs(pixel_color[2] - pixel_info["color"][2]) <= 20):
                matches += 1

        return matches == len(self.wildlands_pixels)

    def check_wildlands_search(self):
        if not self.game_window:
            self.game_window = self.get_game_window()
            if not self.game_window:
                return False

        offset_x = self.game_window.left
        offset_y = self.game_window.top

        matches = 0
        for pixel_info in self.wildlands_search_pixels:
            screen_x = offset_x + pixel_info["x"]
            screen_y = offset_y + pixel_info["y"]
            pixel_color = self.get_pixel_color(screen_x, screen_y)

            if (abs(pixel_color[0] - pixel_info["color"][0]) <= 20 and
                abs(pixel_color[1] - pixel_info["color"][1]) <= 20 and
                abs(pixel_color[2] - pixel_info["color"][2]) <= 20):
                matches += 1

        return matches == len(self.wildlands_search_pixels)

    def check_attack(self):
        if not self.game_window:
            return False

        offset_x = self.game_window.left
        offset_y = self.game_window.top

        matches = 0
        for pixel_info in self.attack_pixels:
            screen_x = offset_x + pixel_info["x"]
            screen_y = offset_y + pixel_info["y"]
            pixel_color = self.get_pixel_color(screen_x, screen_y)

            if (abs(pixel_color[0] - pixel_info["color"][0]) <= 20 and
                abs(pixel_color[1] - pixel_info["color"][1]) <= 20 and
                abs(pixel_color[2] - pixel_info["color"][2]) <= 20):
                matches += 1

        return matches == len(self.attack_pixels)

    def check_attack_demon(self):
        if not self.game_window:
            return False

        offset_x = self.game_window.left
        offset_y = self.game_window.top

        matches = 0
        for pixel_info in self.attack_demon_pixels:
            screen_x = offset_x + pixel_info["x"]
            screen_y = offset_y + pixel_info["y"]
            pixel_color = self.get_pixel_color(screen_x, screen_y)

            if (abs(pixel_color[0] - pixel_info["color"][0]) <= 20 and
                abs(pixel_color[1] - pixel_info["color"][1]) <= 20 and
                abs(pixel_color[2] - pixel_info["color"][2]) <= 20):
                matches += 1

        return matches == len(self.attack_demon_pixels)

    def get_current_location(self):
        if self.check_village():
            return "Деревня"
        
        offset_x = self.game_window.left
        offset_y = self.game_window.top
        
        screen_x = offset_x + 318
        screen_y = offset_y + 51
        color_d1 = self.get_pixel_color(screen_x, screen_y)
        
        if abs(color_d1[0] - 129) < 30 and abs(color_d1[1] - 181) < 30 and abs(color_d1[2] - 220) < 30:
            
            if self.check_attack_demon():
                return "Окно атаки | Нечисть"
            return "Окно атаки"
        
        if abs(color_d1[0] - 247) < 30 and abs(color_d1[1] - 144) < 30 and abs(color_d1[2] - 41) < 30:
            
            sx = offset_x + 630
            sy = offset_y + 833
            color_d2 = self.get_pixel_color(sx, sy)
            
            if color_d2[0] == 49 and color_d2[1] == 98 and color_d2[2] == 140:
                return "Дикие земли | Поиск"
            return "Дикие земли"
        
        return "Неизвестно"

    def background_check(self):
        while self.running_check:
            try:
                current_location = self.get_current_location()
                
                if self.last_location != current_location:
                    self.last_location = current_location
                    
                    if current_location == "Деревня":
                        color = "#00aa00"
                    elif "Окно атаки" in current_location:
                        color = "#ff0000"
                    elif "Поиск" in current_location:
                        color = "#ffd700"
                    elif "Дикие земли" in current_location:
                        color = "#ff8800"
                    else:
                        color = "#ff4444"
                    
                    self.root.after(0, lambda loc=current_location, c=color: self.location_label.config(
                        text=f"{loc}",
                        foreground=c
                    ))
                    
                    self.log(f"📍 Переход: {current_location}")
                
                if not self.is_paused:
                    if current_location == "Деревня":
                        color = "#00aa00"
                    elif "Окно атаки" in current_location:
                        color = "#ff0000"
                    elif "Поиск" in current_location:
                        color = "#ffd700"
                    elif "Дикие земли" in current_location:
                        color = "#ff8800"
                    else:
                        color = "#ff4444"
                    self.root.after(0, lambda loc=current_location, c=color: self.location_label.config(
                        text=f"{loc}",
                        foreground=c
                    ))
                
            except Exception as e:
                self.log(f"Ошибка: {e}")
            
            time.sleep(0.5)

    def create_widgets(self):
        self.root.configure(bg='#e0f7fa')

        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill='x')

        self.start_button = ttk.Button(control_frame, text="🚀 Старт", command=self.start_clicking)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(control_frame, text="⏸️ Пауза", command=self.pause_clicking, state='disabled')
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(control_frame, text="⏹️ Стоп", command=self.stop_clicking, state='disabled')
        self.stop_button.grid(row=0, column=2, padx=5)

        self.counter_label = ttk.Label(self.root, text="🖱️ Кликов: 0", background='#e0f7fa')
        self.counter_label.pack(pady=5)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=5)

        self.location_label = tk.Label(
            status_frame,
            text="Локация: ?",
            font=('Arial', 14, 'bold'),
            background='#e0f7fa',
            foreground='#888888'
        )
        self.location_label.pack()

        settings_frame = ttk.LabelFrame(self.root, text="Настройки 🔧")
        settings_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(settings_frame, text="Задержка (мс):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.delay_var = tk.IntVar(value=self.delay)
        self.delay_entry = ttk.Entry(settings_frame, textvariable=self.delay_var, width=10)
        self.delay_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        logs_frame = ttk.LabelFrame(self.root, text="Логи 📝")
        logs_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            height=10,
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white'
        )
        self.logs_text.pack(fill='both', expand=True, padx=5, pady=5)

        self.fit_button = ttk.Button(self.root, text="📐 Подогнать окно", command=self.fit_window)
        self.fit_button.pack(pady=5)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Меню", menu=settings_menu)
        settings_menu.add_command(label="Выход", command=self.root.quit)

    def log(self, message):
        self.logs_text.insert(tk.END, message + '\n')
        self.logs_text.see(tk.END)

    def start_clicking(self):
        self.is_running = True
        self.is_paused = False
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal', text='⏸️ Пауза')
        self.stop_button.config(state='normal')

        self.game_window = self.get_game_window()
        if not self.game_window:
            self.log("❌ Окно игры не найдено!")
            self.is_running = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            return

        self.log(f"✅ Окно найдено: {self.game_window.title}")

        current_location = self.get_current_location()
        print(f"Локация = {current_location}")
        self.log(f"📍 Локация: {current_location}")

        self.running_check = True
        self.check_thread = threading.Thread(target=self.background_check, daemon=True)
        self.check_thread.start()

        self.log("🔥 Запуск кликера")
        self.click()

    def pause_clicking(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text='▶️ Продолжить')
            self.log("⏸️ Пауза приостановлена")
        else:
            self.pause_button.config(text='⏸️ Пауза')
            self.log("▶️ Продолжение работы")
            self.click()

    def stop_clicking(self):
        self.is_running = False
        self.running_check = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text='⏸️ Пауза')
        self.stop_button.config(state='disabled')
        self.log("🛑 Кликер остановлен")

    def click(self):
        if self.is_running and not self.is_paused:
            self.click_count += 1
            self.counter_label.config(text=f"🖱️ Кликов: {self.click_count}")
            try:
                self.delay = int(self.delay_var.get())
            except ValueError:
                self.delay = 1000
            self.log(f"Клик #{self.click_count}")
            self.root.after(self.delay, self.click)

    def fit_window(self):
        self.root.update_idletasks()
        self.root.geometry('')
        self.root.resizable(True, True)
        self.log("🧩 Размер окна подогнан")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerBot(root)
    root.mainloop()