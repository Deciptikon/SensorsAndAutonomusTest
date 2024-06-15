import pygame
import math

# Инициализация Pygame
pygame.init()

pygame.font.init()
font = pygame.font.SysFont(None, 24)

# Константы
VERSION = '1.1'
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 30
SENSOR_RADIUS = 100


DELTAACCELERATE = 0.001
DELTAANGLESPEED = 0.01
MAXACCELERATE = 1
MAXANGLESPEED = 5

ACCURACY = 0.00001

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (100, 100, 255)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f'Simulation {VERSION}')

# Модель транспортного средства
class Car:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.accelerate = 0
        self.angle_speed = 0
        self.trajectory = []
        
        self.driving_history = [] 
        self.sensor_history = [] 
        
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        self.image.fill(BLUE)
        
        h = 5 
        w = 7
        red_rect_size = (w, h)
        pygame.draw.rect(self.image, RED, (CAR_WIDTH - w, 0, *red_rect_size))
        pygame.draw.rect(self.image, RED, (CAR_WIDTH - w, CAR_HEIGHT - h, *red_rect_size))
        pygame.draw.rect(self.image, LIGHTBLUE, (0, 0, *(2/3*CAR_WIDTH, CAR_HEIGHT)))

    def update(self):
        # Обновление позиции и угла
        
        self.accelerate *= 0.96
        
        if abs(self.accelerate) < ACCURACY :
            self.accelerate = 0
        
        
        
        self.angle_speed *= 0.99
        
        if abs(self.angle_speed) < ACCURACY :
            self.angle_speed = 0
        
        self.speed += self.accelerate
        self.speed *= 0.98
        
        if abs(self.speed) < ACCURACY :
            self.speed = 0
        if abs(self.speed) > 5 :
            if self.speed > 0 :
                self.speed = 5
            else:
                self.speed = -5
        
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.angle += self.angle_speed

        # Запоминание траектории
        self.trajectory.append((self.x, self.y))
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)

    def draw(self, screen):
        # Отрисовка траектории
        for point in self.trajectory:
            pygame.draw.circle(screen, GREEN, (int(point[0]), int(point[1])), 2)

        # Поворот машины
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))

        # Отрисовка машины
        screen.blit(rotated_image, new_rect.topleft)

    def control(self, keys):
        if keys[pygame.K_w]:
            self.accelerate += DELTAACCELERATE
        if keys[pygame.K_s]:
            self.accelerate -= DELTAACCELERATE
        #else:
            #self.speed = 0

        if keys[pygame.K_a]:
            self.angle_speed += DELTAANGLESPEED
        if keys[pygame.K_d]:
            self.angle_speed -= DELTAANGLESPEED
        #else:
           # self.angle_speed = 0

        if self.accelerate > MAXACCELERATE :
            self.accelerate = MAXACCELERATE
        if self.accelerate < -MAXACCELERATE : 
            self.accelerate = -MAXACCELERATE
        
        if self.angle_speed > MAXANGLESPEED :
            self.accelerate = MAXANGLESPEED
        if self.angle_speed < -MAXANGLESPEED :
            self.accelerate = -MAXANGLESPEED

# Виртуальный датчик
class Sensor:
    def __init__(self, x: float, y: float, radius: float, id: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.id = id

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius, 1)

def draw_text(screen, text, pos):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, pos)

def main():
    clock = pygame.time.Clock()
    car = Car(WIDTH // 2, HEIGHT // 2)
    sensors = [Sensor(100, 100, SENSOR_RADIUS, 0), Sensor(700, 500, SENSOR_RADIUS, 1)]

    running = True
    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление состояния машины
        keys = pygame.key.get_pressed()
        car.control(keys)
        car.update()

        # Отрисовка
        car.draw(screen)
        for sensor in sensors:
            sensor.draw(screen)

        # Вывод текста
        
        draw_text(screen, f'Accelerate: {car.accelerate}', (10, HEIGHT - 80))
        draw_text(screen, f'Speed: {car.speed}', (10, HEIGHT - 60))
        draw_text(screen, f'Angle speed: {car.angle_speed}', (10, HEIGHT - 40))
        draw_text(screen, f'Angle: {car.angle}', (10, HEIGHT - 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()