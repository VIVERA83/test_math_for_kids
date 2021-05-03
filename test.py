from interface.Menu_elements import *


class Example_field(Base):
    def __init__(self, name: str, size: (int, int), numbers: [int], img_act, img_pas):
        self.matrix = self.__get_count_cell_xy(numbers)
        self.name = name
        self.size = size
        self.columns = len(self.matrix[0])  # column -  x  - столбец
        self.rows = len(self.matrix)  # row -  y - строка
        self.size_button = size[0] // self.columns, size[1] // self.rows
        self.x, self.y = 0, 0  # координаты
        # self.background_color = 115, 67, 255
        self.table = self.__create(self.matrix, img_act, img_pas)

    def __create(self, matrix, img_act, img_pas):
        # создаем кнопки
        font = pg.font.SysFont(None, 40)

        table = []
        for y, line in enumerate(matrix):
            temp = []
            for x, char in enumerate(line):
                name = str(x) + str(y)
                img_text = font.render(char, 1, (127, 127, 10))
                if char == 'i':
                    temp.append(Input_text(name, ""))
                else:
                    temp.append(Button(name, img_text, img_act, img_pas))
            table.append(temp)

        # устанавливаем координаты
        [[button.setCoord((self.size_button[0] * x, self.size_button[1] * y)) for x, button in enumerate(columns)]
         for y, columns in enumerate(table)]
        # устанавливаем размер
        [[button.set_size(self.size_button) for button in columns] for columns in table]
        return table

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.set_colorkey((0, 0, 0))
        [[image.blit(button.draw(self._correctionMousePos(mouse_pos)), (button.x, button.y)) for button in columns] for
         columns in self.table]

        # Рисуем линию под примером
        x1 = self.size_button[0]
        x2 = self.size_button[0] * (self.columns - 1)
        y = self.size_button[1] * (self.rows - 2)
        pg.draw.line(image, "red", (x1, y), (x2, y), 4)
        # рисуем знак +
        x1 = 5
        x2 = self.size_button[0] - 5
        y = self.size_button[1] * (self.rows - 3)
        pg.draw.line(image, "red", (x1, y), (x2, y), 4)

        y1 = y - (self.size_button[1] // 2) + 5
        y2 = y + (self.size_button[1] // 2) - 5
        x1 = self.size_button[0] // 2
        pg.draw.line(image, "red", (x1, y1), (x1, y2), 4)
        return image

    def key_pressed(self, mouse_pos, key):
        mouse_pos = self._correctionMousePos(mouse_pos)
        for elements in self.table:
            for index, element in enumerate(elements):
                if element.checkCoor(mouse_pos):
                    result = element.key_pressed(mouse_pos, key)
                    if result:
                        return result

    def click(self, mouse_pos, mouse_click):
        mouse_pos = self._correctionMousePos(mouse_pos)
        if self.checkCoor(mouse_pos):
            mouse_pos = self._correctionMousePos(mouse_pos)
            for columns in self.table:
                for button in columns:
                    if button.checkCoor(mouse_pos) and mouse_click:
                        return button.click(mouse_pos, mouse_click)

    def setAction(self, function, params=None):
        [button.setAction(function, [x, y, params[x][y]]) for x, buttons in enumerate(self.table)
         for y, button in enumerate(buttons)]  # не нравиться

    def set_size(self, size: (int, int)):
        self.size = size
        self.act_pas = self.__create(self.img_text,
                                     pg.transform.scale(self.img_act, size),
                                     pg.transform.scale(self.img_pas, size))

    def __get_count_cell_xy(self, numbers: [str]) -> [str]:
        """Создает матрицу по которой будет формироваться виджет"""
        numbers.append(str(sum([int(number) for number in numbers])))
        max_len = max([len(number) for number in numbers])
        max_len += 0 if all([max_len > len(number) for number in numbers]) else 1
        numbers = [" " * (max_len - len(number)) + number + " " for number in numbers.copy()]
        print(max_len)
        matrix = [[" "] * len(numbers[0])]
        matrix.append([" "] * len(numbers[0]))
        for number in numbers:
            temp = []
            for char in number:
                temp.extend(char)
            matrix.append(temp)
        matrix.append([" "] * len(numbers[0]))
        for item in range(1, max_len):
            matrix[len(matrix) - 2][item] = "i"
        for item in range(1, max_len - 1):
            matrix[1][item] = "i"
        [print(line) for line in matrix]
        return matrix

    def get_numbers(self):
        numbers = {"up": [],
                   "down": []}
        for y, line in enumerate(self.matrix):
            for x, element in enumerate(line):
                if element == "i":
                    if y == 1:
                        numbers["up"].append(self.table[y][x].get_message())
                    else:
                        numbers["down"].append(self.table[y][x].get_message())
        return numbers


class Input_text(Base):
    def __init__(self, name: str, default_msg: str):
        self.TEXTCOLOR = (0, 255, 0)
        self.BGCOLOR = (255, 255, 255)
        self.Font = pg.font.SysFont(None, 65)

        self.name = name
        self.max_msg_len = 1
        self.message = default_msg[:self.max_msg_len]
        self.cursor_pos = len(self.message)

        self.img_text = self.Font.render(self.message[:30], 1, self.TEXTCOLOR)
        self.imgage = pg.Surface((300, 35))

        self.x, self.y = 0, 0
        self.size = self.imgage.get_size()[0], self.imgage.get_size()[1]

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.fill(self.BGCOLOR)
        pg.draw.rect(image, (50, 50, 50), (0, 0, *self.getSize()), 1, 1)
        image.blit(self.img_text, (0, 0))
        return image

    def key_pressed(self, mouse_pos, key):
        if self.checkCoor(mouse_pos):
            if key in [8, 127] and self.cursor_pos:  # K_BACKSPACE
                self.message = ""
            elif key not in [8, 13, 127] and key in list(range(48, 58)):
                self.message = chr(key)
                self.cursor_pos += 1 if self.cursor_pos < self.max_msg_len else 0
        self.img_text = self.Font.render(self.message, 1, self.TEXTCOLOR)

    def __return(self):
        return self.message

    def set_size(self, size: (int, int)):
        self.imgage = pg.Surface(size)
        self.size = self.imgage.get_size()[0], self.imgage.get_size()[1]

    def get_message(self):
        return self.message
