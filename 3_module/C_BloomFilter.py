import math
from sys import exit

# итак, n - приблизительное число элементов в массиве, P - вероятность ложноположительного ответа, тогда размер
# структуры m = -(nlog2P) / ln2 (2 - основание), количество хеш-функций будет равно -log2P
# хеш-функции используются вида: (((i + 1)*x + p(i+1)) mod M) mod m,где - x - ключ, i - номер хэш-функции,
# pi - i-тое по счету простое число, а M - 31ое число Мерсенна, M = 2^31 - 1, M = 2 147 483 647, M - простое число.

# При подсчёте хеш-функций необходимо знать первые k простых чисел. Посчитаем их один раз в конструкторе BloomFilter
# и будем хранить в структуре данных.
# Также нам необходимо создать битовый массив размера m, однако по умолчанию в питоне битовый массив отсутствует,
# поэтому будем использовать байтовый массив. Реализуем для удобства отдельную СД, из методов необходимо: изменить
# указанный бит на 1, проверить является ли указанный бит 1 и напечатать (вернуть) сам массив

Mersen_31 = 2147483647


class BitArray:
    def __init__(self, size):
        self.__array = bytearray(int(math.ceil(size / 8)))
        self.__size = size

    def add_bit(self, i):
        # i-тый бит содержится в i//8 байте на i % 8 месте
        self.__array[i // 8] |= 2 ** (7 - (i % 8))

    def check_bit(self, i):
        if (self.__array[i // 8] & (2 ** (7 - (i % 8)))) == 0:
            return False
        else:
            return True

    def print(self):
        array_str = ""
        for byte in self.__array:
            _line = str(bin(byte))[2:]
            if len(_line) != 8:
                _line = '0' * (8 - len(_line)) + _line
            array_str += _line
        return array_str[:self.__size]


class BloomFilter:
    def __init__(self, n: int, p: float):
        self.size = int(-round(n * math.log2(p) / math.log(2)))
        self.hash_numbers = int(-round(math.log2(p)))
        self.__prime_numbers = list()
        self.__get_prime(self.hash_numbers + 1)
        self.__bitarray = BitArray(self.size)

    def __get_prime(self, prime_size):
        # обычный проход по всем числам и их проверка на простоту - сложно по времени
        # немного упростим: во-первых будем идти с интервалом 2, начиная от 3, а после новое число проверять на
        # делимость на уже найденные простые числа (кроме двойки, мы же рассматриваем нечётные)
        if prime_size == 1:
            self.__prime_numbers.append(2)
            return
        self.__prime_numbers.append(2)
        i = 3
        while len(self.__prime_numbers) < prime_size:
            j = 1
            prime_flag = True
            while j < len(self.__prime_numbers):
                if (i % self.__prime_numbers[j]) == 0:
                    prime_flag = False
                    break
                j += 1
            if prime_flag:
                self.__prime_numbers.append(i)
            i += 2

    def __get_hash(self, x, i):
        return (((i + 1) * x + self.__prime_numbers[i]) % Mersen_31) % self.size

    def add(self, key: int):
        i = 0
        while i < self.hash_numbers:
            self.__bitarray.add_bit(self.__get_hash(key, i))
            i += 1

    def search(self, key: int):
        i = 0
        while i < self.hash_numbers:
            if not self.__bitarray.check_bit(self.__get_hash(key, i)):
                return False
            i += 1
        return True

    def print(self):
        return self.__bitarray.print()


bloom_filter = 0

while True:
    try:
        line = input().split()
        if len(line) == 0:
            continue
        else:
            if line[0] == "set":
                try:
                    elements_number = int(line[1])
                    probability = float(line[2])
                    if (elements_number <= 0) | (probability <= 0) | (probability >= 1):
                        print("error")
                        continue
                    bloom_filter = BloomFilter(elements_number, probability)
                    if (bloom_filter.size == 0) | (bloom_filter.hash_numbers == 0):
                        print("error")
                        continue
                    break
                except TypeError:
                    print("error")
                    continue
            else:
                print("error")
                continue
    except EOFError:
        exit()

print(bloom_filter.size, bloom_filter.hash_numbers)

while True:
    try:
        line = input().split()
        if len(line) == 0:
            continue
        elif line[0] == "print":
            print(bloom_filter.print())
        elif (line[0] == "add") & (line[1].isnumeric()):
            bloom_filter.add(int(line[1]))
        elif (line[0] == "search") & (line[1].isnumeric()):
            print(int(bloom_filter.search(int(line[1]))))
        else:
            print("error")
    except EOFError:
        break
