import random

# Класс точки с координатами. Проверка что точка находится в пределах игрового поля находится в конструкторе. Путем
# путем вызова исколючения,которое будет обработано при ее создании
class Dot:
    def __init__(self, x, y):
        if x not in range (0, 6) or y not in range(0, 6):
            raise IndexError
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __str__(self):
        return f'{self.__x}, {self.__y} |'

    def __eq__(self, other):
        return self.__x == other.x and self.__y == other.y

# Класс корабля, который получает в конструкторе точку с координатами и хранит их во внутреннем списке
class SheepLvl1:
    def __init__(self, dot1):
        self._coordinates = [dot1]
        self._hp = 1

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def hp(self):
        return self._hp

    def get_attacked(self, dot):
        if dot in self._coordinates:
            self._hp -= 1

# Корабли можно размещать не только слева направо и сверху вниз, но и наоборот. Проверка того, чтобы переданные точки с
# координатами валидны происходит в конструкторе и в случае, если нет, то вызыввается исключение, которое будет
# обработано при создании корабля: классом Player - будет предложено ввести коорданты корабля заново, а классом Bot
# сгенерировать новые координаты, которые не будут вызывать исключения
class Sheeplvl2(SheepLvl1):
    def __init__(self, dot1, dot2):
        super().__init__(dot1)
        if not (dot1.x == dot2.x and (dot1.y == dot2.y + 1 or dot1.y == dot2.y - 1)):
            if not (dot1.y == dot2.y and (dot1.x == dot2.x + 1 or dot1.x == dot2.x - 1)):
                raise ValueError
        self._coordinates.append(dot2)
        self._hp += 1

class SheepLvl3(Sheeplvl2):
    def __init__(self, dot1, dot2, dot3):
        super().__init__(dot1, dot2)
        if dot1.x == dot2.x:
            if not (dot1.x == dot3.x):
                raise ValueError
            if dot1.y == dot2.y + 1:
                if not (dot2.y == dot3.y + 1):
                    raise ValueError
            if dot1.y == dot2.y - 1:
                if not (dot2.y == dot3.y - 1):
                    raise ValueError
        if dot1.y == dot2.y:
            if not (dot1.y == dot3.y):
                raise ValueError
            if dot1.x == dot2.x + 1:
                if not (dot2.x == dot3.x + 1):
                    raise ValueError
            if dot1.x == dot2.x - 1:
                if not (dot2.x == dot3.x - 1):
                    raise ValueError
        self._coordinates.append(dot3)
        self._hp += 1

# Класс отвечающий за вывод игрового поля. Получает в конструкторе список кораблей и формирует внутренний массив,
# который выводит по запросу. У игрока и бота два таких поля: одно поле со своими кораблями, а второе то как игрок
# или бот видят поле противника
class GameField:
    FREE_CELL = '0'
    SHEEP = "■"
    MISS = "T"
    DESTROYED = "X"
    def __init__(self, sheeps_list):
        self.__height = 6
        self.__weight = 6
        self.initialize_field()
        self.__shoted_cells = []
        for sheep in sheeps_list:
            for dot in sheep.coordinates:
                self.__gameField[dot.x][dot.y] = self.SHEEP

    def initialize_field(self):
        self.__gameField = [[self.FREE_CELL for element in range(self.__height)] for cow in range(self.__weight)]

    def set_dot_status_miss(self, dot):
        self.__gameField[dot.x][dot.y] = self.MISS
        self.__shoted_cells.append(dot)

    def set_dot_status_hit(self, dot):
        self.__gameField[dot.x][dot.y] = self.DESTROYED
        self.__shoted_cells.append(dot)

    @property
    def shoted_cells(self):
        return self.__shoted_cells

    def show_field(self):
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i, cow in enumerate(self.__gameField):
            print(f'{i + 1} |', end='')
            for element in cow:
                print('', element, '|', end='')
            print()

class Player():
    def __init__(self):
        self._count_lvl1sheep = 4
        self._count_lvl2sheep = 2
        self._count_lvl3sheep = 1
        self._occup_coord = []
        self._impos_coord = []
        self._sheeps_list = []
        self._player_field = GameField(self._sheeps_list)
        self._enemy_field = GameField(self._sheeps_list)

