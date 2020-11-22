import time


class LabirintTurtle:
    def __init__(self):
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

    def load_map(self, file_name) -> None:
        try:
            file_with_map = open(file_name, 'rt')
            field_with_coordinates = file_with_map.read()
        except TypeError:
            print("Неправильное название файла, загрузите другой файл")
        except FileNotFoundError:
            print("Файл не найден, загрузите другой файл")
        except UnicodeDecodeError:
            print("Некорректные данные файла")

        self.__parse_map_from_file(field_with_coordinates)

    def show_map(self, turtle: bool = False) -> None:
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

    def check_map(self) -> None:
        ''' Проверка карты на валидность '''
        if __is_map_valid:
            print("Карта валидна")
        else:
            print("Карта не валидна, введите другую")

    def exit_count_step(self) -> None:
        if not self.__is_map_valid:
            print("Карта не валидна")
            return

        print("Минимальное количество ходов - ", self.__minimum_steps_amount)

    def exit_show_step(self) -> None:
        if not self.__is_map_valid:
            print("Карта не валидна")
            return
        for i in self.__graphics_map:
            print(*i, sep='\t')

    def __parse_map_from_file(self, field_with_coordinates):

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

        # Если черепаха уже на выходе
        if self.__turtle_coordinates[0] == len(self.__map_of_numbers) - 1 or \
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

        self.__queue = [self.__turtle_coordinates]

        for row in range(len(self.__map_of_numbers)):
            for col in range(len(self.__map_of_numbers[row])):
                if self.__map_of_numbers[row][col] == '*':
                    self.__map_of_numbers[row][col] = -2
                elif self.__map_of_numbers[row][col] == ' ':
                    self.__map_of_numbers[row][col] = -1
                else:
                    print("Неправильный символ")
                    return

        # Если координаты вне поля
        if not (0 <= self.__turtle_coordinates[0] <= len(
                self.__map_of_numbers) - 1) or \
                not (0 <= self.__turtle_coordinates[1] <= len(
                    self.__map_of_numbers[0]) - 1) or \
                self.__map_of_numbers[self.__turtle_coordinates[0]][
                    self.__turtle_coordinates[1]] == -2:
            print("Карта не валидна")
            self.__is_map_valid = False
            return

        self.__map_of_numbers[self.__turtle_coordinates[0]][
            self.__turtle_coordinates[1]] = 1

        while self.__queue:
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

    def __add_to_queue(self, current_position, row, col) -> None:
        if not self.__is_map_valid:
            return
        try:
            if not (0 <= row <= len(self.__map_of_numbers) - 1) or \
                    not (0 <= col <= len(self.__map_of_numbers[0]) - 1) or \
                    self.__map_of_numbers[row][col] == -2:
                return
        except IndexError:
            print("Вы пытаетесь сломать программу?")
            self.__is_map_valid = False
            return

        if self.__map_of_numbers[row][col] == -1 or \
                self.__map_of_numbers[row][col] > \
                self.__map_of_numbers[current_position[0]][
                    current_position[1]] + 1:
            self.__map_of_numbers[row][col] = \
            self.__map_of_numbers[current_position[0]][current_position[1]] + 1
            self.__queue.append((row, col))
        if (row == 0 or row == len(self.__map_of_numbers) - 1 or \
            col == 0 or col == len(self.__map_of_numbers[0]) - 1) and \
                (self.__minimum_steps_amount == -1 or
                 self.__map_of_numbers[row][
                     col] < self.__minimum_steps_amount):  # Мы нашли выход
            self.__minimum_steps_amount = self.__map_of_numbers[row][col]
            self.__out_point_row = row
            self.__out_point_col = col

    def __reverse_path(self, row, col) -> None:

        if self.__minimum_steps_amount == -1:
            self.__is_map_valid = False
            return None

        self.__graphics_map[row][col] = self.__way_char
        if row == 0:
            row += 1
        elif col == 0:
            col += 1
        elif row == len(self.__map_of_numbers) - 1:
            row -= 1
        else:
            col -= 1
        while self.__map_of_numbers[row][col] != 1:
            self.__graphics_map[row][col] = self.__way_char

            if self.__map_of_numbers[row + 1][col] == \
                    self.__map_of_numbers[row][col] - 1:
                row += 1
            elif self.__map_of_numbers[row - 1][col] == \
                    self.__map_of_numbers[row][col] - 1:
                row -= 1
            elif self.__map_of_numbers[row][col + 1] == \
                    self.__map_of_numbers[row][col] - 1:
                col += 1
            elif self.__map_of_numbers[row][col - 1] == \
                    self.__map_of_numbers[row][col] - 1:
                col -= 1

        self.__graphics_map[self.__turtle_coordinates[0]][
            self.__turtle_coordinates[1]] = self.__turtle_char
