import pygame as pg


class Base:

    def checkCoor(self, mouse_pos):
        return (self.x < mouse_pos[0] < self.x + self.size[0]) and (self.y < mouse_pos[1] < self.y + self.size[1])

    def setCoord(self, coord: (int, int)):
        self.x, self.y = coord

    def get_coord(self):
        return self.x, self.y

    def getSize(self):
        return self.size

    def click(self, mouse_pos, mouse_click):
        pass

    def key_pressed(self, mouse_pos, key):
        pass

    def _correctionMousePos(self, mouse_pos):
        return mouse_pos[0] - self.x, mouse_pos[1] - self.y


class Button(Base):
    def __init__(self, name: str, img_text, img_act, img_pas, *args):
        """ img_text, img_act , img_pas - картинки"""
        self.name = name
        self.img_text = img_text
        self.img_act = img_act
        self.img_pas = img_pas
        self.size = img_pas.get_size()
        self.x, self.y = 0, 0  # координаты для отрисовки

        self.act_pas = self.__create(img_text, img_act, img_pas)  # изображение активной и пасивной кнопки
        self.action = None  # ссылка на функцию
        self.action_params = None  # ссылка на параметры

    def __create(self, img_text, img_act, img_pas):
        act_pas = []
        for index, image in enumerate([img_act, img_pas]):
            x = (image.get_size()[0] - img_text.get_size()[0]) // 2
            y = (image.get_size()[1] - img_text.get_size()[1]) // 2
            surface = pg.Surface(image.get_size())
            surface.blit(image, (0, 0))
            surface.blit(img_text, (x, y))
            surface.set_colorkey((0, 0, 0))
            act_pas.append(surface)
        return act_pas

    def draw(self, mouse_pos):  # добавил  mouse_click - 0 False, 1 True
        return self.act_pas[0] if self.checkCoor(mouse_pos) else self.act_pas[1]

    def click(self, mouse_pos, mouse_click):
        if mouse_click and self.checkCoor(mouse_pos):
            if self.action:
                print(self.action, self.params)
                if self.params != None:
                    return self.action.__name__, self.action(self.params)
                else:
                    return self.action.__name__, self.action()

    def setAction(self, function, params=None):
        self.action = function
        self.params = params

    def set_size(self, size: (int, int)):
        self.size = size
        self.act_pas = self.__create(self.img_text,
                                     pg.transform.scale(self.img_act, size),
                                     pg.transform.scale(self.img_pas, size))

    def set_image(self, img_text, img_act, img_pas):
        self.img_text = img_text
        self.img_act = img_act
        self.img_pas = img_pas


class Title(Base):

    def __init__(self, name, text, image, *args):
        self.title_name = name
        self.size = image.get_size()
        self.x, self.y = 0, 0
        self.image = self.__create(text, image)

    def __create(self, text, image):
        x = (self.size[0] - text.get_size()[0]) // 2
        y = (self.size[1] - text.get_size()[1]) // 2
        surface = pg.Surface(image.get_size())
        surface.blit(image, (0, 0))
        surface.blit(text, (x, y))
        surface.set_colorkey((0, 0, 0))
        return surface

    def draw(self, *args):
        return self.image


