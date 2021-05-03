import settings as sett
import pygame
from os import getcwd

screen_resolution = 800, 600

screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
FPS = 60

current_dir = f"{getcwd()}\\"
print(current_dir)
bk = pygame.image.load(current_dir + f"Resources\\map_bk.jpg")
mouse_click = pygame.mouse.get_pressed()[0]
mouse_pos = pygame.mouse.get_pos()
img_answer = sett.Title('0', sett.img_text_2, sett.img_text_1).draw()
run = True
while run:
    clock.tick(FPS)
    key = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.unicode:
                key = ord(event.unicode)
            else:
                key = event.key
            if key:
                sett.example_field.key_pressed(mouse_pos, key)

        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        if mouse_click:
            sett.example_field.click(mouse_pos, mouse_click)
            result = sett.button.click(mouse_pos, mouse_click)
            if result:
                print("кнопку", result)
                # answer = int("".join(result[1]["down"]))
                # print("answer = ",answer, answer)
                if result[1]["down"] == [str(number) for number in str(sett.answer)]:
                    img_answer = sett.Title('a', sett.img_a, sett.img_b).draw()
                    print("молодец")
                else:
                    img_answer = sett.Title('0', sett.img_text_2, sett.img_text_1).draw()
    screen.blit(bk, (0, 0))
    screen.blit(img_answer, (400, 100))
    screen.blit(sett.button.draw(mouse_pos), (400, 400))
    screen.blit(sett.example_field.draw(mouse_pos), (15, 15))
    # pygame.draw.line(screen, "red", (20, 100), (60, 100), 4)
    # pygame.draw.line(screen, "red", (40, 80), (40, 120), 4)
    pygame.display.update()

pygame.quit()
