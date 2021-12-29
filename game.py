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
    game = game2048()
    
    running = True
    while running:

        prevGameBoard = game.gameBoard
        game.drawBoard()
        scoreVal = game.font.render(str(game.score), 1, TEXTCOLOUR)
        game.screen.blit(game.scoreText, (100, 20))
        game.screen.blit(scoreVal, (150, 70))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('KEY PRESSED')
                
                game.makeMove(event)

                if (game.isValidMove(prevGameBoard) and not game.boardFull()):
                    game.addRandomTile()

                if (game.boardFull()) and game.checkGameOver():
                    print('game over')
                    #game.reset()
   
            if event.type == pygame.QUIT:
                running = False

class game2048:
    def __init__(self, width=GAME_WIDTH, height=GAME_HEIGHT):
        self.font = pygame.font.SysFont("Clear Sans Regular", 60)
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
        pygame.display.set_caption('2048')
        self.gameBoard = self.getStartingBoard()
        self.score = 0
        self.scoreText = self.font.render("Score:", 1, TEXTCOLOUR)
    
    def reset(self):
        self.gameBoard = self.getStartingBoard()
        self.score = 0
        self.frameIteration = 0

    def makeMove(self, event):
        if event.key == pygame.K_UP:
            print("UP")
            self.gameBoard = [list(col) for col in zip(*self.gameBoard[::-1])]
            self.score += self.moveTilesRight(BOARD_HEIGHT)
            for i in range(0, 3, 1):
                self.gameBoard = [list(col) for col in zip(*self.gameBoard[::-1])]

        if event.key == pygame.K_DOWN:
            print("DOWN")
            self.gameBoard = [list(col) for col in zip(*self.gameBoard[::-1])]
            self.score += self.moveTilesLeft(BOARD_HEIGHT)
            for i in range(0, 3, 1):
                self.gameBoard = [list(col) for col in zip(*self.gameBoard[::-1])]

        if event.key == pygame.K_LEFT:
            print("LEFT")
            self.gameBoard = [list(col) for col in self.gameBoard]
            self.score += self.moveTilesLeft(BOARD_WIDTH)

        if event.key == pygame.K_RIGHT:
            print("RIGHT")
            self.gameBoard = [list(col) for col in self.gameBoard]
            self.score += self.moveTilesRight(BOARD_WIDTH)

    def boardFull(self):
        for row in range(len(self.gameBoard)):
            for col in range(len(self.gameBoard[0])):
                if self.gameBoard[row][col] == 0:
                    return False
        else: return True

    def checkGameOver(self):
        for row in range(len(self.gameBoard)):
            for col in range(1, 3, 1):
                if self.gameBoard[row][col] == self.gameBoard[row][col-1]:
                    return False
        self.gameBoard = [list(col) for col in zip(*self.gameBoard[::-1])]
        for row in range(len(self.gameBoard)):
            for col in range(1, 3, 1):
                if self.gameBoard[row][col] == self.gameBoard[row][col-1]:
                    return False
        game = [list(col) for col in list(reversed(list(zip(*self.gameBoard))))]
        return True
                
    def isValidMove(self, prevBoard):
        if self.gameBoard == prevBoard:
            return False
        else:
            return True

    def moveTilesLeft(self, n):
        points = 0
        for arr in self.gameBoard:
            self._pushZerosToEnd(arr, n)
            for j in range(1, n, 1):
                if arr[j] == arr[j-1]:
                    points += arr[j]+arr[j-1]
                    arr[j-1] = arr[j]+arr[j-1]
                    arr[j] = 0
            self._pushZerosToEnd(arr, n)
        return points

    def _pushZerosToEnd(self, arr, n):
        count = 0
        for i in range(n):
            if arr[i] != 0:  
                arr[count] = arr[i]
                count+=1
        while count < n:
            arr[count] = 0
            count += 1

    def moveTilesRight(self, n):
        points = 0
        for arr in self.gameBoard:
            self._pushZerosToStart(arr, n)
            for j in range(2, -1, -1):
                if arr[j] == arr[j+1]:
                    points += arr[j]+arr[j+1]
                    arr[j+1] = arr[j]+arr[j+1]
                    arr[j] = 0
            self._pushZerosToStart(arr, n)
        return points

    def _pushZerosToStart(self, arr, n):
        count = 0
        for i in range(3, -1, -1):
            if arr[i] != 0:  
                arr[3-count] = arr[i]
                count+=1
        while count < n:
            arr[3-count] = 0
            count += 1

    def getLeftTopOfTile(self, tileX, tileY):
        left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return (left, top)

    def addRandomTile(self):
        emptyTileCoordinates = []
        for row in range(len(self.gameBoard)):
            for col in range(len(self.gameBoard[row])):
                if self.gameBoard[row][col] == 0:
                    emptyTileCoordinates.append([row, col])

        newTileLocation = random.choice(range(len(emptyTileCoordinates)))
        newTileX = emptyTileCoordinates[newTileLocation][0]
        newTileY = emptyTileCoordinates[newTileLocation][1]
        self.gameBoard[newTileX][newTileY] = 2 # change this to 2 or 4 with some probabilities
        self.drawTile(newTileX, newTileY, 2)

    def drawTile(self, tilex, tiley, number, adjx=0, adjy=0):
        left, top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(self.screen, TILECOLOUR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        if number != 0:
            textSurf = self.font.render(str(number), True, TEXTCOLOUR)
            textRect = textSurf.get_rect()
            textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
            self.screen.blit(textSurf, textRect)

    def drawBoard(self):
        self.screen.fill(BORDERCOLOUR)
        for tilex in range(len(self.gameBoard)):
            for tiley in range(len(self.gameBoard[0])):
                self.drawTile(tiley, tilex, self.gameBoard[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = BOARD_WIDTH * TILESIZE
        height = BOARD_HEIGHT * TILESIZE
        pygame.draw.rect(self.screen, BORDERCOLOUR, (left - 5, top - 5, width + 11, height + 11), 4)

    def getStartingBoard(self):
        random.seed(a=None, version=2)
        self.gameBoard = []

        for x in range(BOARD_WIDTH):
            column = []
            for y in range(BOARD_HEIGHT):
                column.append(0)
            self.gameBoard.append(column)

        startingNumber1X = random.randint(0, 3)
        startingNumber1Y = random.randint(0, 3)
        startingNumber2X = random.randint(0, 3)
        startingNumber2Y = random.randint(0, 3)
        self.gameBoard[startingNumber1X][startingNumber1Y] = 2
        self.gameBoard[startingNumber2X][startingNumber2Y] = 2  
        return self.gameBoard

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()