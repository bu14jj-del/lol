from PIL import ImageGrab
import win32api, win32con
import time
import math

x_pad = 222
y_pad = 351

SQUARE_COORDS = {
    0: (65, 30), 1: (185, 30), 2: (305, 30), 3: (425, 30),
    4: (65, 150), 5: (185, 150), 6: (305, 150), 7: (425, 150),
    8: (65, 270), 9: (185, 270), 10: (305, 270), 11: (425, 270),
    12: (65, 390), 13: (185, 390), 14: (305, 390), 15: (425, 390)
}

VK_CODE = {'left': 0x25, 'up': 0x26, 'right': 0x27, 'down': 0x28}

SQUARE_SCORES = {
    0: 0, 2: 0, 4: 4, 8: 11, 16: 28, 32: 65, 64: 141,
    128: 300, 256: 627, 512: 1292, 1024: 2643, 2048: 5372
}

SQUARE_MULTS = {
    0: 2, 1: 2, 2: 2, 3: 2,
    4: 1.25, 5: 1.25, 6: 1.25, 7: 1.25,
    8: 1, 9: 1, 10: 1, 11: 1,
    12: 0.8, 13: 0.8, 14: 0.8, 15: 0.8
}

def arrowKey(direction):
    win32api.keybd_event(VK_CODE[direction], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(VK_CODE[direction], 0, win32con.KEYEVENTF_KEYUP, 0)

def screenGrab():
    box = (x_pad, y_pad, 722, 851)
    return ImageGrab.grab(box)

def getSquareNumbers():
    im = screenGrab()
    board = [[0]*4 for _ in range(4)]
    
    for sq in range(16):
        rgb = im.getpixel(SQUARE_COORDS[sq])
        val = getNumberFromRGB(rgb)
        board[sq % 4][sq // 4] = val
    
    return board

def getNumberFromRGB(rgb):
    def distance(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    
    if distance(rgb, (204, 192, 179)) <= 5: return 0
    elif distance(rgb, (238, 228, 218)) <= 5: return 2
    elif distance(rgb, (237, 224, 200)) <= 5: return 4
    elif distance(rgb, (242, 177, 121)) <= 5: return 8
    elif distance(rgb, (245, 149, 99)) <= 5: return 16
    elif distance(rgb, (246, 124, 95)) <= 5: return 32
    elif distance(rgb, (246, 94, 59)) <= 5: return 64
    elif distance(rgb, (237, 207, 114)) <= 5: return 128
    elif distance(rgb, (237, 204, 97)) <= 5: return 256
    elif distance(rgb, (237, 200, 80)) <= 5: return 512
    elif distance(rgb, (237, 197, 63)) <= 3: return 1024
    elif distance(rgb, (237, 194, 46)) <= 5: return 2048
    return 0

def makeMove(array, direction):
    score = 0
    legal = 0
    arr = [row[:] for row in array]
    
    if direction == 'left':
        for y in range(4):
            row = [x for x in arr[y] if x]
            for i in range(len(row)-1):
                if row[i] == row[i+1] and row[i]:
                    row[i] *= 2
                    score += row[i]
                    row[i+1] = 0
            row = [x for x in row if x]
            while len(row) < 4: row.append(0)
            arr[y] = row
            if row != arr[y]: legal = 1
    
    elif direction == 'right':
        for y in range(4):
            row = [x for x in arr[y] if x][::-1]
            for i in range(len(row)-1):
                if row[i] == row[i+1] and row[i]:
                    row[i] *= 2
                    score += row[i]
                    row[i+1] = 0
            row = [x for x in row if x]
            while len(row) < 4: row.append(0)
            arr[y] = row[::-1]
            if arr[y] != array[y]: legal = 1
    
    elif direction == 'up':
        for x in range(4):
            col = [arr[y][x] for y in range(4) if arr[y][x]]
            for i in range(len(col)-1):
                if col[i] == col[i+1] and col[i]:
                    col[i] *= 2
                    score += col[i]
                    col[i+1] = 0
            col = [x for x in col if x]
            while len(col) < 4: col.append(0)
            for y in range(4):
                arr[y][x] = col[y]
            if arr[0][x] != array[0][x] or arr[1][x] != array[1][x]: legal = 1
    
    elif direction == 'down':
        for x in range(4):
            col = [arr[y][x] for y in range(4) if arr[y][x]][::-1]
            for i in range(len(col)-1):
                if col[i] == col[i+1] and col[i]:
                    col[i] *= 2
                    score += col[i]
                    col[i+1] = 0
            col = [x for x in col if x]
            while len(col) < 4: col.append(0)
            for y in range(4):
                arr[y][x] = col[::-1][y]
            if arr[3][x] != array[3][x]: legal = 1
    
    return (arr, score if legal else -1)

def evaluateBoard(array):
    score = 0
    maximum = 0
    for sq in range(16):
        val = array[sq % 4][sq // 4]
        score += SQUARE_SCORES.get(val, 0) * SQUARE_MULTS[sq]
        maximum = max(maximum, val)
    if array[0][0] == maximum and maximum > 0:
        score *= 1.4
    return score

def search(array, depth):
    best_score = -1
    best_move = 'left'
    
    for move in ['left', 'up', 'down', 'right']:
        new_board, move_score = makeMove(array, move)
        
        if move_score == -1:
            continue
        
        if depth <= 0:
            score = move_score + evaluateBoard(new_board)
        else:
            worst = 100000000
            for sq in range(16):
                if new_board[sq % 4][sq // 4] != 0:
                    continue
                temp = [row[:] for row in new_board]
                temp[sq % 4][sq // 4] = 2
                s = evaluateBoard(temp)
                worst = min(worst, s)
                if new_board[0][0] == 0:
                    worst *= 0.9
                if new_board[1][0] == 0:
                    worst *= 0.97
            score = 0.9 * (move_score + worst)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return (best_move, best_score)

def printBoard(array, text=""):
    print(text)
    for row in array:
        print(row)

moves = 0
max_score = 0

def main():
    global moves, max_score
    
    print("Старт через 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Поехали!")
    
    while True:
        board = getSquareNumbers()
        
        if moves % 10 == 0:
            printBoard(board, f'Ход: {moves}')
        
        (move, score) = search(board, 3)
        print(f"Ход: {move}, Оценка: {score}")
        
        arrowKey(move)
        time.sleep(0.3)
        
        moves += 1
        
        if moves > 5000:
            print(f"Стоп! Макс счет: {max_score}")
            break

if __name__ == '__main__':
    moves = 0
    max_score = 0
    main()