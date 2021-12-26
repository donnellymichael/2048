import pygame
import random

GAME_WIDTH = 600
GAME_HEIGHT = 700
BOARD_WIDTH = 4
BOARD_HEIGHT = 4
TILESIZE = 120
TILECOLOUR = 102, 102, 102
TEXTCOLOUR = 238, 228, 218
BORDERCOLOUR = 74, 74, 74

XMARGIN = int((GAME_WIDTH - (TILESIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
YMARGIN = int((GAME_HEIGHT +50 - (TILESIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

def main():
    global screen, font

    font = pygame.font.SysFont("Clear Sans Regular", 60)
    screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
    pygame.display.set_caption('2048')

    gameBoard = getStartingBoard()
    score = 0

    scoreText = font.render("Score:", 1, TEXTCOLOUR)
    
    running = True
    while running:

        prevGameBoard = gameBoard
        drawBoard(gameBoard)
        scoreVal = font.render(str(score), 1, TEXTCOLOUR)
        screen.blit(scoreText, (100, 20))
        screen.blit(scoreVal, (150, 70))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('KEY PRESSED')
                
                if event.key == pygame.K_UP:
                    print("UP")
                    gameBoard = [list(col) for col in zip(*gameBoard[::-1])]
                    score += moveTilesRight(gameBoard, BOARD_HEIGHT)
                    gameBoard = [list(col) for col in list(reversed(list(zip(*gameBoard))))]

                if event.key == pygame.K_DOWN:
                    print("DOWN")
                    gameBoard = [list(col) for col in zip(*gameBoard[::-1])]
                    score += moveTilesLeft(gameBoard, BOARD_HEIGHT)
                    gameBoard = [list(col) for col in list(reversed(list(zip(*gameBoard))))]

                if event.key == pygame.K_LEFT:
                    print("LEFT")
                    gameBoard = [list(col) for col in gameBoard]
                    score += moveTilesLeft(gameBoard, BOARD_WIDTH)

                if event.key == pygame.K_RIGHT:
                    print("RIGHT")
                    gameBoard = [list(col) for col in gameBoard]
                    score += moveTilesRight(gameBoard, BOARD_WIDTH)

                if (isValidMove(prevGameBoard, gameBoard)):
                    addRandomTile(gameBoard)
                else:
                    print('Move invalid')

                if (boardFull(gameBoard)) and checkGameOver(gameBoard):
                    print('game over')
   
            if event.type == pygame.QUIT:
                running = False

def boardFull(game):
    for row in range(len(game)):
        for col in range(len(game[0])):
            if game[row][col] == 0:
                return False
    else: return True

def checkGameOver(game):
    for row in range(len(game)):
        for col in range(1, 3, 1):
            if game[row][col] == game[row][col-1]:
                return False

    game = [list(col) for col in zip(*game[::-1])]
    for row in range(len(game)):
        for col in range(1, 3, 1):
            if game[row][col] == game[row][col-1]:
                return False
    game = [list(col) for col in list(reversed(list(zip(*game))))]
    
    return True
            
            
def isValidMove(prevBoard, currBoard):
    if currBoard == prevBoard:
        return False
    else:
        return True

def moveTilesLeft(board, n):
    points = 0
    for arr in board:
        pushZerosToEnd(arr, n)
        for j in range(1, n, 1):
            if arr[j] == arr[j-1]:
                points += arr[j]+arr[j-1]
                arr[j-1] = arr[j]+arr[j-1]
                arr[j] = 0
        pushZerosToEnd(arr, n)
    return points

def pushZerosToEnd(arr, n):
    count = 0
    for i in range(n):
        if arr[i] != 0:  
            arr[count] = arr[i]
            count+=1
    while count < n:
        arr[count] = 0
        count += 1

def moveTilesRight(board, n):
    points = 0
    for arr in board:
        pushZerosToStart(arr, n)
        for j in range(2, -1, -1):
            if arr[j] == arr[j+1]:
                points += arr[j]+arr[j+1]
                arr[j+1] = arr[j]+arr[j+1]
                arr[j] = 0
        pushZerosToStart(arr, n)
    return points

def pushZerosToStart(arr, n):
    count = 0
    for i in range(3, -1, -1):
        if arr[i] != 0:  
            arr[3-count] = arr[i]
            count+=1
    while count < n:
        arr[3-count] = 0
        count += 1

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def addRandomTile(board):
    emptyTileCoordinates = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                emptyTileCoordinates.append([row, col])

    newTileLocation = random.choice(range(len(emptyTileCoordinates)))
    newTileX = emptyTileCoordinates[newTileLocation][0]
    newTileY = emptyTileCoordinates[newTileLocation][1]
    board[newTileX][newTileY] = 2 # change this to 2 or 4 with some probabilities
    drawTile(newTileX, newTileY, 2)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(screen, TILECOLOUR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number != 0:
        textSurf = font.render(str(number), True, TEXTCOLOUR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        screen.blit(textSurf, textRect)

def drawBoard(board):
    screen.fill(BORDERCOLOUR)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            drawTile(tiley, tilex, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARD_WIDTH * TILESIZE
    height = BOARD_HEIGHT * TILESIZE
    pygame.draw.rect(screen, BORDERCOLOUR, (left - 5, top - 5, width + 11, height + 11), 4)

def getStartingBoard():
    random.seed(a=None, version=2)
    board = []

    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(0)
        board.append(column)

    startingNumber1X = random.randint(0, 3)
    startingNumber1Y = random.randint(0, 3)
    startingNumber2X = random.randint(0, 3)
    startingNumber2Y = random.randint(0, 3)
    board[startingNumber1X][startingNumber1Y] = 2
    board[startingNumber2X][startingNumber2Y] = 2  
    return board

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()