from game import Game
import pygame
import sys
import os 
import neat
from helper import *
import random
import pickle

pygame.init()

class TetrisGame:

    def __init__(self):
        self.game = Game()

    def run(self):

        light_grey = (60,52,75)


        score_font = pygame.font.Font(None, 40)

        screen = pygame.display.set_mode((500,600))
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()

        UPDATE = pygame.USEREVENT
        pygame.time.set_timer(UPDATE, 200)


        while self.game.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.game.state == 1:
                    if event.key == pygame.K_LEFT:
                        self.game.left()

                    if event.key == pygame.K_RIGHT:
                        self.game.right()

                    if event.key == pygame.K_DOWN:
                        self.game.down()
                        
                    if event.key == pygame.K_UP:
                        self.game.rotate()
                
                if event.type == UPDATE and self.game.state == 1:
                    self.game.down()
                    #pygame.time.set_timer(UPDATE, max((100 - (game.score//400)*10), 80))
            
            score_surface = score_font.render(str(self.game.score), True, (255,255,255))


            screen.fill(light_grey)
            self.game.board.draw(screen)
            self.game.cur_piece.draw(screen)
            screen.blit(score_surface, (310,100))
            pygame.display.update()


            clock.tick(60)

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        light_grey = (60,52,75)
        score_font = pygame.font.Font(None, 40)
        screen = pygame.display.set_mode((500,600))
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()
        UPDATE = pygame.USEREVENT
        pygame.time.set_timer(UPDATE, 1)

        OUTPUT = pygame.USEREVENT + 1
        pygame.time.set_timer(OUTPUT, 1)
        inc= 10
        mx=None
        maxSpeed=False
        while self.game.state != 0:

            #Select Move
            if self.game.state == 1:

                #get move and matching features
                board = [row[:] for row in self.game.board.board]
                stats, moves, boards = calculate_moves(board, self.game.cur_piece.id)
                holder = list(zip(stats,moves,boards))
                random.shuffle(holder)

                #pick best move
                for stat, move, bc in holder:
                    
                    output = net.activate(stat)
                    if mx==None or output>=mx[0]:
                        mx=[output, move, bc, stat]

                self.game.state = 2


            for event in pygame.event.get():
                if event.type == OUTPUT and self.game.state == 2:
                    
                    if mx[1][0] > 0:
                        self.game.rotate()
                        mx[1][0] -=1
                    else:

                        left_most = self.game.cur_piece.cords[0][0]
                        for i in range(1,4):
                            if self.game.cur_piece.cords[i][0] < left_most:
                                left_most = self.game.cur_piece.cords[i][0]
                    
                        if left_most < mx[1][1]:
                            self.game.right()
                        elif left_most > mx[1][1]:
                            self.game.left()
                        else:
                            self.game.state=3
                            self.game.check = mx[2]

                            mx=None
                    
                if event.type == UPDATE:
                    self.game.down()

            if not maxSpeed==False:
                newSpeed = max(30, 80-(inc/2))

                if self.game.score >= inc:
                    pygame.time.set_timer(UPDATE, newSpeed)
                    inc += 10

                if newSpeed == 30:
                    maxSpeed = True

            if self.game.score >= 600:
                self.game.state=0

            score_surface = score_font.render(str(self.game.score), True, (255,255,255))

            screen.fill(light_grey)
            self.game.board.draw(screen)
            self.game.cur_piece.draw(screen)
            screen.blit(score_surface, (310,100))
            pygame.display.update()

            clock.tick(300)
        
        genome.fitness += self.game.score   

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        light_grey = (60,52,75)
        score_font = pygame.font.Font(None, 40)
        screen = pygame.display.set_mode((500,600))
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()
        UPDATE = pygame.USEREVENT
        pygame.time.set_timer(UPDATE, 60)

        OUTPUT = pygame.USEREVENT + 1
        pygame.time.set_timer(OUTPUT, 60)
        inc= 10
        mx=None
        maxSpeed=False
        while self.game.state != 0:

            #Select Move
            if self.game.state == 1:

                #get move and matching features
                board = [row[:] for row in self.game.board.board]
                stats, moves, boards = calculate_moves(board, self.game.cur_piece.id)
                holder = list(zip(stats,moves,boards))
                random.shuffle(holder)

                #pick best move
                for stat, move, bc in holder:
                    
                    output = net.activate(stat)
                    if mx==None or output>=mx[0]:
                        mx=[output, move, bc, stat]

                self.game.state = 2


            for event in pygame.event.get():
                if event.type == OUTPUT and self.game.state == 2:
                    
                    if mx[1][0] > 0:
                        self.game.rotate()
                        mx[1][0] -=1
                    else:

                        left_most = self.game.cur_piece.cords[0][0]
                        for i in range(1,4):
                            if self.game.cur_piece.cords[i][0] < left_most:
                                left_most = self.game.cur_piece.cords[i][0]
                    
                        if left_most < mx[1][1]:
                            self.game.right()
                        elif left_most > mx[1][1]:
                            self.game.left()
                        else:
                            self.game.state=3
                            self.game.check = mx[2]

                            mx=None
                    
                if event.type == UPDATE:
                    self.game.down()

            if not maxSpeed==False:
                newSpeed = max(30, 80-(inc/2))

                if self.game.score >= inc:
                    pygame.time.set_timer(UPDATE, newSpeed)
                    inc += 10

                if newSpeed == 30:
                    maxSpeed = True

            if self.game.score >= 700:
                self.game.state=0

            score_surface = score_font.render(str(self.game.score), True, (255,255,255))

            screen.fill(light_grey)
            self.game.board.draw(screen)
            self.game.cur_piece.draw(screen)
            screen.blit(score_surface, (310,100))
            pygame.display.update()

            clock.tick(300)

        print(self.game.score)


def eval_genomes(genomes, config):
    
    for (genome_id, genome) in genomes:
        genome.fitness = 0
        game = TetrisGame()
        game.train_ai(genome, config)

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-19')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 20)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):

    with open("best.pickle", "rb") as f:
              winner = pickle.load(f)
    game = TetrisGame()
    game.test_ai(winner, config)
              

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
    #test_ai(config)