import sys
import os
from random import randint
from pygame import QUIT, init
import pygame
import neat


WIDTH = 800
HEIGHT = 450
GEN = 0
WIN_ON = True

pygame.init()
STAT_FONT = pygame.font.SysFont("arial sans serif", 40)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong AI")

class Paddle:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = 0
        self.color = color
        self.width = 5
        self.height = HEIGHT/10
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.height)

    def move_up(self):
        self.vel = -5

    def move_down(self):
        self.vel = 5

    def move_stop(self):
        self.vel = 0

    def move(self):
        if self.rect.top <= 0 and self.vel < 0:
            self.vel = 0
        elif self.rect.bottom >= HEIGHT and self.vel > 0:
            self.vel = 0

        self.rect = self.rect.move([0,self.vel])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_y(self):
        return self.rect.y

    def get_x(self):
        return self.rect.x

class Ball:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = [random_sign()*4,random_sign()*4]
        self.color = color
        self.width = 10
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.width)

    def change_vel_y(self):
        self.vel[1] = -self.vel[1]

    def change_vel_x(self):
        self.vel[0] = -self.vel[0]

    def move(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.change_vel_y()
        self.rect = self.rect.move([self.vel[0],self.vel[1]])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def collide(self, paddle):
        return self.rect.colliderect(paddle)

def draw_window(screen, paddles, paddles_r, balls):
    screen.fill((0,0,0))
    for ball in balls:
        ball.draw(screen)
    for paddle in paddles:
        paddle.draw(screen)
    for paddle in paddles_r:
        paddle.draw(screen)
    score_label = STAT_FONT.render("Gens: " + str(GEN-1),1,(255,255,255))
    screen.blit(score_label, (WIDTH/2-50, 10))
    pygame.display.flip()

def random_sign():
    i = randint(0,1)
    if i == 0:
        return -1
    return 1

def eval_genomes(genomes, config):
    global GEN
    global WIN_ON
    GEN += 1
    score = 0
    paddles = []
    paddles_r = []
    balls = []
    nets = [] 
    ge = []  
    for _,g in genomes:
        tmp_color = (randint(100,255),randint(100,255),randint(100,255))
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        paddles.append(Paddle(20,240,tmp_color))
        paddles_r.append(Paddle(WIDTH-25,240,tmp_color))
        balls.append(Ball(randint(100,255),randint(100,255),tmp_color))
        g.fitness = 0
        ge.append(g)
    clock = pygame.time.Clock()
    run = True
    while run and len(paddles) > 0:
        if WIN_ON: clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                sys.exit()
                break
        for x_c, paddle in enumerate(paddles):
            
            ge[x_c].fitness += 0.05
            paddle.move()
            outputs = nets[paddles.index(paddle)].activate((paddle.get_y(),
                                    abs(paddle.get_x() - balls[paddles.index(paddle)].rect.x),
                                    balls[paddles.index(paddle)].rect.y))

            if outputs[0] > outputs[1]:
                if outputs[0] > 0.5:
                    paddle.move_up()
                else:
                    paddle.move_stop()
            elif outputs[1] > 0.5:
                paddle.move_down()
            else:
                paddle.move_stop()
        
        for x_c, paddle in enumerate(paddles_r):
            
            ge[x_c].fitness += 0.05
            paddle.move()

            outputs = nets[paddles_r.index(paddle)].activate((paddle.get_y(),
                            abs(paddle.get_x() - balls[paddles_r.index(paddle)].rect.x),
                            balls[paddles_r.index(paddle)].rect.y))

            if outputs[0] > outputs[1]:
                if outputs[0] > 0.5:
                    paddle.move_up()
                else:
                    paddle.move_stop()
            elif outputs[1] > 0.5:
                paddle.move_down()
            else:
                paddle.move_stop()

        
        for ball in balls:
            if ball.collide(paddles[balls.index(ball)]):
                ball.change_vel_x()
                ge[balls.index(ball)].fitness += 5
                score += 1
            if ball.collide(paddles_r[balls.index(ball)]):
                ball.change_vel_x()
                ge[balls.index(ball)].fitness += 5
                score += 1
            ball.move()
            if ball.get_x() < 0 or ball.get_x() > WIDTH:
                
                ge[balls.index(ball)].fitness -= 2
                nets.pop(balls.index(ball))
                ge.pop(balls.index(ball))
                paddles.pop(balls.index(ball))
                paddles_r.pop(balls.index(ball))
                balls.pop(balls.index(ball))
        if WIN_ON:
            draw_window(screen, paddles, paddles_r, balls)
        if score > 500:
            break

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 1000)
    print('\nBest genome:\n{!s}'.format(winner))
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)