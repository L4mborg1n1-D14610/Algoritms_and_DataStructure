from collections import deque


class Node:
    def __init__(self, key: int, value):
        self.key = key
        self.value = value


class Heap:
    def __init__(self):
        self.data = list()  # list of nodes
        self.size = 0
        self.keys = dict()  # index-key

    def __swap_list(self, i, j):
        get = self.data[i], self.data[j]
        self.data[j], self.data[i] = get

    def __swap_dict(self, key1, key2):
        get = self.keys[key1], self.keys[key2]
        self.keys[key2], self.keys[key1] = get

    def __heapify(self, i):
        left = self.__left(i)
        right = self.__right(i)
        if left >= self.size:
            return
        if self.data[left].key < self.data[i].key:
            smallest = left
        else:
            smallest = i
        if right < self.size:
            if self.data[right].key < self.data[smallest].key:
                smallest = right
        if smallest != i:
            self.__swap_list(i, smallest)
            self.__swap_dict(self.data[i].key, self.data[smallest].key)
            self.__heapify(smallest)

    def __heapify_up(self, i):
        if self.data[i].key < self.data[self.__parent(i)].key:
            self.__swap_list(i, self.__parent(i))
            self.__swap_dict(self.data[i].key, self.data[self.__parent(i)].key)
            self.__heapify_up(self.__parent(i))

    @staticmethod
    def __left(i):
        return 2 * i + 1

    @staticmethod
    def __right(i):
        return 2 * i + 2

    @staticmethod
    def __parent(i):
        return int((i - 1) / 2)

    def add(self, key: int, value):
        if len(self.data) == 0:
            self.data.append(Node(key, value))
            self.keys[key] = 0
            self.size += 1
            return
        if key in self.keys:
            raise Exception('error')
        self.size += 1
        i = self.size - 1
        self.data.append(None)
        while (i > 0) & (self.data[self.__parent(i)].key > key):
            self.data[i] = self.data[self.__parent(i)]
            self.keys[self.data[i].key] = i
            i = self.__parent(i)
        self.data[i] = Node(key, value)
        self.keys[key] = i

    def set(self, key, value):
        if key not in self.keys:
            raise Exception('error')
        i = self.keys[key]
        self.data[i].value = value

    def delete(self, key):
        if key not in self.keys:
            raise Exception('error')
        i = self.keys[key]
        self.size -= 1
        if (i == self.size) | (self.size == 0):
            del self.keys[key]
            del self.data[-1]
            return
        del self.keys[key]
        self.data[i] = self.data[self.size]
        self.keys[self.data[i].key] = i
        del self.data[-1]
        if i < self.size:
            self.__heapify_up(i)
        self.__heapify(i)

    def search(self, key):
        if key not in self.keys:
            return None
        i = self.keys[key]
        return self.data[i], i

    def min(self):
        if self.size > 0:
            return self.data[0]
        else:
            raise Exception('error')

    def max(self):
        if self.size > 0:
            i = self.__parent(self.size - 1) + 1  # первый лист
            max_index = i
            max_element = self.data[i]
            i += 1
            while i < self.size:
                if max_element.key < self.data[i].key:
                    max_element = self.data[i]
                    max_index = i
                i += 1
            return max_element, max_index
        else:
            raise Exception('error')

    def extract(self):
        if self.size == 0:
            raise Exception('error')
        min_node = self.data[0]
        self.data[0] = self.data[self.size - 1]
        self.keys[self.data[0].key] = 1
        self.size -= 1
        del self.data[self.size]
        del self.keys[min_node.key]
        self.__heapify(0)
        return min_node

    def get_heap(self):
        heap_deque = deque()
        if self.size == 0:
            heap_deque.append("_")
            return heap_deque
        heap_deque.append("[" + str(self.data[0].key) + ' ' + str(self.data[0].value) + "]")
        if self.size == 1:
            return heap_deque
        right_node = 4
        i = 1
        level = ""
        while i < self.size:
            level += ("[" + str(self.data[i].key) + ' ' + self.data[i].value
                      + ' ' + str(self.data[self.__parent(i)].key) + "] ")
            if i == self.size - 1:
                level += "_ " * (right_node - i - 2)
                heap_deque.append(level[:-1])
                break
            if i == right_node - 2:
                heap_deque.append(level[:-1])
                level = ""
                right_node *= 2
            i += 1
        return heap_deque


heap = Heap()
while True:
    try:
        line = input().split()
        if len(line) == 0:
            continue
        elif line[0] == "add":
            try:
                heap.add(int(line[1]), line[2])
            except Exception as e:
                print(e)
        elif line[0] == "set":
            try:
                heap.set(int(line[1]), line[2])
            except Exception as e:
                print(e)
        elif line[0] == "delete":
            try:
                heap.delete(int(line[1]))
            except Exception as e:
                print(e)
        elif line[0] == "search":
            element = heap.search(int(line[1]))
            if element is None:
                print(0)
            else:
                print("1", element[1], element[0].value)
        elif line[0] == "min":
            try:
                min_el = heap.min()
                print(min_el.key, "0", min_el.value)
            except Exception as e:
                print(e)
        elif line[0] == "max":
            try:
                max_el = heap.max()
                print(max_el[0].key, max_el[1], max_el[0].value)
            except Exception as e:
                print(e)
        elif line[0] == "extract":
            try:
                element = heap.extract()
                print(element.key, element.value)
            except Exception as e:
                print(e)
        elif line[0] == "print":
            deq = heap.get_heap()
            while deq:  # not empty
                print(deq.popleft())
        else:
            print("error")
    except EOFError:
        break
