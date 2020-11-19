class LabirintTurtle:
    def __init__(self):
        self.labyrinth_field = None
        self.turtle_coordinates = (0, 0)

    def load_map(self, file_name):
        try:
            with open(file_name, 'rt') as file:
                self.labyrinth_field = file.read()
        except TypeError:
            print("Неправильное название файла, загрузите другой файл")
        except FileNotFoundError:
            print("Файл не найден, загрузите другой файл")
        except UnicodeDecodeError:
            print("Некорректные данные файла")

        self._parse_map_from_file()

    def show_map(self, turtle=False):
        pass

    def check_map(self):
        pass

    def exit_count_step(self):
        pass

    def exit_show_step(self):
        pass

    def _parse_map_from_file(self):
        self.labyrinth_field = self.labyrinth_field.split('\n')[:-2]
        for i in self.labyrinth_field:
            if 

game = LabirintTurtle()
game.load_map("l1.txt")
print(*game.labyrinth_field, sep='\n')


