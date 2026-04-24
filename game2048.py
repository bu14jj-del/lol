from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class Game2048Bot:
    def __init__(self):
        self.driver = None
        self.running = False
        
    def start(self):
        self.driver = webdriver.Edge()
        self.driver.get("https://play2048.co/")
        time.sleep(5)
        print("Игра 2048 запущена!")
        self.running = True
        self.play()
    
    def get_grid(self):
        grid = [[0]*4 for _ in range(4)]
        try:
            tiles = self.driver.find_elements(By.CSS_SELECTOR, ".tile")
            
            for tile in tiles:
                classes = tile.get_attribute("class")
                if "tile-position" in classes:
                    pos_class = [c for c in classes.split() if "tile-position" in c][0]
                    pos = pos_class.replace("tile-position-", "").split("-")
                    row, col = int(pos[0]) - 1, int(pos[1]) - 1
                    
                    inner = tile.find_element(By.CSS_SELECTOR, ".tile-inner")
                    value = int(inner.text)
                    
                    grid[row][col] = value
        except:
            pass
        return grid
    
    def print_grid(self, grid):
        print("\n  2048")
        print("-" * 17)
        for row in grid:
            print("|" + "|".join([f"{v:4d}" if v else "   ." for v in row]) + "|")
            print("-" * 17)
    
    def move_grid(self, grid, direction):
        new_grid = [row[:] for row in grid]
        
        if direction == "left":
            for r in range(4):
                row = [x for x in new_grid[r] if x]
                for c in range(len(row)-1):
                    if row[c] == row[c+1]:
                        row[c] *= 2
                        row[c+1] = 0
                row = [x for x in row if x]
                while len(row) < 4:
                    row.append(0)
                new_grid[r] = row
        elif direction == "right":
            for r in range(4):
                row = [x for x in new_grid[r] if x][::-1]
                for c in range(len(row)-1):
                    if row[c] == row[c+1]:
                        row[c] *= 2
                        row[c+1] = 0
                row = [x for x in row if x]
                while len(row) < 4:
                    row.append(0)
                new_grid[r] = row[::-1]
        elif direction == "up":
            for c in range(4):
                col = [new_grid[r][c] for r in range(4) if new_grid[r][c]]
                for r in range(len(col)-1):
                    if col[r] == col[r+1]:
                        col[r] *= 2
                        col[r+1] = 0
                col = [x for x in col if x]
                while len(col) < 4:
                    col.append(0)
                for r in range(4):
                    new_grid[r][c] = col[r]
        elif direction == "down":
            for c in range(4):
                col = [new_grid[r][c] for r in range(4) if new_grid[r][c]][::-1]
                for r in range(len(col)-1):
                    if col[r] == col[r+1]:
                        col[r] *= 2
                        col[r+1] = 0
                col = [x for x in col if x]
                while len(col) < 4:
                    col.append(0)
                for r in range(4):
                    new_grid[r][c] = col[::-1][r]
        
        return new_grid
    
    def get_best_move(self, grid):
        best = "left"
        best_score = -1
        
        for move in ["left", "up", "down"]:
            new_grid = self.move_grid(grid, move)
            if new_grid != grid:
                empty = sum(1 for r in range(4) for c in range(4) if new_grid[r][c] == 0)
                max_tile = max(r for row in new_grid for r in row)
                score = empty * 100 + max_tile
                if score > best_score:
                    best_score = score
                    best = move
        
        if best_score == -1:
            best = "right"
        
        return best
    
    def move(self, direction):
        try:
            actions = ActionChains(self.driver)
            
            if direction == "up":
                actions.send_keys(Keys.ARROW_UP)
            elif direction == "down":
                actions.send_keys(Keys.ARROW_DOWN)
            elif direction == "left":
                actions.send_keys(Keys.ARROW_LEFT)
            elif direction == "right":
                actions.send_keys(Keys.ARROW_RIGHT)
            
            actions.perform()
            time.sleep(0.25)
        except:
            pass
    
    def is_game_over(self):
        try:
            msg = self.driver.find_element(By.CSS_SELECTOR, ".game-message")
            style = msg.get_attribute("style")
            if style and "none" in style:
                return False
            p = msg.find_element(By.CSS_SELECTOR, "p")
            if p and p.text:
                return True
        except:
            pass
        return False
    
    def get_score(self):
        try:
            score = self.driver.find_element(By.CSS_SELECTOR, ".score-container .value")
            return int(score.text.replace(" ", ""))
        except:
            return 0
    
    def restart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".restart-button").click()
            time.sleep(0.5)
        except:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".retry-button").click()
                time.sleep(0.5)
            except:
                pass
    
    def play(self):
        moves = 0
        score = 0
        max_score = 0
        
        while self.running:
            grid = self.get_grid()
            
            if moves % 30 == 0:
                self.print_grid(grid)
            
            if self.is_game_over():
                print(f"Игра окончена! Счет: {score}, Макс: {max_score}")
                self.restart()
                moves = 0
                continue
            
            current_score = self.get_score()
            if current_score > max_score:
                max_score = current_score
                print(f"Рекорд: {max_score}")
            
            score = current_score
            
            best_move = self.get_best_move(grid)
            self.move(best_move)
            
            moves += 1
            
            if moves > 5000:
                print(f"Итог: {max_score}")
                break
        
        input("Enter...")
        self.driver.quit()

if __name__ == "__main__":
    bot = Game2048Bot()
    bot.start()