import pygame
from random import randint
from copy import deepcopy
import pygame as pg

class Game:
    def __init__(self, width, height, tile_size, fps): #Инициализация игры. Указываем ширину,высоту,размер клетки,fps игры.
        self.WIDTH = width
        self.HEIGHT = height
        self.TILE = tile_size
        self.W = self.WIDTH // self.TILE
        self.H = self.HEIGHT // self.TILE
        self.FPS = fps
        self.drawing = False
        self.delete_cells = False
        pygame.init()
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Of Life")  # Устанавливаем заголовок окна
        self.clock = pygame.time.Clock()
        self.start_game = False
        self.next_field = [[0 for _ in range(self.W)] for _ in range(self.H)]
        #self.current_field = [[randint(0, 1) for _ in range(self.W)] for _ in range(self.H)]
        #self.current_field = [[i % 13 == 0 for i in range(self.W)] for _ in range(self.H)]
        self.current_field= [[0 for _ in range(self.W)] for _ in range(self.H)]
        pygame.font.init()
        self.font = pygame.font.Font('GraverplateRegular.ttf', 72)  # Загружаем шрифт для отображения текста

    def check_cell(self, x, y):#Функция игры, которая проверяет количество живых клеток вокруг определенной клетки
        count = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if self.current_field[i][j] == 1:
                    count += 1
        if self.current_field[y][x]:
            count -= 1
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

    '''
    def run(self):#Функция игры
        while True:
            self.surface.fill(pygame.Color('black'))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():#Проверка и обработка всевозможных событий в игре
                if event.type == pygame.QUIT:
                    exit()
                if keys[pygame.K_q]:
                    self.display_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:#Рисовка клеток
                    if event.button == 1: # Левая кнопка мыши
                        self.drawing = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.drawing = False

                if event.type == pygame.MOUSEBUTTONDOWN:#Удаление клеток
                    if event.button == 3: # Правая кнопка мыши
                        self.delete_cells = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.delete_cells = False

                if keys[pygame.K_SPACE]:#После нажатия клавиши Пробел - игра запускается
                    self.start_game = True
                if keys[pygame.K_r]:#Перезапуск игры
                    self.start_game = False
                    self.current_field = [[0 for _ in range(self.W)] for _ in range(self.H)]
                    self.current_field = [[0 for _ in range(self.W)] for _ in range(self.H)]
                if self.drawing and event.type == pygame.MOUSEMOTION:#Зарисовка клеток,которые мы указали
                    x, y = event.pos
                    x //= self.TILE
                    y //= self.TILE
                    if 0 <= x < self.W and 0 <= y < self.H:
                        self.current_field[y][x] = 1
                if self.delete_cells and event.type == pygame.MOUSEMOTION:#Удаление клеток,которые мы указали
                    x, y = event.pos
                    x //= self.TILE
                    y //= self.TILE
                    if 0 <= x < self.W and 0 <= y < self.H:
                        self.current_field[y][x] = 0
            [pygame.draw.line(self.surface, pygame.Color('grey'), (x, 0), (x, self.HEIGHT)) for x in
             range(0, self.WIDTH, self.TILE)]#Образуем сетку на экране
            [pygame.draw.line(self.surface, pygame.Color('grey'), (0, y), (self.WIDTH, y)) for y in
             range(0, self.HEIGHT, self.TILE)]

            for x in range(1, self.W - 1):
                for y in range(1, self.H - 1):
                    if self.current_field[y][x]:#Если клетка живая,то мы зарисовываем данную клетку зелёным
                        pygame.draw.rect(self.surface, pygame.Color('forestgreen'),
                                         (x * self.TILE + 2, y * self.TILE + 2, self.TILE - 2, self.TILE - 2))
                    self.next_field[y][x] = self.check_cell(x, y)

            if self.start_game:
                self.current_field = deepcopy(self.next_field)
            print(round(self.clock.get_fps(),2))
            pygame.display.flip()
            self.clock.tick(self.FPS)
        '''

    def run(self):#Функция игры
        while True:
            self.surface.fill(pygame.Color('black'))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if keys[pygame.K_q]:
                    self.display_menu()

                self.handle_mouse_events(event)

                if keys[pygame.K_SPACE]:
                    self.start_game = True

                if keys[pygame.K_r]:
                    self.reset_game()

            self.draw_grid()

            for x in range(1, self.W - 1):
                for y in range(1, self.H - 1):
                    self.draw_cell(x, y)

            if self.start_game:
                self.current_field = deepcopy(self.next_field)

            print(round(self.clock.get_fps(), 2))
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def handle_mouse_events(self, event):#отслеживание действий мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.drawing = True
            elif event.button == 3:
                self.delete_cells = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
            elif event.button == 3:
                self.delete_cells = False

        elif (self.drawing or self.delete_cells) and event.type == pygame.MOUSEMOTION:
            self.draw_or_delete_cells(event)

    def draw_or_delete_cells(self, event):#Функция,в которой мы будем закрашивать или удалять клетки в зависимости от того
        #какой клавишей мыши мы нажимали на клетку
        x, y = event.pos
        x //= self.TILE
        y //= self.TILE
        if 0 <= x < self.W and 0 <= y < self.H:
            self.current_field[y][x] = 1 if self.drawing else 0

    def reset_game(self):#Функция,которая делает рестарт игры
        self.start_game = False
        self.current_field = [[0 for _ in range(self.W)] for _ in range(self.H)]
        self.next_field = [[0 for _ in range(self.W)] for _ in range(self.H)]

    def draw_cell(self, x, y):#Функция отрисовки клеток на игровом поле
        if self.current_field[y][x]:
            pygame.draw.rect(self.surface, pygame.Color('forestgreen'),
                             (x * self.TILE + 2, y * self.TILE + 2, self.TILE - 2, self.TILE - 2))
        self.next_field[y][x] = self.check_cell(x, y)

    def draw_grid(self):#Функция отрисовки сетки
        [pygame.draw.line(self.surface, pygame.Color('grey'), (x, 0), (x, self.HEIGHT)) for x in
         range(0, self.WIDTH, self.TILE)]
        [pygame.draw.line(self.surface, pygame.Color('grey'), (0, y), (self.WIDTH, y)) for y in
         range(0, self.HEIGHT, self.TILE)]

    def display_menu(self):#Функция главного меню
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Проверяем, нажата ли клавиша Enter (K_RETURN)
                self.run()
            menu_items = [("Game Of Life", (self.WIDTH // 2, 100)),
                          ("Play", (self.WIDTH // 2, 500)),
                          ("Settings", (self.WIDTH // 2, 600))]

            for text, position in menu_items:
                text_surface = self.font.render(text, True, pygame.Color('green'))
                text_rect = text_surface.get_rect(center=position)
                self.surface.blit(text_surface, text_rect)

            pygame.display.update()