# Метод отвечающий за ввод и вызывающий исключение в случае непраавильного ввода
    def input_dot(self):
        coord = input()
        if len(coord) > 2:
            raise ValueError
        x = int(coord[0]) - 1
        y = int(coord[1]) - 1
        return Dot(x, y)

# Метод добавляющий соседние клетки с занятыми кораблями в список
    def occupy_neighbor_cells(self, dot):
        try:
            self._impos_coord.append(Dot(dot.x - 1, dot.y))
        except IndexError:
            pass
        try:
            self._impos_coord.append(Dot(dot.x + 1, dot.y))
        except IndexError:
            pass
        try:
            self._impos_coord.append(Dot(dot.x, dot.y + 1))
        except IndexError:
            pass
        try:
            self._impos_coord.append(Dot(dot.x, dot.y - 1))
        except IndexError:
            pass

# При размещении корабля проверяется, чтобы корабль был не в занятой клетке и не по соседству с другим кораблем.
# Так же в методе обрабытываются исключения, которые могут возникнуть при невалидных координатах корабля (См. классы
# ShipLvl2 и Shiplvl3), исключение неправильного ввода(См. метод input_dot) и исключение, которое может возникнуть, если
# создать обьект класса Dot вне пределах игрового поля
    def place_ships(self):
        for i in range(self._count_lvl1sheep):
            while True:
                try:
                    print("Введите координату одноклеточного корабля:")
                    dot = self.input_dot()
                    if dot in self._occup_coord:
                        raise ValueError
                    if dot in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(SheepLvl1(dot))
                    self._player_field = GameField(self._sheeps_list)
                    self.show_player_field()
                except IndexError:
                    print("Координаты не существует")
                except ValueError:
                    print("Недопустимый ввод. Введите незанятую координату состоящую из двух цифр")
                else:
                    self._occup_coord.extend([dot])
                    self.occupy_neighbor_cells(dot)
                    break
        for i in range(self._count_lvl2sheep):
            while True:
                try:
                    print("Введите первую координату двухклеточного корабля:")
                    dot1 = self.input_dot()
                    if dot1 in self._occup_coord or dot1 in self._impos_coord:
                        raise ValueError
                    print("Введите вторую координату двухклеточного корабля:")
                    dot2 = self.input_dot()
                    if dot2 in self._occup_coord or dot2 in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(Sheeplvl2(dot1, dot2))
                    self._player_field = GameField(self._sheeps_list)
                    self.show_player_field()
                except IndexError:
                    print("Координаты не существует")
                except ValueError:
                    print("Недопустимый ввод. Введите незанятую координату состоящую из двух цифр")
                else:
                    self._occup_coord.extend([dot1, dot2])
                    self.occupy_neighbor_cells(dot1)
                    self.occupy_neighbor_cells(dot2)
                    break
        for i in range(self._count_lvl3sheep):
            while True:
                try:
                    print("Введите первую координату трехклеточного корабля:")
                    dot1 = self.input_dot()
                    if dot1 in self._occup_coord or dot1 in self._impos_coord:
                        raise ValueError
                    print("Введите вторую координату трехклеточного корабля:")
                    dot2 = self.input_dot()
                    if dot2 in self._occup_coord or dot2 in self._impos_coord:
                        raise ValueError
                    print("Введите третью координату трехклеточного корабля:")
                    dot3 = self.input_dot()
                    if dot3 in self._occup_coord or dot3 in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(SheepLvl3(dot1, dot2, dot3))
                    self._player_field = GameField(self._sheeps_list)
                except IndexError:
                    print("Координаты не существует")
                except ValueError:
                    print("Недопустимый ввод. Введите незанятую координату состоящую из двух цифр")
                else:
                    self._occup_coord.extend([dot1, dot2, dot3])
                    self.occupy_neighbor_cells(dot1)
                    self.occupy_neighbor_cells(dot2)
                    self.occupy_neighbor_cells(dot3)
                    break

    def show_player_field(self):
        self._player_field.show_field()

    def show_enemy_field(self):
        self._enemy_field.show_field()

    def shot(self):
        while True:
            try:
                print("Введите координату куда хотите стрельнуть:")
                dot = self.input_dot()
                if dot in self._enemy_field.shoted_cells:
                    raise IndexError
            except IndexError:
                print("Координаты не существует или Вы уже стреляли туда")
            except ValueError:
                print("Координаты не существует")
            else:
                break
        return dot

    def mark_enemy_field(self, mark, dot):
        if mark:
            self._enemy_field.set_dot_status_hit(dot)
        else:
            self._enemy_field.set_dot_status_miss(dot)