class Checkbox(Base):

    def __init__(self, name, img_text, img_act, img_pas, button_text: list):
        self.x, self.y = 0, 0
        self.name = name
        self.title = Title(self.name, img_text, img_text)
        self.checkbox_button = [Button(str(name), button_text, img_act, img_pas) for name, button_text in
                                enumerate(button_text)]
        for button in self.checkbox_button:
            button.select = False
        self.setselect(0)
        self.size = self.__create(img_text)

    def __create(self, img_text):
        print("__createMenu--------------")
        # максимальная высота изображения
        max_width_line = [img_text.get_size()[0], sum([button.getSize()[0] for button in self.checkbox_button])]
        max_height_line = [img_text.get_size()[1], max([button.getSize()[1] for button in self.checkbox_button])]

        shif_x = 10  # расстояние между элементами по оси X
        shif_y = 10  # расстояние между элементами по оси Y
        W_window = max(max_width_line) + shif_x * len(self.checkbox_button)  # ширина диалогового окна
        H_window = sum(max_height_line) + shif_y * 2  # высота диалогового окна
        # print(W_window, H_window)
        # Начальные точки для каждой линии отрисовки
        step_y = 10
        # step_x = 0
        self.title.x = (W_window - self.title.getSize()[0]) // 2
        self.title.y = step_y
        coord = self.x, self.y + self.title.getSize()[1] + step_y
        for button in self.checkbox_button:
            button.setCoord(coord)
            coord = coord[0] + button.getSize()[0] + shif_x, coord[1]

        return W_window, H_window

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.set_colorkey((0, 0, 0))
        image.blit(self.title.draw(1), (self.title.x, self.title.y))
        for button in self.checkbox_button:
            if button.select:
                image.blit(button.draw((button.x + 1, button.y + 1)), (button.x, button.y))
            else:
                image.blit(button.draw((-1, -1)), (button.x, button.y))
        return image

    def click(self, mouse_pos, mouse_click):
        if self.checkCoor(mouse_pos):
            mouse_pos = self._correctionMousePos(mouse_pos)
            for index, button in enumerate(self.checkbox_button):
                if button.checkCoor(mouse_pos) and mouse_click:
                    self.setselect(index)
                    return button.click(mouse_pos, mouse_click)

    def setselect(self, button_number):
        for bt in self.checkbox_button:
            bt.select = False
        self.checkbox_button[button_number].select = True

    def setAction(self, function, params=None):
        for index, button in enumerate(self.checkbox_button):
            print(function, params[index])
            button.setAction(function, params[index])


class Table(Base):
    def __init__(self, name: str, size: (int, int), columns: int, rows: int, img_text, img_act, img_pas):
        self.name = name
        self.size = size
        self.size_button = size[0] // columns, size[1] // rows
        self.columns = columns  # column -  x  - столбец
        self.rows = rows  # row -  y - строка
        self.x, self.y = 0, 0  # координаты
        self.background_color = 115, 67, 255
        self.table = self.__create(self.size, self.columns, self.rows, img_text, img_act, img_pas)

    def __create(self, size: (int, int), columns: int, rows: int, img_text, img_act, img_pas):
        # создаем кнопки
        table = [[Button(str(x) + str(y), img_text, img_act, img_pas) for x in range(columns)]
                 for y in range(rows)]
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
        return image

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

    def set_image_button(self, x, y, img_text, img_act, img_pas):
        self.table[x][y].set_image(img_text, img_act, img_pas)
        self.table[x][y].set_size(self.size_button)


class Inputbox(Base):
    def __init__(self, name: str, default_msg: str, button_text, img_act, img_pas):
        self.TEXTCOLOR = (0, 255, 0)
        self.BGCOLOR = (255, 255, 255)
        self.Font = pg.font.SysFont(None, 40)

        self.name = name
        self.max_msg_len = 15
        self.message = default_msg[:self.max_msg_len]
        self.cursor_pos = len(self.message)
        self.button_text = button_text

        self.img_act = img_act
        self.img_pas = img_pas
        self.img_text = self.Font.render(self.message[:30], 1, self.TEXTCOLOR)
        self.imgage = pg.Surface((300, 35))

        self.button = Button(name, button_text, img_act, img_pas)
        self.button.setAction(self.__return)
        self.button.setCoord((self.imgage.get_size()[0], 0))
        self.button.set_size((40, 35))

        self.x, self.y = 0, 0
        self.size = self.imgage.get_size()[0] + self.button.size[0], self.imgage.get_size()[1]

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.fill(self.BGCOLOR)
        pg.draw.rect(image, (50, 50, 50), (0, 0, *self.getSize()), 1, 1)
        image.blit(self.img_text, (0, 0))
        image.blit(self.button.draw(self._correctionMousePos(mouse_pos)), (self.size[0] - self.button.size[0], 0))
        return image

    def key_pressed(self, mouse_pos, key):
        if self.checkCoor(mouse_pos):
            if key == 8 and self.cursor_pos:  # K_BACKSPACE
                self.message = self.message[:self.cursor_pos - 1] + self.message[self.cursor_pos:]
                self.cursor_pos -= 1
            elif key == 127 and self.cursor_pos < len(self.message):  # K_DELETE
                self.message = self.message[:self.cursor_pos] + self.message[self.cursor_pos + 1:]
            elif key == 1073741904 and self.cursor_pos > 0:  # K_LEFT:
                self.cursor_pos -= 1
            elif key == 1073741903 and self.cursor_pos < len(self.message):  # K_RIGHT:
                self.cursor_pos += 1
            elif key == 13 and self.cursor_pos:
                button_mouse_pos = self.button.x + 1, self.button.y + 1
                return self.button.click(button_mouse_pos, 1)
            elif key not in [8, 13, 127] and key < 9000:
                self.message = (self.message[0: self.cursor_pos] + chr(key) + self.message[self.cursor_pos:])[
                               :self.max_msg_len]
                self.cursor_pos += 1 if self.cursor_pos < self.max_msg_len else 0
        temp_message = self.message[0: self.cursor_pos] + "|" + self.message[self.cursor_pos:]
        self.img_text = self.Font.render(temp_message, 1, self.TEXTCOLOR)

    def __return(self):
        return self.message

    def click(self, mouse_pos, mouse_click):
        if self.checkCoor(mouse_pos) and mouse_click:
            return self.button.click(self._correctionMousePos(mouse_pos), mouse_click)


