import time
'''
TODO: 

'''

class LabirintTurtle:

    def __init__(self, *args, **kwargs):
        self.__labyrinth_field = None
        self.__turtle_coordinates = (0, 0)
        self.__wall_char = '*'
        self.__way_char = '🌏'
        self.__space_char = ' '
        self.__turtle_char = u"\U0001F422"  # - Черепашка 🌏
        self.__is_map_valid = True
        self.__minimum_steps_amount = -1
        self.__out_point_row = -1
        self.__out_point_col = -1
        self.__queue = []
        self.__map_of_numbers = None
        self.__graphics_map = None
        self.__graphics_map_without_way = None
        self.__way_word_description = []
        # Словесное описание дороги (тут в градусах поворота)

    def load_map(self, file_name, *args, **kwargs) -> None:
        try:
            file_with_map = open(file_name, 'rt')
            field_with_coordinates = file_with_map.read()
        except TypeError:
            print(
                "\033[31m{}".format(
                    "Неправильное название файла, загрузите другой файл"
                ),
                "\033[39m"  # Обнуление цвета
            )
            self.__is_map_valid = False
            return
        except FileNotFoundError:
            print(
                "\033[31m{}".format(
                    "Файл не найден, загрузите другой файл"
                ),
                "\033[39m"  # Обнуление цвета
            )
            self.__is_map_valid = False
            return
        except UnicodeDecodeError:
            print(
                "\033[31m{}".format(
                    "Некорректные данные файла"
                ),
                "\033[39m"  # Обнуление цвета
            )
            self.__is_map_valid = False
            return

        self.__is_map_valid = True
        self.__parse_map_from_file(field_with_coordinates)

    def show_map(self, turtle: bool = False, *args, **kwargs) -> None:
        '''
        Вывод карты в консоль
        :param turtle: False - черепашка не выводится, True, выводится
        :return: None
        '''
        if turtle:
            self.__graphics_map_without_way[self.__turtle_coordinates[0]][
                self.__turtle_coordinates[1]] = self.__turtle_char
        else:
            self.__graphics_map_without_way[self.__turtle_coordinates[0]][
                self.__turtle_coordinates[1]] = self.__space_char
        for i in self.__graphics_map_without_way:
            print(*i, sep='\t')

    def check_map(self, *args, **kwargs) -> None:
        ''' Проверка карты на валидность '''
        if __is_map_valid:
            print("\033[32m{}".format("Карта валидна"), "\033[39m")
        else:
            print(
                "\033[31m{}".format("Карта не валидна, введите другую"),
                "\033[39m"  # Обнуление цвета
            )

    def exit_count_step(self, *args, **kwargs) -> None:
        if not self.__is_map_valid:
            print("\033[31m{}".format("Карта не валидна"), "\033[39m")
            return

        print(
            "\033[32mМинимальное количество ходов - {}".format(
                self.__minimum_steps_amount
            ),
            "\033[39m"  # Обнуление цвета
        )

    def exit_show_step(self, *args, **kwargs) -> None:
        if not self.__is_map_valid:
            print("\033[31m{}".format("Карта не валидна"), "\033[39m")
            return
        for i in self.__graphics_map:
            for j in i:
                if j == self.__wall_char:
                    print("\033[33m{}".format(j), end='\t')
                else:
                    print(j, end='\t')
            print()
        print("\033[39m")

    def describe_turtle_path(self, *args, **kwargs):

        if (self.__turtle_coordinates[0] == 0):
            print("Повернись вправо")
            print(f"Идти вперед на 1")
            return
        elif (self.__turtle_coordinates[0] == len(
                self.__map_of_numbers
        ) - 1):
            print("Повернись влево")
            print(f"Идти вперед на 1")
            return
        elif (self.__turtle_coordinates[1] == 0):
            print(f"Идти вперед на 1")
            return
        elif (self.__turtle_coordinates[1] == len(
                self.__map_of_numbers[0]
        ) - 1):
            print("Развернуться")
            print(f"Идти вперед на 1")
            return

        directions_words = {
            90: "Повернись вправо",
            180: "Развернуться",
            270: "Повернись влево"
        }

        forward_length_count = 0
        current_turtle_direction = 270
        for direction in reversed(self.__way_word_description):
            if (360 - (current_turtle_direction - direction)) % 360 == 0:
                forward_length_count += 1
            else:
                print(f"Идти вперед на {forward_length_count}")
                print(directions_words[(360 - (current_turtle_direction - direction)) % 360])
                forward_length_count = 1
                current_turtle_direction = direction

        print(f"Идти вперед на {forward_length_count}")

    def __parse_map_from_file(
            self, field_with_coordinates, *args, **kwargs
    ):

        if not field_with_coordinates:
            self.__is_map_valid = False
            print("\033[31m{}".format("Карта не валидна"), "\033[39m")
            return

        self.__map_of_numbers = list(map(
            list,
            field_with_coordinates.split('\n'))
        )[:-2]  # Две последние строки - координаты черепахи

        self.__graphics_map = list(map(
            list,
            field_with_coordinates.split('\n'))
        )[:-2]

        self.__graphics_map_without_way = list(map(
            list,
            field_with_coordinates.split('\n'))
        )[:-2]

        self.__turtle_coordinates = (
            int(field_with_coordinates.split('\n')[-1]),
            int(field_with_coordinates.split('\n')[-2])
        )

        self.__queue = [self.__turtle_coordinates]

        for row in range(len(self.__map_of_numbers)):
            for col in range(len(self.__map_of_numbers[row])):
                if self.__map_of_numbers[row][col] == '*':
                    self.__map_of_numbers[row][col] = -2
                elif self.__map_of_numbers[row][col] == ' ':
                    self.__map_of_numbers[row][col] = -1
                else:
                    print("\033[31m{}".format("Карта не валидна"), "\033[39m")
                    self.__is_map_valid = False
                    return

        # Если координаты вне поля
        if not (0 <= self.__turtle_coordinates[0] <= len(self.__map_of_numbers) - 1) or \
                not (0 <= self.__turtle_coordinates[1] <= len(self.__map_of_numbers[0]) - 1) or \
                (self.__map_of_numbers[self.__turtle_coordinates[0]][self.__turtle_coordinates[1]] == -2):
            print("\033[31m{}".format("Карта не валидна"), "\033[39m")
            self.__is_map_valid = False
            return

        # Если черепаха уже на выходе
        if self.__turtle_coordinates[0] == len(
                self.__map_of_numbers) - 1 or \
                self.__turtle_coordinates[1] == len(
            self.__map_of_numbers[0]) - 1 or \
                (self.__turtle_coordinates[0] == 0) or \
                (self.__turtle_coordinates[1] == 0):

            self.__minimum_steps_amount = 1
            self.__out_point_row = self.__turtle_coordinates[0]
            self.__out_point_col = self.__turtle_coordinates[1]
            self.__graphics_map[self.__turtle_coordinates[0]][
                self.__turtle_coordinates[1]] = self.__turtle_char

            return

        self.__map_of_numbers[self.__turtle_coordinates[0]][
            self.__turtle_coordinates[1]] = 1  # Устанавливаем черепаху

        while self.__queue:  # Добавить все еденицы прохода в очередь
            current_position = self.__queue.pop(0)
            self.__add_to_queue(
                current_position,
                current_position[0] + 1,
                current_position[1]
            )
            self.__add_to_queue(
                current_position,
                current_position[0] - 1,
                current_position[1]
            )
            self.__add_to_queue(
                current_position,
                current_position[0],
                current_position[1] + 1
            )
            self.__add_to_queue(
                current_position,
                current_position[0],
                current_position[1] - 1
            )
        self.__reverse_path(self.__out_point_row, self.__out_point_col)

    def __add_to_queue(
            self, current_position, row, col, *args, **kwargs
    ) -> None:
        if not self.__is_map_valid:
            return
        try:
            if not (0 <= row <= len(self.__map_of_numbers) - 1) or \
                    not (0 <= col <= len(self.__map_of_numbers[0]) - 1) or \
                    self.__map_of_numbers[row][col] == -2:
                return
        except IndexError:
            print("Вы пытаетесь сломать программу? Карта неправильная")
            self.__is_map_valid = False
            return

        if self.__map_of_numbers[row][col] == -1 or \
                self.__map_of_numbers[row][col] > \
                self.__map_of_numbers[current_position[0]][
                    current_position[1]] + 1:
            self.__map_of_numbers[row][col] = self.__map_of_numbers[
                                                  current_position[0]
                                              ][
                                                  current_position[1]
                                              ] + 1
            self.__queue.append((row, col))
        if (row == 0 or row == len(self.__map_of_numbers) - 1 or
            col == 0 or col == len(self.__map_of_numbers[0]) - 1) and \
                (self.__minimum_steps_amount == -1 or
                 self.__map_of_numbers[row][
                     col] < self.__minimum_steps_amount):  # Мы нашли выход
            self.__minimum_steps_amount = self.__map_of_numbers[row][col]
            self.__out_point_row = row
            self.__out_point_col = col

    def __reverse_path(self, row, col, *args, **kwargs) -> None:

        if self.__minimum_steps_amount == -1:
            self.__is_map_valid = False
            return None

        self.__graphics_map[row][col] = self.__way_char
        if row == 0:
            row += 1
            self.__way_word_description.append(0)
            self.__way_word_description.append(0)
        elif col == 0:
            col += 1
            self.__way_word_description.append(270)
            self.__way_word_description.append(270)
        elif row == len(self.__map_of_numbers) - 1:
            row -= 1
            self.__way_word_description.append(180)
            self.__way_word_description.append(180)
        else:
            col -= 1
            self.__way_word_description.append(90)
            self.__way_word_description.append(90)

        while 1:
            self.__graphics_map[row][col] = self.__way_char

            if self.__map_of_numbers[row + 1][col] == \
                    self.__map_of_numbers[row][col] - 1:
                row += 1
                self.__way_word_description.append(0)

            elif self.__map_of_numbers[row - 1][col] == \
                    self.__map_of_numbers[row][col] - 1:
                row -= 1
                self.__way_word_description.append(180)

            elif self.__map_of_numbers[row][col + 1] == \
                    self.__map_of_numbers[row][col] - 1:
                col += 1
                self.__way_word_description.append(270)

            elif self.__map_of_numbers[row][col - 1] == \
                    self.__map_of_numbers[row][col] - 1:
                col -= 1
                self.__way_word_description.append(90)

            if self.__map_of_numbers[row][col] == 1:
                break

        self.__graphics_map[self.__turtle_coordinates[0]][
            self.__turtle_coordinates[1]] = self.__turtle_char


test = LabirintTurtle()
test.load_map('hard_test.txt')
test.exit_show_step()
test.exit_count_step()
test.describe_turtle_path()
