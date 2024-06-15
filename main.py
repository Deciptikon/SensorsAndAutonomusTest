import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
VERSION = '1.0'
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 30
SENSOR_RADIUS = 100

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
        self.angle_speed = 0
        self.trajectory = []

    def update(self):
        # Обновление позиции и угла
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

        # Отрисовка машины
        car_rect = pygame.Rect(0, 0, CAR_WIDTH, CAR_HEIGHT)
        car_rect.center = (self.x, self.y)
        rotated_car = pygame.transform.rotate(pygame.Surface((CAR_WIDTH, CAR_HEIGHT)), self.angle)
        rotated_car.fill(BLUE)
        screen.blit(rotated_car, rotated_car.get_rect(center=car_rect.center))

    def control(self, keys):
        if keys[pygame.K_w]:
            self.speed = 5
        elif keys[pygame.K_s]:
            self.speed = -5
        else:
            self.speed = 0

        if keys[pygame.K_a]:
            self.angle_speed = 5
        elif keys[pygame.K_d]:
            self.angle_speed = -5
        else:
            self.angle_speed = 0

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