class Messagebox(Base):
    def __init__(self, name: str, default_msg: str):
        self.TEXTCOLOR = (0, 255, 0)
        self.bg_color_select = (127, 127, 127)
        self.bg_color_notselect = (255, 255, 255)
        self.select = False
        self.Font = pg.font.SysFont(None, 40)

        self.name = name
        self.max_msg_len = 15
        self.message = default_msg[:self.max_msg_len]
        self.message_image = None
        self.set_message(self.message)
        self.cursor_pos = len(self.message)

        self.x, self.y = 0, 0
        self.size = pg.Surface((300, 35)).get_size()

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.fill(self.bg_color_select if self.select else self.bg_color_notselect)
        pg.draw.rect(image, (50, 50, 50), (0, 0, *self.getSize()), 1, 1)
        image.blit(self.get_message_image(), (0, 0))
        return image

    def click(self, mouse_pos, mouse_click):
        if self.checkCoor(mouse_pos) and mouse_click:
            return self.message

    def key_pressed(self, mouse_pos, key):
        if self.checkCoor(mouse_pos) and key == 13:
            return self.message

    def set_message(self, message):
        self.message = message
        self.message_image = self.Font.render(message, 1, self.TEXTCOLOR)

    def get_message_image(self):
        return self.message_image


class Textlist(Base):
    def __init__(self, name: str, message_list: [str], number_rows: int, img_act, img_pas):
        self.name = name
        self.number_rows = number_rows if number_rows > 2 else 2
        self.current_position = 0  # внутри textlist
        self.position_msg_list = 0
        self.message_list = message_list
        self.message_count = len(self.message_list)
        if self.message_count < number_rows:
            message_list.extend([""] * (self.number_rows - self.message_count))
        self.textlist = []
        self.buttons = []
        self.button_size = 35, 35
        self.x, self.y = 0, 0
        self.size = self.__create(img_act, img_pas)

    def __create(self, img_act, img_pas):
        self.textlist = [Messagebox(str(m_name), message) for m_name, message in
                         enumerate(self.message_list[:self.number_rows])]
        [messagebox.setCoord((0, index * messagebox.getSize()[1])) for index, messagebox in enumerate(self.textlist)]
        self.textlist[0].select = True

        self.buttons = [Button(str(name), pg.Surface((1, 1)), img_act, img_pas) for name in range(2)]
        [button.set_size(self.button_size) for button in self.buttons]
        self.buttons[0].setAction(self.scroll_up)
        self.buttons[1].setAction(self.scroll_down)

        self.buttons[0].setCoord((self.textlist[0].getSize()[0], self.y))
        self.buttons[1].setCoord(
            (self.textlist[0].getSize()[0], (self.number_rows - 1) * self.textlist[0].getSize()[1]))
        return self.textlist[0].getSize()[0] + self.button_size[0], self.number_rows * self.textlist[0].getSize()[1]

    def draw(self, mouse_pos):
        image = pg.Surface(self.size)
        image.set_colorkey((0, 0, 0))
        [image.blit(message_box.draw(mouse_pos), message_box.get_coord()) for message_box in self.textlist]
        [image.blit(button.draw(self._correctionMousePos(mouse_pos)), button.get_coord()) for button in self.buttons]
        return image

    def click(self, mouse_pos, mouse_click):
        mouse_pos = self._correctionMousePos(mouse_pos)
        for index, message_box in enumerate(self.textlist):
            result = message_box.click(mouse_pos, mouse_click)
            if result:
                self.setselect(index)
                return self.click.__name__, result
        for button in self.buttons:
            result = button.click(mouse_pos, mouse_click)
            if result:
                return result

    def key_pressed(self, mouse_pos, key):
        for index, message_box in enumerate(self.textlist):
            result = message_box.key_pressed(mouse_pos, key)
            if result:
                self.setselect(index)
                return result

    def setselect(self, button_number):
        for message_box in self.textlist:
            message_box.select = False
        self.textlist[button_number].select = True

        if button_number > self.current_position:
            self.position_msg_list += button_number - self.current_position
        elif button_number < self.current_position:
            self.position_msg_list += button_number - self.current_position
        self.current_position = button_number

    def scroll_up(self):
        if self.current_position:
            self.current_position -= 1
            self.position_msg_list -= 1
        elif self.position_msg_list:
            self.position_msg_list -= 1
            for index in range(self.number_rows):
                self.textlist[index].set_message(
                    self.message_list[self.position_msg_list + index - self.current_position])
        self.setselect(self.current_position)

    def scroll_down(self):
        if self.current_position < self.number_rows - 1:
            self.current_position += 1
            self.position_msg_list = self.current_position
        elif self.position_msg_list < self.message_count - 1:
            self.position_msg_list += 1
            for index in range(self.number_rows):
                self.textlist[index].set_message(
                    self.message_list[self.position_msg_list + index - self.current_position])
        self.setselect(self.current_position)


