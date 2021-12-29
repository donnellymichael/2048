import torch
import random
import numpy as np
from collections import deque
from gameAI import game2048AI
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
from time import sleep

GAME_WIDTH = 600
GAME_HEIGHT = 700
TEXTCOLOUR = 238, 228, 218

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(16, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = np.array(game.gameBoard)
        #print(state)
        state = np.reshape(game.gameBoard, 16)
        #print(state)
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 100 - self.n_games
        if self.epsilon < 5:
            self.epsilon = 5
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            #print('Next move is: ', final_move)

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    reward = 0
    gameCount = 0
    gameCountList = []
    rewardList = []
    agent = Agent()
    game = game2048AI()
    done = False
    while True:

        #sleep(0.2)

        done = False

        game.drawBoard()
        scoreVal = game.font.render(str(game.score), 1, TEXTCOLOUR)
        game.screen.blit(game.scoreText, (100, 20))
        game.screen.blit(scoreVal, (150, 70))
        
        # This returns our input to the NN
        state_old = agent.get_state(game)

        # This calculates the action from the state, one of these:
        # [1 0 0 0] = Left
        # [0 1 0 0] = Up
        # [0 0 1 0] = Right
        # [0 0 0 1] = Down
        final_move = agent.get_action(state_old)

        prevGameBoard = game.gameBoard
        oldScore = game.score

        # makeMove performs the move on the gameBoard
        game.makeMove(final_move)

        newScore = game.score

        # +10 for a valid move
        if (game.isValidMove(prevGameBoard) and not game.boardFull()):
            reward += newScore-oldScore
            game.addRandomTile()

        # -10 for a game over
        if (game.boardFull()) and game.checkGameOver():
            #print('GAME OVER')
            reward -= 100
            done = True
        
        score = game.score
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            done = False
            gameCountList.append(gameCount)
            gameCount += 1
            rewardList.append(reward)
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            if gameCount == 100:
                plt.plot(gameCountList, plot_mean_scores)
                plt.title('Plot of mean scores')
                plt.show()

                plt.plot(gameCountList, plot_scores)
                plt.title('Plot of scores')
                plt.show()

                plt.plot(gameCountList, rewardList)
                plt.title('Plot of reward')
                plt.show()


if __name__ == '__main__':
    train()