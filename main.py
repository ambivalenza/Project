import os
import random
import sys
import time

import pygame
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QComboBox, QWidget, QApplication, QPushButton, QLabel

from leadertable import Ui_Dialog, DB


class widget(QWidget):
    def open_leadertable(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog(self.curr_text)
        self.ui.setupUi(self.window)
        self.window.show()

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = ''
        self.ls = []

        self.setWindowTitle('Ввод данных')
        self.setFixedSize(270, 150)

        self.line = QLabel('Введите ваше имя', self)
        self.line.setFont(QFont("MonacoRegular.ttf", 8))
        self.line.move(25, 10)
        self.line.resize(110, 25)

        self.input_value = QLineEdit('', self)
        self.input_value.move(140, 10)
        self.input_value.resize(100, 25)

        self.line2 = QLabel('Уровень сложности', self)
        self.line2.setFont(QFont("MonacoRegular.ttf", 8))
        self.line2.adjustSize()
        self.line2.move(25, 55)
        self.line2.resize(110, 25)

        self.difficulty = QComboBox(self)
        self.difficulty.addItems(["Любитель", "Профи"])
        self.difficulty.move(140, 55)
        self.difficulty.resize(80, 25)
        self.game.difficulty = self.curr_text = 'Любитель'
        self.difficulty.currentTextChanged.connect(self.difficulty2)

        self.button = QPushButton('Начать игру', self)
        self.button.move(170, 105)
        self.button.resize(85, 25)
        self.button.clicked.connect(self.exec)

        self.button_leader = QPushButton('Таблица лидеров', self)
        self.button_leader.move(25, 105)
        self.button_leader.resize(130, 25)
        self.button_leader.clicked.connect(self.open_leadertable)

        self.db = DB()

    def difficulty2(self):
        self.curr_text = self.difficulty.currentText()
        self.game.difficulty = self.curr_text

    def exec(self):
        if self.curr_text == '':
            self.curr_text = 'Любитель'
        if self.input_value.text() == '':
            self.name = 'unnamed'
        else:
            self.name = self.input_value.text()
        self.game.username = self.name
        self.ls = [self.name, self.curr_text]

        pygame.mixer.music.unpause()
        w.hide()


class Game:
    def __init__(self):
        self.username = ''
        self.difficulty = ''

        # задаем размеры экрана
        self.screen_width = 720
        self.screen_height = 460

        self.food_flag = True
        self.circle_radius = 10
        self.touch_the_circle = False

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.sweet_green = pygame.Color(154, 255, 154)
        self.green = pygame.Color(0, 139, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()

    def set_surface_and_title(self):
        """Задаем surface(поверхность поверх которой будет все рисоваться)
        и устанавливаем загаловок окна"""
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Змейка')
        # Добавление музыки на задний фон
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.set_volume(0.3)

    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                elif event.key == pygame.K_p:
                    self.pause()
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def print_text(self, message, x, y, font_color=(0, 0, 139), font_type='MonacoRegular.ttf', font_size=30):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.play_surface.blit(text, (x, y))

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        if w.ls[1] == 'Любитель':
            game.fps_controller.tick(15)
        else:
            game.fps_controller.tick(25)

    def pause(self):
        paused = True

        pygame.mixer.music.pause()

        while paused:
            self.print_text('Paused. Press enter to continue', 80, 250)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        paused = False
                        pygame.mixer.music.unpause()
            self.refresh_screen()

    def start_screen(self):
        pygame.mixer.music.pause()
        intro_text = ["ЗМЕЙКА", "",
                      "В разработке принимали участие", ""
                                                        "Боровков Павел и Шорников Александр", "", "", "", "",
                      "НАЖМИТЕ space ЧТОБЫ НАЧАТЬ",
                      "НАЖМИТЕ esc ЧТОБЫ ВЫЙТИ"]
        name = os.path.join('snake_background.jpg')
        load_image = pygame.image.load(name)
        fon = pygame.transform.scale(load_image, (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))
        font = pygame.font.SysFont('monaco', 25)
        text_coord = 30
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color(0, 0, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            self.play_surface.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        return
                pygame.display.flip()

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_over отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def save_score(self):
        """Сохранение результата"""
        db = DB()
        db.save(self.username, self.difficulty, self.score)

    def game_over(self):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        pygame.mixer.music.pause()
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        self.save_score()
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()


class Snake:
    def __init__(self, snake_color):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [100, 50]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # направление движение змеи, изначально
        # зададимся вправо
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Изменияем направление движения змеи только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        flag = True
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            while flag:
                # Цикл для проверки координат еды
                food_pos = [random.randrange(1, screen_width / 10) * 10,
                            random.randrange(1, screen_height / 10) * 10]
                for pos in self.snake_body:
                    if food_pos[0] != pos[0] and food_pos[1] != pos[1]:
                        flag = False
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            score += 1
            # если змея сьела большое яблоко то размер яблока возвращается к привычному значению
            if game.touch_the_circle:
                game.food_flag = True
                game.circle_radius = 10
                game.touch_the_circle = False

        else:
            # если не нашли еду, то убираем последний сегмент,
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        """Отображаем все сегменты змеи"""
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, 460 / 10) * 10]

    def draw_food(self, play_surface):
        """Отображение еды"""
        # когда отрисовывать большое яблоко
        if game.score % 7 == 0 and game.circle_radius > 2 and game.score != 0 and game.food_flag:
            self.circle_pos = self.food_pos[0] + 5, self.food_pos[1] + 5
            game.circle_radius -= 1 / 7
            pygame.draw.circle(game.play_surface, pygame.Color('red'), self.circle_pos, game.circle_radius)

        # если игрок не успел сьесть большое ялоко, рисуется обычное яблоко
        elif game.circle_radius <= 2:
            pygame.draw.rect(
                play_surface, self.food_color, pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    self.food_size_x, self.food_size_y))

        # если большое яблоко было съедено то счет прибавляется и флаг поднимается
        if game.circle_radius > 2 and game.circle_radius < 10 and (game.score - 1) % 7 == 0:
            game.score += 2
            game.touch_the_circle = True

        # если игрок не успел сьесть большое ялоко, опускается флаг
        if game.circle_radius <= 2:
            game.food_flag = False

        # рисуется обычное яблоко
        if game.score % 7 != 0 or game.circle_radius <= 2 or game.score == 0 or game.food_flag == False:
            pygame.draw.rect(
                play_surface, self.food_color, pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.green)

food = Food(game.brown, game.screen_width, game.screen_height)
game.init_and_check_for_errors()
game.set_surface_and_title()
pygame.mixer.music.play(-1)

app = QApplication(sys.argv)
w = widget(game)

while w.name == '':
    game.start_screen()
    w.show()



while True:
    snake.change_to = game.event_loop(snake.change_to)
    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.sweet_green)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.refresh_screen()
