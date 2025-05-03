import pygame
import random

# Путь к изображениям указан жестко, без использования os
IMAGE_DIR = './'

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
        super().__init__()
        try:
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except Exception as e:
            print(f"Ошибка при загрузке изображения '{filename}': {e}")
            raise SystemExit(e)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(GameSprite):
    def __init__(self, filename, x, y, width, height, speed=7):
        super().__init__(filename, x, y, width, height)
        self.speed = speed

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, filename, x, y, width, height, speed=7):
        super().__init__(filename, x, y, width, height)
        self.speed = speed

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, filename, x, y, width, height, speed=5):
        super().__init__(filename, x, y, width, height)
        self.speed_x = random.choice([-speed, speed])
        self.speed_y = random.choice([-speed, speed])

    def update(self):
        # Отскок от верхнего и нижнего краев
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            
        # Перенос мяча обратно в центр при выходе за экран
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.reset()

        # Перемещаем мяч
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()
        self.background_img = pygame.image.load(IMAGE_DIR + 'background.jpg').convert()
        self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
        self.score_player1 = 0
        self.score_player2 = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)

        # Создаем объекты
        self.player1 = Player(IMAGE_DIR + 'player.png', 50, HEIGHT//5, 100, 200)
        self.enemy = Enemy(IMAGE_DIR + 'enemy.png', WIDTH - 150 - 10, HEIGHT//5, 100, 200)
        self.ball = Ball(IMAGE_DIR + 'ball.png', WIDTH//2, HEIGHT//5, 50, 50)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            keys = pygame.key.get_pressed()
            self.player1.update(keys)
            self.enemy.update(keys)
            self.ball.update()

            # Проверяем столкновения мяча с ракетками
            if pygame.sprite.collide_rect(self.ball, self.player1):
                self.ball.speed_x *= -1
            if pygame.sprite.collide_rect(self.ball, self.enemy):
                self.ball.speed_x *= -1

            # Очки игрокам
            if self.ball.rect.left < 0:
                self.increment_score(2)
            elif self.ball.rect.right > WIDTH:
                self.increment_score(1)

            # Проверка окончания игры
            if max(self.score_player1, self.score_player2) >= 10:
                self.show_game_over_screen()
                return

            # Фоновая картинка
            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.enemy.image, self.enemy.rect)
            self.screen.blit(self.ball.image, self.ball.rect)

            # Показываем счёт
            scores_text = f"{self.score_player1}:{self.score_player2}"
            scores_surface = self.font.render(scores_text, True, (255, 255, 255))
            self.screen.blit(scores_surface, ((WIDTH-scores_surface.get_width())//2, 10))

            pygame.display.flip()
            self.clock.tick(60)

    def increment_score(self, player_number):
        if player_number == 1:
            self.score_player1 += 1
        else:
            self.score_player2 += 1

    def show_game_over_screen(self):
        winner_message = "You Win!" if self.score_player1 > self.score_player2 else "You Lose!"
        text_surface = self.game_over_font.render(winner_message, True, (255, 0, 0))
        self.screen.blit(text_surface, ((WIDTH-text_surface.get_width())//2, (HEIGHT-text_surface.get_height())//2))
        pygame.display.flip()
        pygame.time.wait(3000)

# Запуск игры
WIDTH, HEIGHT = 800, 600
game_manager = GameManager()
game_manager.run_game()
pygame.quit()