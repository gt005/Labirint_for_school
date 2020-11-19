class LabirintTurtle:
    def __init__(self):
        self.labyrinth_field = [ [ 0 ] ]
        self.turtle_coordinates = (0, 0)
        self.wall_char = '*'
        self.space_char = ' '
        self.turtle_char = u"\U0001F422"

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

        self.__parse_map_from_file()

    def show_map(self, turtle=False):
        pass

    def check_map(self):
        pass

    def exit_count_step(self):
        pass

    def exit_show_step(self):
        pass
    
    def __parse_map_from_file(self):
        self.labyrinth_field = list(map(list, self.labyrinth_field.split('\n')[:-2]))
        self.turtle_coordinates = (self.labyrinth_field.split('\n')[:-1], self.labyrinth_field.split('\n')[:-2])
        print(*self.labyrinth_field, sep='\n')


game = LabirintTurtle()
game.wall_char = '*'
game.space_char = ' '
game.load_map("l1.txt")
# print(*game.labyrinth_field, sep='\n')


