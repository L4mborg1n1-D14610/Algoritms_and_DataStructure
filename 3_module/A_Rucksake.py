import math


class Node:
    def __init__(self, size: int, len_items: int):
        self.values = [[0] * (size + 1) for i in range(len_items)]
        self.optimal_row = 0
        self.optimal_value = 0


class Backpack:
    def __init__(self, size: int):
        self.__size = size
        self.__weights = []
        self.__values = []

    def add(self, weight: int, value: int):
        self.__weights.append(weight)
        self.__values.append(value)

    def __make_gcd(self):
        nod = self.__size
        for el_ in self.__weights:
            nod = math.gcd(nod, el_)
        if nod != 1:
            self.__size = int(self.__size / nod)
            i = 0
            while i < len(self.__weights):
                self.__weights[i] = int(self.__weights[i] / nod)
                i += 1
        return int(nod)

    def max_value(self):
        if self.__size == 0:
            i = 0
            weight = 0
            value = 0
            items = list()
            while i < len(self.__weights):
                if self.__weights[i] == 0:
                    weight += self.__weights[i]
                    value += self.__values[i]
                    items.append(i + 1)
                i += 1
            return weight, value, items

        # будем заполнять массив стоимостью оптимального набора вещей
        # при этом будем рассматривать веса рюкзака от 1 до size
        # а набор вещей будет размера от 1 до len(elements)
        # полный массив должен быть размера len(elements) x size, однако мы будем хранить в памяти много лишнего
        # например, для заполнения новой строчки массива нам нужна информация только о предыдущей его строчке
        # поэтому достаточно массива размера 2 х size, а строки будем просто перезаписывать
        # также можно сократить длинну масива, если НОД всех весов и размера самого рюкзака больше 1
        # пропорционально уменьшив длину массива
        # Однако встаёт проблема с выводом элементов, которые составляют оптимальный набор
        # Вариантов несколько: будем сразу хранить необходимые элементы, но тогда надо хранить элементы для каждой
        # ячейки таблицы в том или ином виде. Получается трёхмерный массив размера 2 x backpack_size х len(elements)
        # Второй вариант: восстанавливаем по таблице набор предметов, но тогда придется хранить всю таблицу размером
        # backpack_size x len(elements). Второй вариант более оптимальный по памяти. Им и воспользуемся

        nod = self.__make_gcd()
        node = Node(self.__size, len(self.__weights))
        i = 0
        while i < len(self.__weights):
            j = 0
            while j <= self.__size:
                if i == 0:
                    if self.__weights[i] <= j:
                        node.values[i][j] = self.__values[i]
                elif (j - self.__weights[i]) < 0:
                    node.values[i][j] = node.values[i - 1][j]
                elif int(node.values[i - 1][j]) > self.__values[i] + node.values[i - 1][j - self.__weights[i]]:
                    node.values[i][j] = node.values[i - 1][j]
                else:
                    node.values[i][j] = self.__values[i] + node.values[i - 1][j - self.__weights[i]]
                j += 1
            if node.values[i][j - 1] > node.optimal_value:
                node.optimal_value = node.values[i][j - 1]
                node.optimal_row = i
            i += 1
        weight = 0
        i = node.optimal_row  # для итерации по строкам node.values
        j = self.__size  # для итерации по столбцам node.values
        # итерироваться будем с конца
        items = list()
        while i >= 0:
            if node.values[i][j] == 0:
                break
            if i == 0:
                if len(items) == 0:
                    items.append(i + 1)
                    weight += self.__weights[i]
                elif items[-1] != (i + 1):
                    items.append(i + 1)
                    weight += self.__weights[i]
            if node.values[i][j] != node.values[i-1][j]:
                if len(items) == 0:  # чтобы избежать повторного пуша
                    items.append(i + 1)
                    weight += self.__weights[i]
                elif items[-1] != (i + 1):
                    items.append(i + 1)
                    weight += self.__weights[i]
                j -= self.__weights[i]
            i -= 1
        weight *= nod
        return weight, node.optimal_value, reversed(items)


pack_size = 0
while True:
    line = input()
    if len(line) == 0:
        continue
    else:
        if line.isnumeric():
            pack_size = line
            break
        else:
            print("error")
            continue

pack = Backpack(int(line))
while True:
    try:
        line = input().split()
        if len(line) == 0:
            continue
        elif len(line) != 2:
            print("error")
            continue
        elif line[0].isnumeric() & line[1].isnumeric():
            pack.add(int(line[0]), int(line[1]))
        elif line[0] == "k":
            pack.max_value()
        else:
            print("error")
    except EOFError:
        break

answer = pack.max_value()
print(answer[0], answer[1])
for el in answer[2]:
    print(el)
