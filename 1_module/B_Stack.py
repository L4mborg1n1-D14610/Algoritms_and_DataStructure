import sys


class Stack(object):

    def __init__(self, size):
        self.massive = [0] * size
        self.size = size
        self.top = 0

    def print_stack(self):
        if self.top > 0:
            for number in range(self.top - 1):
                print(self.massive[number], end=" ")
            print(self.massive[self.top - 1])
        else:
            print("empty")

    def pop(self):
        if self.top == 0:
            print("underflow")
            return
        self.top -= 1
        print(self.massive[self.top])
        self.massive[self.top] = 0
        return

    def push(self, x):
        if self.top == self.size:
            print("overflow")
            return
        self.massive[self.top] = x
        self.top += 1
        return


while True:
    try:
        line = input().strip()
        if ("set_size " in line) & (line[9:].isdigit()):
            break
        elif line == '':
            continue
        else:
            print("error")
    except EOFError:
        sys.exit()

try:
    stack = Stack(int(line[9:]))
except:
    print("error")
    sys.exit()
while True:
    try:
        line = input().rstrip('\n')
        if line == '':
            continue
        elif line == "pop":
            stack.pop()
        elif line == "print":
            stack.print_stack()
        elif "push " in line:
            if " " in line[5:]:
                print("error")
            else:
                stack.push(line[5:])
        else:
            print("error")
    except EOFError:
        break
