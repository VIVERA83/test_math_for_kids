from Resource import Resource
from new_tree_menu import Functions
import pygame

# Создаем ресурс с всеми картинками которые будут использоваться в программе

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

res = Resource()
res.add_image_file("bk_window", r"Resources\bk.jpg")
res.add_image_file("cb_act", r"Resources\checkbox_button_active.png")
res.add_image_file("cb_pas", r"Resources\checkbox_button_pass.png")
res.add_image_file("bk_menu", r"Resources\background_menu.jpg")
res.add_image_file("button", r"Resources\button_play_active.png")
res.add_image_file("active", r"Resources\button_blue.png")
res.add_image_file("pass", r"Resources\button_purple.png")
res.add_image_file("rect", r"Resources\rect.png")

res.add_sound("move", pygame.mixer.Sound(r"Resources\move.ogg"))
res.add_sound("choice", pygame.mixer.Sound(r"Resources\choice.ogg"))
# Параметры дисплея

screen_resolution = 1960, 1080
background = res.get_image("bk_window")

# Описываем структуру меню

main_menu = {0: [["window", "Главное меню", "bk_menu", screen_resolution]],  # фон меню - картинка
             1: [["title", "TITLE", "Главное меню", "button"]],
             2: [["button", "name_1", "Одиночная игра", "active", "pass"]],
             3: [["button", "name_2", "Сетевая игра", "active", "pass"]],
             4: [["button", "name_3", "Рекорды", "active", "pass"]],
             5: [["button", "name_4", "Настройки", "active", "pass"]],
             6: [["button", "name_5", "Сменить игрока", "active", "pass"]],
             7: [["button", "name_6", "Выход", "active", "pass"]]
             }

single_game_menu = {0: [["window", "Одиночная игра", "bk_menu", screen_resolution]],  # фон меню - картинка
                    1: [["title", "TITLE", "Одиночная игра", "button"]],
                    2: [["button", "name_1", "Продолжить", "active", "pass"]],
                    3: [["button", "name_2", "Новая игра", "active", "pass"]],
                    4: [["button", "name_3", "Назад", "active", "pass"]]
                    }
multiplayer_menu = {}

message_list = ["button", "name_1", "Продолжить", "active", "pass"]


records_menu = {0: [["window", "Рекорды", "bk_menu", screen_resolution]],
                1: [["title", "TITLE", "Смена игрока", "button"]],
                2: [["textlist", "textlist_1", [], 5, "active", "pass"],
                    ["table", "table_1", (400, 180), 2, 5, " ", "active", "active"]],
                3: [["title", "TITLE", " ", "Добавить игрока"],
                    ["inputbox", "inputbox_1", "Игрок_1", "ок ", "active", "pass"]],
                4: [["button", "name_2", "Применить", "active", "pass"],
                    ["button", "name_1", "Назад", "active", "pass"]],
                }
settings_menu = {0: [["window", "Одиночная игра", "bk_menu", screen_resolution]],  # фон меню - картинка
                 1: [["title", "TITLE", "Настройки", "button"]],
                 2: [["checkbox", "name_1", "Музыка", "cb_act", "cb_pas", ("Вкл", "Выкл")]],
                 3: [["checkbox", "name_2", "Звуки", "cb_act", "cb_pas", ("Вкл", "Выкл")]],
                 4: [["button", "name_3", "Назад", "active", "pass"]]
                 }
change_player_menu = {}

exit_menu = {0: [["window", "Выход", "bk_menu", screen_resolution]],
             1: [["title", "TITLE", " ", "Выйти из игры ?"]],
             2: [["button", "name_1", "Да", "active", "pass"], ["button", "name_2", "Нет", "active", "pass"]]
             }

new_game_menu = {0: [["window", "Новая игра", "bk_menu", screen_resolution]],  # фон меню - картинка
                 1: [["title", "TITLE", "Новая игра", "button"]],
                 2: [["checkbox", "name_1", "Размер игрового поля", "cb_act", "cb_pas", ("3x3", "7x7", "11x11")]],
                 3: [["checkbox", "name_2", "Победная линия", "cb_act", "cb_pas", ("3", "5", "7")]],
                 4: [["checkbox", "name_3", "Очередность хода", "cb_act", "cb_pas", ("Игрок", "Комп")]],
                 5: [["button", "name_1", "В бой", "active", "pass"], ["button", "name_2", "Назад", "active", "pass"]]
                 }

# Создаем меню, и добавляем окна

win = Functions("Главное меню", res, main_menu, screen_resolution)

# Служебные флаги
run = True
play_music = win.play_music(True)
play_sound = win.play_sound(True)
default_settings = [("play_music", play_music), ("play_sound", play_sound)]

win.addWindow("Одиночная игра", single_game_menu)
win.addWindow("Новая игра", new_game_menu)
win.addWindow("Рекорды", records_menu)
win.addWindow("Настройки", settings_menu)
win.addWindow("Выход", exit_menu)

# Создаем связи между окнами
# переход ИЗ "Главное меню"
win.createLink("Главное меню", "button", "name_1", "Одиночная игра")
win.createLink("Главное меню", "button", "name_3", "Рекорды")
win.createLink("Главное меню", "button", "name_4", "Настройки")
win.createLink("Главное меню", "button", "name_6", "Выход")

# Переход ИЗ "Одиночная игра"
win.createLink("Одиночная игра", "button", "name_2", "Новая игра")
win.createLink("Одиночная игра", "button", "name_3", "Главное меню")

# Переход ИЗ "Новая игра"
win.createLink("Новая игра", "button", "name_2", "Одиночная игра")

# Переход ИЗ "Рекорды"
win.createLink("Рекорды", "button", "name_1", "Главное меню")

# Переход ИЗ "Настройки"
win.createLink("Настройки", "button", "name_3", "Главное меню")
win.setActionMenuItem("Настройки", "checkbox", "name_1", win.play_music, [True, False])
win.setActionMenuItem("Настройки", "checkbox", "name_2", win.play_sound, [True, False])

# Переход ИЗ "Выход"
win.createLink("Выход", "button", "name_2", "Главное меню")
win.setActionMenuItem("Выход", "button", "name_1", win.exit_program)
# Переход ИЗ В бой


