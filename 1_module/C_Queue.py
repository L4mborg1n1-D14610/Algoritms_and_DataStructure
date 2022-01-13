import sys


class Queue(object):
    def __init__(self, size, file):
        self.__massive = [0] * size
        self.__size = size
        self.__head = -1
        self.__tail = -1
        self.__file = file

    def print_queue(self):
        if self.__head - self.__tail > 0:
            for number in range(self.__head - self.__tail):
                self.__file.write(str(self.__massive[number + self.__tail]) + ' ')
            self.__file.write(str(self.__massive[self.__head]) + '\n')
        elif self.__head - self.__tail < 0:
            for number in range(self.__size - self.__tail):
                self.__file.write(str(self.__massive[number + self.__tail]) + ' ')
            for number in range(self.__head):
                self.__file.write(str(self.__massive[number]) + ' ')
            self.__file.write(str(self.__massive[self.__head]) + '\n')
        elif self.__tail == -1:
            self.__file.write("empty\n")
        else: # one element in massive
            self.__file.write(str(self.__massive[self.__tail]) + '\n')

    def pop(self):
        if self.__tail == -1:
            self.__file.write("underflow\n")
            return
        self.__file.write(str(self.__massive[self.__tail]) + '\n')
        self.__massive[self.__tail] = 0
        if self.__head == self.__tail:
            self.__head = -1
            self.__tail = -1
        else:
            self.__tail += 1
        if self.__tail == self.__size:
            self.__tail = 0
        return

    def push(self, x):
        self.__head += 1
        if (self.__head == self.__tail) \
                | ((self.__tail == 0) & (self.__head == self.__size)):
            self.__file.write("overflow\n")
            self.__head -= 1
            return
        if self.__head == self.__size:
            self.__head = 0
        if self.__tail == -1:
            self.__tail = 0
        self.__massive[self.__head] = x
        return


test_file = open(sys.argv[1], 'r')
answer_file = open(sys.argv[2], 'w')
size = 0
for line in test_file:
    try:
        line = line.rstrip("\n")
        if ("set_size " in line) & (line[9:].isdigit()):
            size = int(line[9:])
            break
        elif line == '':
            continue
        else:
            answer_file.write("error\n")
    except EOFError:
        test_file.close()
        sys.exit()

try:
    queue = Queue(size, answer_file)
except:
    answer_file.write("error\n")
    answer_file.close()
    test_file.close()
    sys.exit()

for line in test_file:
    try:
        line = line.rstrip("\n")
        if line == '':
            continue
        elif line == "pop":
            queue.pop()
        elif line == "print":
            queue.print_queue()
        elif "push " in line:
            if " " in line[5:]:
                answer_file.write("error\n")
            else:
                queue.push(line[5:])
        else:
            answer_file.write("error\n")
    except EOFError:
        test_file.close()
        answer_file.close()
        sys.exit()
