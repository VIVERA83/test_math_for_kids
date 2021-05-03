from Menu_elements import *

class Creator:
    def __init__(self):
        self.__create_dict = {"button": self.__button,
                              "window": self.__window,
                              "title": self.__title,
                              "table": self.__table,
                              "checkbox": self.__checkbox,
                              "inputbox": self.__inputbox,
                              "messagebox": self.__messagebox,
                              "textlist": self.__textlist, }

    def __call__(self, resource, menuStruct: dict):
        self.res = resource
        self.winstruct = {key: [] for key in menuStruct.keys()}
        for key, items in menuStruct.items():
            for value in items:
                self.winstruct[key].append(self.__create_dict[value[0]](*value[1:]))
        return Window(self.window_name, self.background, self.screen_resolution, self.winstruct)

    def __window(self, name, background, screen_resolution):
        self.window_name = name
        self.background = self.res.get_image(background)
        self.screen_resolution = screen_resolution  #

    def __button(self, name: str, img_text, img_act, img_pas):
        self.res.add_list_string([img_text])
        return Button(name, self.res.get_image(img_text), self.res.get_image(img_act), self.res.get_image(img_pas))

    def __title(self, name, img_text, image):
        self.res.add_list_string([img_text, image])
        return Title(name, self.res.get_image(img_text), self.res.get_image(image))

    def __checkbox(self, name, img_text, img_act, img_pas, button_text: list):
        self.res.add_list_string([img_text, *button_text])
        return Checkbox(name, self.res.get_image(img_text), self.res.get_image(img_act), self.res.get_image(img_pas),
                        [self.res.get_image(item) for item in button_text])

    def __table(self, name: str, size: (int, int), columns: int, rows: int, img_text, img_act, img_pas):
        self.res.add_list_string([img_text])
        return Table(name, size, columns, rows, self.res.get_image(img_text), self.res.get_image(img_act),
                     self.res.get_image(img_pas))

    def __inputbox(self, name: str, default_msg: str, button_text: str, img_act, img_pas):
        self.res.add_list_string([button_text])
        return Inputbox(name, default_msg, self.res.get_image(button_text),
                        self.res.get_image(img_act), self.res.get_image(img_pas))

    def __messagebox(self, name: str, default_msg: str):
        return Messagebox(name, default_msg)

    def __textlist(self, name: str, message_list: [str], number_rows: int, img_act, img_pas):
        return Textlist(name, message_list, number_rows, self.res.get_image(img_act), self.res.get_image(img_pas))


