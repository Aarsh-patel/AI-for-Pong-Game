BAT_A = BAT(WHITE, 10, 100)
BAT_A.rect.x = 20
BAT_A.rect.y = 200

BAT_B = BAT(WHITE, 10 , 100)
BAT_B.rect.x = 770
BAT_B.rect.y = 200

ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
SA = 0
SB = 0
SPRITE = pygame.sprite.Group()
SPRITE.add(BAT_A)
SPRITE.add(BAT_B)
SPRITE.add(ball)
run=True

def main(genomes, config):
    
    global generation, SCREEN 
    screen = SCREEN
    generation += 1 
    
    score = 0     
    models_list = [] 
    genomes_list = [] 
    bat_list = [] 
    
    for genome_id, genome in genomes: 
        bat_list.append(BAT(20,200))
        genome.fitness = 0 
        genomes_list.append(genome) 
        model = neat.nn.FeedForwardNetwork.create(genome, config) 
        models_list.append(model)
    run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a=False
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     BAT_A.moveUp(5)
    # if keys[pygame.K_s]:
    #     BAT_A.moveDown(5)
    # if keys[pygame.K_UP]:
    #     BAT_B.moveUp(5)
    # if keys[pygame.K_DOWN]:
    #     BAT_B.moveDown(5)
    
    if ball.rect.x < 400 and ball.velocity[0]<0:
        BAT_A.cheat(ball)
    # elif ball.rect.x > 400 and ball.velocity[0]>0:    
    #     BAT_B.cheat(ball)
    if SA > 10:
        run = False
    elif SB > 10:
        run = False
    if ball.rect.x>=800:
        ball.velocity[0] = -ball.velocity[0]
        SA+=1
        BAT_A.reset()
        BAT_B.reset()
        ball.reset()
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
        SB+=1
        BAT_A.reset()
        BAT_B.reset()
        ball.reset()
    if ball.rect.y>450:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1] 
    if pygame.sprite.collide_mask(ball, BAT_A) or pygame.sprite.collide_mask(ball, BAT_B):
      ball.bounce()
    SPRITE.update()
    screen.fill(BLACK)
    SPRITE.draw(screen) 
    pygame.draw.line(screen, WHITE, [400, 0], [400, 450], 1)
    font = pygame.font.Font(None, 74)
    text = font.render(str(SA), 1, WHITE)
    screen.blit(text, (200,10))
    text = font.render(str(SB), 1, WHITE)
    screen.blit(text, (600,10))
    pygame.display.update()
    CLOCK.tick(60)
pygame.quit
