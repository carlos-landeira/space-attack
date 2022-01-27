import pygame
from pygame import mixer
import os
import time
import random
import sys
pygame.font.init()


def game():
        
    inimigo1 = pygame.image.load(os.path.join("imagens", "atomictraveler.png"))
    inimigo2 = pygame.image.load(os.path.join("imagens", "suitstruggler.png"))

    jogador1 = pygame.image.load(os.path.join("imagens", "CenturiumEagle.png"))
    jogador2 = pygame.image.load(os.path.join("imagens", "BearBeets.png"))
    jogador3 = pygame.image.load(os.path.join("imagens", "CentenaryScout.png"))

    tiro1 = pygame.image.load(os.path.join("imagens", "projatomic.png"))
    tiro2 = pygame.image.load(os.path.join("imagens", "projsuit.png"))
    tiro3 = pygame.image.load(os.path.join("imagens", "projeagle.png"))
    tiro4 = pygame.image.load(os.path.join("imagens", "projbeets.png"))

    class Projetil:
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            self.y += vel

        def off_screen(self, height):
            return not(self.y <= height and self.y >= 0)

        def colisao(self, obj):
            return colidir(self, obj)


    class Nave:
        COOLDOWN = 30

        def __init__(self, x, y, vida=100):
            self.x = x
            self.y = y
            self.vida = vida
            self.img_nave = None
            self.projetil_img = None
            self.projeteis = []
            self.cool_down = 0

        def draw(self, window):
            window.blit(self.img_nave, (self.x, self.y))
            for projetil in self.projeteis:
                projetil.draw(window)

        def move_projeteis(self, vel, obj):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                elif projetil.colisao(obj):
                    obj.vida -= 10
                    self.projeteis.remove(projetil)

        def cooldown(self):
            if self.cool_down >= self.COOLDOWN:
                self.cool_down = 0
            elif self.cool_down > 0:
                self.cool_down += 1

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1

        def get_width(self):
            return self.img_nave.get_width()

        def get_height(self):
            return self.img_nave.get_height()


    class Player1(Nave):

        def __init__(self, x, y, vida=100):
            super().__init__(x, y, vida)
            self.img_nave = jogador1
            self.projetil_img = tiro3
            self.mask = pygame.mask.from_surface(self.img_nave)
            self.max_vida = vida

        def move_projeteis(self, vel, objs):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                else:
                    for obj in objs:
                        if projetil.colisao(obj):
                            objs.remove(obj)
                            if projetil in self.projeteis:
                                self.projeteis.remove(projetil)

        def draw(self, window):
            super().draw(window)
            self.barra_vida(window)

        def barra_vida(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width() * (self.vida/self.max_vida), 10))    

    class Inimigo(Nave):
        COLOR_MAP = {
                    "red": (inimigo1, tiro1),
                    "green": (inimigo2, tiro2)
                    }

        def __init__(self, x, y, color, vida=100):
            super().__init__(x, y, vida)
            self.img_nave, self.projetil_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.img_nave)

        def move(self, vel):
            self.y += vel

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x-20, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1


    def colidir(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
        

    def main():
        run = True
        FPS = 60
        level = 0
        vidas = 5
        main_font = pygame.font.SysFont("comicsans", 50)
        fonte_perdeu = pygame.font.SysFont("comicsans", 60)

        inimigos = []
        onda_inimiga = 5
        inimigo_vel = 1
        player_vel = 5
        projetil_vel = 5
        player = Player1(300, 630)

        clock = pygame.time.Clock()

        perdeu = False
        contar_perdas = 0

        def redraw_window():
            WIN.blit(BG, (0,0))

            for inimigo in inimigos:
                inimigo.draw(WIN)

            player.draw(WIN)

            if perdeu:
                frase_perdeu = fonte_perdeu.render("Você Perdeu!!", 1, (255,255,255))
                WIN.blit(frase_perdeu, (WIDTH/2 - frase_perdeu.get_width()/2, 350))

            pygame.display.update()

        while run:
            clock.tick(FPS)
            redraw_window()

            if vidas <= 0 or player.vida <= 0:
                perdeu = True
                contar_perdas += 1
            if perdeu:
                if contar_perdas > FPS * 3:
                    run = False
                else:
                    continue
            if len(inimigos) == 0:
                level += 1
                onda_inimiga += 5
                for i in range(onda_inimiga):
                    inimigo = Inimigo(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green"]))
                    inimigos.append(inimigo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0: # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
                player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0: # up
                player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
                player.y += player_vel
            if keys[pygame.K_SPACE]:
                somtiro = mixer.Sound("projetil.wav")
                somtiro.play()
                player.atirar()

            for inimigo in inimigos[:]:
                inimigo.move(inimigo_vel)
                inimigo.move_projeteis(projetil_vel, player)

                if random.randrange(0, 2*60) == 1:
                    inimigo.atirar()
                if inimigo in inimigos[:] == False:
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()  
                elif colidir(inimigo, player):
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()
                    player.vida -= 10
                    inimigos.remove(inimigo)
                elif inimigo.y + inimigo.get_height() > HEIGHT:
                    vidas -= 1
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()

            player.move_projeteis(-projetil_vel, inimigos)
    
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.set_caption('Menu Principal')

    pygame.display.update()
    mainClock.tick(60)
    
    running = True              
    while running:
        title_font = pygame.font.SysFont("comicsans", 70)
        screen.fill((0,0,0))
        pygame.display.set_caption('Jogo')
        WIDTH, HEIGHT = 920, 840
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        BG = pygame.transform.scale(pygame.image.load(os.path.join("imagens", "background.png")), (WIDTH, HEIGHT))
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Pressione seu mouse para iniciar", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()


def game2():

    inimigo1 = pygame.image.load(os.path.join("imagens", "atomictraveler.png"))
    inimigo2 = pygame.image.load(os.path.join("imagens", "suitstruggler.png"))

    jogador1 = pygame.image.load(os.path.join("imagens", "CenturiumEagle.png"))
    jogador2 = pygame.image.load(os.path.join("imagens", "BearBeets.png"))
    jogador3 = pygame.image.load(os.path.join("imagens", "CentenaryScout.png"))

    tiro1 = pygame.image.load(os.path.join("imagens", "projatomic.png"))
    tiro2 = pygame.image.load(os.path.join("imagens", "projsuit.png"))
    tiro3 = pygame.image.load(os.path.join("imagens", "projeagle.png"))
    tiro4 = pygame.image.load(os.path.join("imagens", "projbeets.png"))

    class Projetil:
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            self.y += vel

        def off_screen(self, height):
            return not(self.y <= height and self.y >= 0)

        def colisao(self, obj):
            return colidir(self, obj)


    class Nave:
        COOLDOWN = 30

        def __init__(self, x, y, vida=100):
            self.x = x
            self.y = y
            self.vida = vida
            self.img_nave = None
            self.projetil_img = None
            self.projeteis = []
            self.cool_down = 0

        def draw(self, window):
            window.blit(self.img_nave, (self.x, self.y))
            for projetil in self.projeteis:
                projetil.draw(window)

        def move_projeteis(self, vel, obj):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                elif projetil.colisao(obj):
                    obj.vida -= 10
                    self.projeteis.remove(projetil)

        def cooldown(self):
            if self.cool_down >= self.COOLDOWN:
                self.cool_down = 0
            elif self.cool_down > 0:
                self.cool_down += 1

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1

        def get_width(self):
            return self.img_nave.get_width()

        def get_height(self):
            return self.img_nave.get_height()


    class Player2(Nave):

        def __init__(self, x, y, vida=100):
            super().__init__(x, y, vida)
            self.img_nave = jogador2
            self.projetil_img = tiro4
            self.mask = pygame.mask.from_surface(self.img_nave)
            self.max_vida = vida

        def move_projeteis(self, vel, objs):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                else:
                    for obj in objs:
                        if projetil.colisao(obj):
                            objs.remove(obj)
                            if projetil in self.projeteis:
                                self.projeteis.remove(projetil)

        def draw(self, window):
            super().draw(window)
            self.barra_vida(window)

        def barra_vida(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width() * (self.vida/self.max_vida), 10))

    class Inimigo(Nave):
        COLOR_MAP = {
                    "red": (inimigo1, tiro1),
                    "green": (inimigo2, tiro2)
                    }

        def __init__(self, x, y, color, vida=100):
            super().__init__(x, y, vida)
            self.img_nave, self.projetil_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.img_nave)

        def move(self, vel):
            self.y += vel

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x-20, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1


    def colidir(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
        

    def main():
        run = True
        FPS = 60
        level = 0
        vidas = 5
        main_font = pygame.font.SysFont("comicsans", 50)
        fonte_perdeu = pygame.font.SysFont("comicsans", 60)

        inimigos = []
        onda_inimiga = 5
        inimigo_vel = 1
        player_vel = 5
        projetil_vel = 5
        player = Player2(300, 630)

        clock = pygame.time.Clock()

        perdeu = False
        contar_perdas = 0

        def redraw_window():
            WIN.blit(BG, (0,0))

            for inimigo in inimigos:
                inimigo.draw(WIN)

            player.draw(WIN)

            if perdeu:
                frase_perdeu = fonte_perdeu.render("Você Perdeu!!", 1, (255,255,255))
                WIN.blit(frase_perdeu, (WIDTH/2 - frase_perdeu.get_width()/2, 350))

            pygame.display.update()

        while run:
            clock.tick(FPS)
            redraw_window()

            if vidas <= 0 or player.vida <= 0:
                perdeu = True
                contar_perdas += 1
            if perdeu:
                if contar_perdas > FPS * 3:
                    run = False
                else:
                    continue
            if len(inimigos) == 0:
                level += 1
                onda_inimiga += 5
                for i in range(onda_inimiga):
                    inimigo = Inimigo(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green"]))
                    inimigos.append(inimigo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0: # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
                player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0: # up
                player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
                player.y += player_vel
            if keys[pygame.K_SPACE]:
                somtiro = mixer.Sound("projetil.wav")
                somtiro.play()
                player.atirar()

            for inimigo in inimigos[:]:
                inimigo.move(inimigo_vel)
                inimigo.move_projeteis(projetil_vel, player)

                if random.randrange(0, 2*60) == 1:
                    inimigo.atirar()
                if inimigo in inimigos[:] == False:
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()  
                elif colidir(inimigo, player):
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()
                    player.vida -= 10
                    inimigos.remove(inimigo)
                elif inimigo.y + inimigo.get_height() > HEIGHT:
                    vidas -= 1
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()

            player.move_projeteis(-projetil_vel, inimigos)
    
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.set_caption('Menu Principal')

    pygame.display.update()
    mainClock.tick(60)
    
    running = True              
    while running:
        title_font = pygame.font.SysFont("comicsans", 70)
        screen.fill((0,0,0))
        pygame.display.set_caption('Jogo')
        WIDTH, HEIGHT = 920, 840
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        BG = pygame.transform.scale(pygame.image.load(os.path.join("imagens", "background.png")), (WIDTH, HEIGHT))
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Pressione seu mouse para iniciar", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()


def game3():


    inimigo1 = pygame.image.load(os.path.join("imagens", "atomictraveler.png"))
    inimigo2 = pygame.image.load(os.path.join("imagens", "suitstruggler.png"))

    jogador1 = pygame.image.load(os.path.join("imagens", "CenturiumEagle.png"))
    jogador2 = pygame.image.load(os.path.join("imagens", "BearBeets.png"))
    jogador3 = pygame.image.load(os.path.join("imagens", "CentenaryScout.png"))

    tiro1 = pygame.image.load(os.path.join("imagens", "projatomic.png"))
    tiro2 = pygame.image.load(os.path.join("imagens", "projsuit.png"))
    tiro3 = pygame.image.load(os.path.join("imagens", "projeagle.png"))
    tiro4 = pygame.image.load(os.path.join("imagens", "projbeets.png"))

    class Projetil:
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            self.y += vel

        def off_screen(self, height):
            return not(self.y <= height and self.y >= 0)

        def colisao(self, obj):
            return colidir(self, obj)


    class Nave:
        COOLDOWN = 30

        def __init__(self, x, y, vida=100):
            self.x = x
            self.y = y
            self.vida = vida
            self.img_nave = None
            self.projetil_img = None
            self.projeteis = []
            self.cool_down = 0

        def draw(self, window):
            window.blit(self.img_nave, (self.x, self.y))
            for projetil in self.projeteis:
                projetil.draw(window)

        def move_projeteis(self, vel, obj):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                elif projetil.colisao(obj):
                    obj.vida -= 10
                    self.projeteis.remove(projetil)

        def cooldown(self):
            if self.cool_down >= self.COOLDOWN:
                self.cool_down = 0
            elif self.cool_down > 0:
                self.cool_down += 1

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1

        def get_width(self):
            return self.img_nave.get_width()

        def get_height(self):
            return self.img_nave.get_height()


    class Player3(Nave):

        def __init__(self, x, y, vida=100):
            super().__init__(x, y, vida)
            self.img_nave = jogador3
            self.projetil_img = tiro4
            self.mask = pygame.mask.from_surface(self.img_nave)
            self.max_vida = vida

        def move_projeteis(self, vel, objs):
            self.cooldown()
            for projetil in self.projeteis:
                projetil.move(vel)
                if projetil.off_screen(HEIGHT):
                    self.projeteis.remove(projetil)
                else:
                    for obj in objs:
                        if projetil.colisao(obj):
                            objs.remove(obj)
                            if projetil in self.projeteis:
                                self.projeteis.remove(projetil)

        def draw(self, window):
            super().draw(window)
            self.barra_vida(window)

        def barra_vida(self, window):
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width() * (self.vida/self.max_vida), 10))    

    class Inimigo(Nave):
        COLOR_MAP = {
                    "red": (inimigo1, tiro1),
                    "green": (inimigo2, tiro2)
                    }

        def __init__(self, x, y, color, vida=100):
            super().__init__(x, y, vida)
            self.img_nave, self.projetil_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.img_nave)

        def move(self, vel):
            self.y += vel

        def atirar(self):
            if self.cool_down == 0:
                projetil = Projetil(self.x-20, self.y, self.projetil_img)
                self.projeteis.append(projetil)
                self.cool_down = 1


    def colidir(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
        

    def main():
        run = True
        FPS = 60
        level = 0
        vidas = 5
        main_font = pygame.font.SysFont("comicsans", 50)
        fonte_perdeu = pygame.font.SysFont("comicsans", 60)

        inimigos = []
        onda_inimiga = 5
        inimigo_vel = 1
        player_vel = 5
        projetil_vel = 5
        player = Player3(300, 630)

        clock = pygame.time.Clock()

        perdeu = False
        contar_perdas = 0

        def redraw_window():
            WIN.blit(BG, (0,0))

            for inimigo in inimigos:
                inimigo.draw(WIN)

            player.draw(WIN)

            if perdeu:
                frase_perdeu = fonte_perdeu.render("Você Perdeu!!", 1, (255,255,255))
                WIN.blit(frase_perdeu, (WIDTH/2 - frase_perdeu.get_width()/2, 350))

            pygame.display.update()

        while run:
            clock.tick(FPS)
            redraw_window()

            if vidas <= 0 or player.vida <= 0:
                perdeu = True
                contar_perdas += 1
            if perdeu:
                if contar_perdas > FPS * 3:
                    run = False
                else:
                    continue
            if len(inimigos) == 0:
                level += 1
                onda_inimiga += 5
                for i in range(onda_inimiga):
                    inimigo = Inimigo(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green"]))
                    inimigos.append(inimigo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0: # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
                player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0: # up
                player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
                player.y += player_vel
            if keys[pygame.K_SPACE]:
                somtiro = mixer.Sound("projetil.wav")
                somtiro.play()
                player.atirar()

            for inimigo in inimigos[:]:
                inimigo.move(inimigo_vel)
                inimigo.move_projeteis(projetil_vel, player)

                if random.randrange(0, 2*60) == 1:
                    inimigo.atirar()
                if inimigo in inimigos[:] == False:
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()  
                elif colidir(inimigo, player):
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()
                    player.vida -= 10
                    inimigos.remove(inimigo)
                elif inimigo.y + inimigo.get_height() > HEIGHT:
                    vidas -= 1
                    inimigos.remove(inimigo)
                    somcolisao = mixer.Sound("explosao.wav")
                    somcolisao.play()

            player.move_projeteis(-projetil_vel, inimigos)
    
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.set_caption('Menu Principal')

    pygame.display.update()
    mainClock.tick(60)
    
    running = True              
    while running:
        title_font = pygame.font.SysFont("comicsans", 70)
        screen.fill((0,0,0))
        pygame.display.set_caption('Jogo')
        WIDTH, HEIGHT = 920, 840
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        BG = pygame.transform.scale(pygame.image.load(os.path.join("imagens", "background.png")), (WIDTH, HEIGHT))
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Pressione seu mouse para iniciar", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

def selecao():

    pygame.init()
    mainClock = pygame.time.Clock()
    W = 500
    H = 500

    superficie = pygame.display.set_mode((W,H), 0, 32)
    pygame.display.set_caption('Seleção de Nave')
    centurium = pygame.image.load(os.path.join('imagens','CenturiumEagle.png'))
    bear = pygame.image.load(os.path.join('imagens','BearBeets.png'))
    centenary = pygame.image.load(os.path.join('imagens','CentenaryScout.png'))

    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    jogo = True
    mouse_pos = (0,0)
    mouse_click = (0,0)
    text1_bool = False
    text2_bool = False
    text3_bool = False
    text4_bool = False
    tecla = pygame.key.get_pressed()

    while jogo == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
            if event.type == MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == MOUSEBUTTONUP:
                mouse_click = event.pos

        superficie.fill(BLACK)
        color = WHITE

        Font = pygame.font.SysFont('comicsans', 50)
        text = Font.render('SELECIONE SUA NAVE',True,color)
        text_rect = text.get_rect()
        text_rect.center = (250,30)
        superficie.blit(text, text_rect)

        Font = pygame.font.SysFont('comicsans', 40)
        if text1_bool:
            color = RED
        text = Font.render('Centurium Eagle',True,color)
        superficie.blit(centurium, (350,70))
        text_rect = text.get_rect()
        text_rect.center = (250,130)
        if text_rect.collidepoint(mouse_click):
            game()
        if text_rect.collidepoint(mouse_pos):
            text1_bool = True
        else:
            text1_bool = False
        superficie.blit(text, text_rect)

        color = WHITE
        if text2_bool:
            color = RED
        
        Font = pygame.font.SysFont('comicsans', 40)
        text = Font.render('Bear Beets',True,color)
        superficie.blit(bear, (310,180))
        text_rect = text.get_rect()
        text_rect.center = (250,230)
        if text_rect.collidepoint(mouse_click):
            game2()
        if text_rect.collidepoint(mouse_pos):
            text2_bool = True
        else:
            text2_bool = False
        superficie.blit(text, text_rect)

        color = WHITE
        if text3_bool:
            color = RED
        
        Font = pygame.font.SysFont('comicsans', 40)
        text = Font.render('Centenary Scout',True,color)
        superficie.blit(centenary, (370,300))
        text_rect = text.get_rect()
        text_rect.center = (250,330)
        if text_rect.collidepoint(mouse_click):
            game3()
        if text_rect.collidepoint(mouse_pos):
            text3_bool = True
        else:
            text3_bool = False
        superficie.blit(text, text_rect)

        pygame.display.flip()
        mainClock.tick(100000)

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Menu Principal')
screen = pygame.display.set_mode((500, 500),0,32)

font = pygame.font.SysFont(None, 24)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def options():
    running = True
    while running:
        screen.fill((0,0,0))
        pygame.display.set_caption('Controles')
 
        draw_text('W - Mover para frente', font, (255, 255, 255), screen, 150, 150)
        draw_text('A - Mover para esquerda', font, (255, 255, 255), screen, 150, 180)
        draw_text('S - Mover para trás', font, (255, 255, 255), screen, 150, 210)
        draw_text('D - Mover para direita', font, (255, 255, 255), screen, 150, 240)
        draw_text('Espaço - Atirar', font, (255, 255, 255), screen, 150, 270)
        draw_text('ESC - Voltar para o menu principal', font, (255, 255, 255), screen, 150, 300)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.set_caption('Menu Principal')
        
        pygame.display.update()
        mainClock.tick(60)

def main_menu():
    while True:
 
        screen.fill((0,0,0))
        draw_text('Space Attack', font, (255, 255, 255), screen, 190, 50)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(150, 150, 200, 50)
        button_2 = pygame.Rect(150, 250, 200, 50)
        if button_1.collidepoint((mx, my)):
            title_font = pygame.font.SysFont("comicsans", 70)
            run = True
            if click:
                selecao()
                pygame.quit()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (96, 96, 96), button_1)
        pygame.draw.rect(screen, (96, 96, 96), button_2)
        screen.blit(font.render('Jogar', True, (255, 255, 255)), (228, 168))
        screen.blit(font.render('Controles', True, (255, 255, 255)), (213, 268))
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)


main_menu()