# Если игрок атакован, то в случае, если точка принадлежит кораблю, значение его жизни, уменьшается на 1.
    def get_attacked(self, dot):
        if dot in self._occup_coord:
            self._player_field.set_dot_status_hit(dot)
            for sheep in self._sheeps_list:
                sheep.get_attacked(dot)
            return True
        else:
            self._player_field.set_dot_status_miss(dot)

# Игра будет закочена, когда жизни всех кораблей, одного из игроков будут равны 0
    def check_alive_sheeps(self):
        sum = 0
        for sheep in self._sheeps_list:
            sum += sheep.hp
        return sum == 0

# Методы класса Bot аналогичны методам класса Player только ориентированы на случайный ввод
class Bot(Player):
    def input_dot(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)

    def place_ships(self):
        for i in range(self._count_lvl1sheep):
            while True:
                try:
                    dot = self.input_dot()
                    if dot in self._occup_coord or dot in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(SheepLvl1(dot))
                    self._player_field = GameField(self._sheeps_list)
                except ValueError:
                    pass
                else:
                    self._occup_coord.extend([dot])
                    self.occupy_neighbor_cells(dot)
                    break
        for i in range(self._count_lvl2sheep):
            while True:
                try:
                    dot1 = self.input_dot()
                    dot2 = self.input_dot()
                    if dot1 in self._occup_coord or dot2 in self._occup_coord:
                        raise ValueError
                    if dot1 in self._impos_coord or dot2 in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(Sheeplvl2(dot1, dot2))
                    self._player_field = GameField(self._sheeps_list)
                except ValueError:
                    pass
                else:
                    self._occup_coord.extend([dot1, dot2])
                    self.occupy_neighbor_cells(dot1)
                    self.occupy_neighbor_cells(dot2)
                    break
        for i in range(self._count_lvl3sheep):
            while True:
                try:
                    dot1 = self.input_dot()
                    dot2 = self.input_dot()
                    dot3 = self.input_dot()
                    if dot1 in self._occup_coord or dot2 in self._occup_coord or dot3 in self._occup_coord:
                        raise ValueError
                    if dot1 in self._impos_coord or dot2 in self._impos_coord or dot3 in self._impos_coord:
                        raise ValueError
                    self._sheeps_list.append(SheepLvl3(dot1, dot2, dot3))
                    self._player_field = GameField(self._sheeps_list)
                except ValueError:
                    pass
                else:
                    self._occup_coord.extend([dot1, dot2, dot3])
                    self.occupy_neighbor_cells(dot1)
                    self.occupy_neighbor_cells(dot2)
                    self.occupy_neighbor_cells(dot3)
                    break
    def shot(self):
        while True:
            try:
                dot = self.input_dot()
                if dot in self._enemy_field.shoted_cells:
                    raise IndexError
            except IndexError:
                pass
            else:
                break
        print(f'Ваш противник стреляет в клетку с координатами {dot.x+1}:{dot.y+1}')
        return dot

class Gamelogic:
    def __init__(self):
        self.__player = Player()
        self.__bot = Bot()
        self.__player.show_player_field()
        self.__player.place_ships()
        self.__bot.place_ships()

    def do_turn_player(self):
        print("Ваше поле")
        self.__player.show_player_field()
        print("Поле противника")
        self.__player.show_enemy_field()
        dot = self.__player.shot()
        self.__player.mark_enemy_field(self.__bot.get_attacked(dot), dot)

    def do_turn_bot(self):
        dot = self.__bot.shot()
        self.__bot.mark_enemy_field(self.__player.get_attacked(dot), dot)

    def check_win(self):
        if self.__player.check_alive_sheeps():
            print('Вы проиграли:-(')
            return True
        if self.__bot.check_alive_sheeps():
            print('Вы победили!!!')
            return True

if __name__ == "__main__":
    game = Gamelogic()
    while game.check_win() is None:
        game.do_turn_player()
        game.do_turn_bot()

