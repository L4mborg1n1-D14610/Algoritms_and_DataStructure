from collections import deque


class SplayTree:
    def __init__(self):
        self.root = None

    def __left_rotate(self, parent_node):
        node = parent_node.right
        parent_node.right = node.left
        if node.left is not None:
            node.left.parent = parent_node
        node.parent = parent_node.parent
        if parent_node.parent is None:
            self.root = node
        elif parent_node is parent_node.parent.left:
            parent_node.parent.left = node
        else:
            parent_node.parent.right = node
        node.left = parent_node
        parent_node.parent = node

    def __right_rotate(self, parent_node):
        node = parent_node.left
        parent_node.left = node.right
        if node.right is not None:
            node.right.parent = parent_node
        node.parent = parent_node.parent
        if parent_node.parent is None:
            self.root = node
        elif parent_node is parent_node.parent.left:
            parent_node.parent.left = node
        else:
            parent_node.parent.right = node
        node.right = parent_node
        parent_node.parent = node

    def __splay(self, node):
        while node is not self.root:
            if node.parent is self.root:
                if node is node.parent.left:
                    self.__right_rotate(node.parent)
                    return
                else:
                    self.__left_rotate(node.parent)
                    return
            elif node is node.parent.left and node.parent is node.parent.parent.left:
                self.__right_rotate(node.parent.parent)
                self.__right_rotate(node.parent)
            elif node is node.parent.right and node.parent is node.parent.parent.right:
                self.__left_rotate(node.parent.parent)
                self.__left_rotate(node.parent)
            elif node is node.parent.left and node.parent is node.parent.parent.right:
                self.__right_rotate(node.parent)
                self.__left_rotate(node.parent)
            else:
                self.__left_rotate(node.parent)
                self.__right_rotate(node.parent)

    def __search_by_key(self, key, node):
        if self.root is None:
            return None
        while node.key != key:
            if key < node.key:
                if node.left is not None:
                    node = node.left
                else:
                    self.__splay(node)
                    return None
            else:
                if node.right is not None:
                    node = node.right
                else:
                    self.__splay(node)
                    return None
        return node

    def add(self, key, value):
        if self.root is None:
            self.root = Node(key, value, None)
            return
        else:
            node = self.root
            while node.key is not None:
                if key == node.key:
                    self.__splay(node)
                    raise Exception('error')
                if key < node.key:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = Node(key, value, node)
                        self.__splay(node.left)
                        return
                else:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = Node(key, value, node)
                        self.__splay(node.right)
                        return

    def set(self, key, value):
        node = self.__search_by_key(key, self.root)
        if node is not None:
            node.value = value
            self.__splay(node)
        else:
            raise Exception('error')

    def delete(self, key):
        node = self.__search_by_key(key, self.root)
        if node is not None:
            self.__splay(node)
            if self.root.right is None and self.root.left is None:
                self.root = None
            elif self.root.right is None:
                self.root.left.parent = None
                self.root = self.root.left
            elif self.root.left is None:
                self.root.right.parent = None
                self.root = self.root.right
            else:
                right_tree = self.root.right
                self.root.left.parent = None
                self.root = self.root.left
                self.max()
                self.root.right = right_tree
                right_tree.parent = self.root
        else:
            raise Exception('error')

    def search(self, key):
        if self.root is None:
            return None
        else:
            node = self.root
            while node.key != key:
                if key < node.key:
                    if node.left is None:
                        self.__splay(node)
                        return None
                    else:
                        node = node.left
                else:
                    if node.right is None:
                        self.__splay(node)
                        return None
                    else:
                        node = node.right
            self.__splay(node)
            return node

    def min(self):
        if self.root is None:
            raise Exception('error')
        else:
            node = self.root
            while node is not None:
                if node.left is None:
                    self.__splay(node)
                    return node
                else:
                    node = node.left

    def max(self):
        if self.root is None:
            raise Exception('error')
        else:
            node = self.root
            while node is not None:
                if node.right is None:
                    self.__splay(node)
                    return node
                else:
                    node = node.right

    def get_tree(self):
        tree_deq = deque()
        if self.root is None:
            tree_deq.append('_')
            return tree_deq
        deq = deque()
        deq.append(self.root)
        pow_counter = 1  # счётчик числа вершин на данном уровне
        while len(deq) > 0:
            counter = 1
            level = ""
            flag = True
            while pow_counter >= counter:
                node = deq.popleft()
                if node is None:
                    level += "_ "
                    deq.append(2)
                    counter += 1
                elif type(node) is int:
                    level += "_ " * int(node)
                    counter += node
                    node *= 2
                    deq.append(node)
                else:
                    flag = False
                    deq.append(node.left)
                    deq.append(node.right)
                    level += "[" + str(node.key) + " " + str(node.value)
                    if node.parent is None:
                        level += "] "
                    else:
                        level += " " + str(node.parent.key) + "] "
                    counter += 1
            if flag:
                break
            tree_deq.append(level[:-1])
            pow_counter *= 2
        return tree_deq


class Node:
    def __init__(self, key: int, value, parent_node):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.parent = parent_node


Tree = SplayTree()
while True:
    try:
        line = input().split()
        if len(line) == 0:
            continue
        elif line[0] == "add":
            try:
                Tree.add(int(line[1]), line[2])
            except Exception as e:
                print(e)
        elif line[0] == "set":
            try:
                Tree.set(int(line[1]), line[2])
            except Exception as e:
                print(e)
        elif line[0] == "delete":
            try:
                Tree.delete(int(line[1]))
            except Exception as e:
                print(e)
        elif line[0] == "search":
            element = Tree.search(int(line[1]))
            if element is None:
                print(0)
            else:
                print("1", element.value)
        elif line[0] == "min":
            try:
                min_el = Tree.min()
                print(min_el.key, min_el.value)
            except Exception as e:
                print(e)
        elif line[0] == "max":
            try:
                max_el = Tree.max()
                print(max_el.key, max_el.value)
            except Exception as e:
                print(e)
        elif line[0] == "print":
            print_deq = Tree.get_tree()
            while print_deq:  # not empty
                print(print_deq.popleft())
        else:
            print("error")
    except EOFError:
        break
