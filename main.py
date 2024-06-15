import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
VERSION = '1.0'
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 30
SENSOR_RADIUS = 100

ANTIACCELERATE = 0.01
DELTAACCELERATE = 0.1
DELTAANGLESPEED = 1
MAXACCELERATE = 1
MAXANGLESPEED = 5

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.accelerate = 0
        self.angle_speed = 0
        self.trajectory = []
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
        if self.accelerate > DELTAACCELERATE :
            self.accelerate -= ANTIACCELERATE
        elif self.accelerate < -DELTAACCELERATE :
            self.accelerate += ANTIACCELERATE
        else:
            self.accelerate /= 2
        
        
        if self.angle_speed > DELTAANGLESPEED :
            self.angle_speed -= DELTAANGLESPEED
        elif self.angle_speed < -DELTAANGLESPEED :
            self.angle_speed += DELTAANGLESPEED
        else:
            self.angle_speed /= 2
        
        self.speed += self.accelerate
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
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius, 1)

def main():
    clock = pygame.time.Clock()
    car = Car(WIDTH // 2, HEIGHT // 2)
    sensors = [Sensor(100, 100, SENSOR_RADIUS), Sensor(700, 500, SENSOR_RADIUS)]

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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()