class Window(Base):

    def __init__(self, name, background, screen_resolution, menuStruct: dict):
        del menuStruct[0]
        self.window_name = name
        self.background = background
        self.screen_resolution = screen_resolution  #
        self.win_objects = {}
        self.x, self.y = 0, 0
        self.image = None
        self.size = self.__createMenu(menuStruct)

    def __createMenu(self, menuStruct: dict):

        for values in menuStruct.values():
            for obj in values:
                if self.win_objects.get(obj.__class__.__name__.lower()):
                    self.win_objects[obj.__class__.__name__.lower()].append(obj)
                else:
                    self.win_objects.setdefault(obj.__class__.__name__.lower(), [obj])

        # создаем список из максимальных высот изображения в каждом из ключевых полей словаря
        max_width_line = [sum([item.getSize()[0] for item in value]) for value in menuStruct.values()]
        max_height_line = [max([item.getSize()[1] for item in value]) for value in menuStruct.values()]

        shif_x = 10  # расстояние между элементами по оси X
        shif_y = 10  # расстояние между элементами по оси Y
        W_window = max(max_width_line) + shif_x  # ширина диалогового окна
        H_window = sum(max_height_line) + (len(menuStruct) + 1) * shif_y  # высота диалогового окна

        # Начальные точки для каждой линии отрисовки
        step_y = 10

        for index, values in enumerate(menuStruct.values()):
            coord = self.x + (W_window - max_width_line[index]) // 2, self.y + step_y
            for obj in values:
                obj.setCoord(coord)
                coord = coord[0] + obj.getSize()[0] + shif_x, coord[1]
            step_y += shif_y + max_height_line[index]
        self.image = pg.Surface((W_window, H_window))
        self.background = pg.transform.scale(self.background, (W_window, H_window))
        return W_window, H_window

    def draw(self, mouse_pos):
        mouse_pos = self._correctionMousePos(mouse_pos)
        self.image.blit(self.background, (0, 0))
        [self.image.blit(item.draw(mouse_pos), (item.x, item.y)) for values in self.win_objects.values() for item in
         values]
        return self.image

    def click(self, mouse_pos, mouse_click):
        mouse_pos = self._correctionMousePos(mouse_pos)
        for values in self.win_objects.values():
            for obj in values:
                result = obj.click(mouse_pos, mouse_click)
                if result:
                    return result

    def key_pressed(self, mouse_pos, key):
        mouse_pos = self._correctionMousePos(mouse_pos)
        for values in self.win_objects.values():
            for obj in values:
                result = obj.key_pressed(mouse_pos, key)
                print("key_pressed", result)
                if result:
                    return result

    def getCoorCenter(self, screen_resolution):
        x = (screen_resolution[0] - self.size[0]) // 2
        y = (screen_resolution[1] - self.size[1]) // 2
        self.setCoord((x, y))
        return x, y
