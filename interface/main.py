from setting import screen_resolution, background, win, run, default_settings
import pygame


def api(api: (__name__, bool)):
    global run
    if api:
        if api[0] == "exit_program":
            run = api[1]
        if api[0] == "play_music":
            if api[1]:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()


# инициализация Звука, и библиотек для работы с звуком

pygame.mixer.music.load(r"Resources\music.mp3")
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
FPS = 60
# запускаем настройки по умолчанию
[api(settings) for settings in default_settings]


mouse_click = pygame.mouse.get_pressed()[0]
mouse_pos = pygame.mouse.get_pos()
key = ""
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.unicode:
                key = ord(event.unicode)
            else:
                key = event.key
            result = win.key_pressed(mouse_pos, key)
        else:
            result = win.click(mouse_pos, mouse_click)
        if result:
            api(result)

    screen.blit(background, (0, 0))
    coord = win.getCoorCenter()
    screen.blit(win.menu[win.current_menu].draw(mouse_pos), coord)

    pygame.display.update()

pygame.quit()
