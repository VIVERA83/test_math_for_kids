from Creator import Creator

class TreeMenu:

    def __init__(self, name, resource, menustruct, screen_resolution, *args):
        self.resource = resource
        self.creator = Creator()
        self.menu = {name: self.creator(self.resource, menustruct)}
        self.current_menu = name
        self.screen_resolution = screen_resolution

    def addWindow(self, name, menustruct: dict):
        self.menu[name] = self.creator(self.resource, menustruct)

    def createLink(self, from_menu_name, from_element_type, from_element_name, in_menu_name):
        for obj in self.menu[from_menu_name].win_objects[from_element_type]:
            if obj.name == from_element_name:
                obj.setAction(self.navigateMenu, in_menu_name)

    def navigateMenu(self, menu_name):
        self.current_menu = menu_name

    def getCoorCenter(self):
        return self.menu[self.current_menu].getCoorCenter(self.screen_resolution)

    def setActionMenuItem(self, menu_name, element_type, element_name, function, params=None):
        for obj in self.menu[menu_name].win_objects[element_type]:
            if obj.name == element_name:
                obj.setAction(function, params)


class Functions(TreeMenu):

    def __init__(self, name, resource, menustruct, screen_resolution):
        super().__init__(name, resource, menustruct, screen_resolution)
        self.sound = True

    def click(self, mouse_pos, mouse_click):
        result = self.menu[self.current_menu].click(mouse_pos, mouse_click)
        if result:
            print("Functions, click =", result)
            if self.current_menu == "В бой":
                self.play_sound(self.sound, "move")
            else:
                self.play_sound(self.sound, "choice")
        return result

    def key_pressed(self, mouse_pos, key):
        return self.menu[self.current_menu].key_pressed(mouse_pos, key)

    def exit_program(self):
        return False

    def play_music(self, play: bool):
        return play

    def play_sound(self, play: bool, sound="choice"):
        self.sound = play
        if play:
            self.resource.get_sound(sound).play()
            return play
