from interface.Menu_elements import *
from interface.Resource import Resource
from pygame import image
from random import randint
from os import getcwd
from test import Example_field


def get_random_numders(discharge: int, count: int) -> [int]:
    """Возвращает список случайных чисел с указанным числовым разрядом. discharge - разрядность числа от 1 до 6 знаков
    count - количество чисел от 1 до 3"""
    if not isinstance(discharge, int) or (1 > discharge) or (discharge > 6):
        raise TypeError(f"discharge - число от 1 до 6, вы передали {type(discharge)} с значением {repr(discharge)}")
    if not isinstance(count, int) or (1 > count) or (count > 3):
        raise TypeError(f"count - число от 1 до 3, вы передали {type(count)} с значением {repr(count)}")
    return [randint(10 ** (discharge - 1), int(str(9) * discharge)) for _ in range(count)]


def get_count_cell_xy(numbers: [str]) -> [str]:
    """Создает матрицу по которой будет формироваться виджет"""
    numbers.append(str(sum([int(number) for number in numbers])))
    max_len = max([len(number) for number in numbers])
    max_len += 0 if all([max_len > len(number) for number in numbers]) else 1
    numbers = [" " * (max_len - len(number)) + number + " " for number in numbers.copy()]
    matrix = [[" "] * len(numbers[0])]
    for number in numbers:
        temp = []
        for char in number:
            temp.extend(char)
        matrix.append(temp)
    matrix.append([" "] * len(numbers[0]))
    return matrix


current_dir = f"{getcwd()}\\"
res = Resource()
res.add_list_string(
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Молодец", "решить", "Не сдавайся ты можешь", " "], font_size=46)
img_text = res.get_image('решить')
img_text_1 = res.get_image("Не сдавайся ты можешь")
img_text_2 = res.get_image(" ")
img_a = res.get_image('Молодец')
img_b = image.load(current_dir + f"Resources\\button_play_active.png")
img_act = image.load(current_dir + f"Resources\\button_blue.png")
img_pas = image.load(current_dir + f"Resources\\button_purple.png")
img_rect = image.load(current_dir + f"Resources\\rect.png")

button = Button("кнопка", img_text, img_act, img_pas)
button.setCoord((400, 400))
numbers_lst = get_random_numders(3, 2)  # первый параметр разрядность числа, второй кол-во чисел
answer = sum(numbers_lst)
print("answer", answer)
numbers_lst = [str(number) for number in numbers_lst.copy()]
example_field = Example_field("test", (300, 300), numbers_lst, img_act, img_rect)
button.setAction(example_field.get_numbers)

#
# lst = get_random_numders(2, 2)
# lst_str = [str(number) for number in lst]
# # print(lst_str)
# n = get_count_cell_xy(lst_str)
# # [print(line) for line in n]
