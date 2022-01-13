# Как работает программа и какова её сложность? (далее сложность - временная) (по памяти - в конце)
# Сложность добавления слова длины m O(m) - побуквенно добавляем слово в
# дерево (или не добавляем часть слова при совпадении префиксов). Далее: пусть добавлено n слов в словарь,
# длина максимального слова m. Рассмотрим сложность в худшем случае: все слова длины m. Сложность составления
# префиксного дерева О(mn).
# Сложность поиска всех слов, расстояние Дамерау-Левенштейна которых отличается от данного ровно на 1.
# Полный алгоритм Дамерау-Левенштейна не реализовывался, так как нас не интересуют слова с расстоянием больше 1.
# У нас есть четыре метода, проверяющие это. Каждый из них вызывает метод сравнения слов, который работает за О(l), где
# l - длина проверяемого слова. 1. Проверка на то, что две буквы поменяли местами имеет сложность O(l)
# 2. Проверка на то, что из слова удалили букву: сложность О(l*k), где k - число детей у данной вершины префиксного
# дерева (в худшем случае k = n), тогда сложность метода - О(l*n).
# 3. Проверка на то, что в слово добавили букву: О(l)
# 4. Проверка на то, что в слове изменили букву: О(l*n)
# Тогда метод, вызывающий в себе все эти четыре метода имеет сложность в худшем случае O(l*n)
# Сам метод вызовется максимально l раз. Тогда сложность проверки слова в худшем случае составит O(l*l*n)
# (при печати ещё делается сортировка, но её сложность несущественна)
# В действительности же зачастую k << n (очень мало слов имеют одинаковый префикс относительно большой длины)
# Предположив, что в среднем k почти константа, тогда сложность проверки одного слова составляет О(l*l)
# Сложность по ПАМЯТИ: О(mn) - память, которую занимает словать (напомним, что m - длина максимального слова,
# n - число слов в словаре. Сложность по памяти при сравнении слова длины l: в худшем случае в списке слов, у которых
# растояние Левенштейна с данным равно единице, находится n слов длины от (l-1) до (l+1) => сложность в худшем
# случае по памяти при проверке одного слова O(mn)
class Node:
    def __init__(self, letter):
        self.letter = letter
        self.children = dict()


class Trie:
    def __init__(self, words_dict):
        self.root = Node(None)
        pos = 0
        while pos < len(words_dict):
            self.__add_word(words_dict[pos])
            pos += 1

    def __add_word(self, word):
        letter_pos = 0
        node = self.root
        new_child = False
        while letter_pos < len(word):
            if not new_child:
                if word[letter_pos] in node.children:
                    node = node.children[word[letter_pos]]
                else:
                    new_child = True
                    node.children[word[letter_pos]] = Node(word[letter_pos])
                    node = node.children[word[letter_pos]]
            else:
                node.children[word[letter_pos]] = Node(word[letter_pos])
                node = node.children[word[letter_pos]]
            letter_pos += 1
        node.children["end"] = word

    @staticmethod
    def __check_equivalent(word, node):
        letter_pos = 0
        while letter_pos < len(word):
            if word[letter_pos] in node.children:
                node = node.children[word[letter_pos]]
                letter_pos += 1
            else:
                return None
        if "end" in node.children:
            return node.children["end"]

    # Каждый из этих методов подразумевает, что word[0] == node.letter (кроме node == self.root)
    def __check_swap(self, word, node):
        if len(word) == 1:
            return None

        if self.root == node:  # проверка на свап 1 и 2 буквы
            if word[1] in node.children:
                node = node.children[word[1]]
                if word[0] in node.children:
                    right_word = self.__check_equivalent(word[2:], node.children[word[0]])
                    if right_word is not None:
                        return right_word
            return None

        if len(word) == 2:  # проверили либо ниже, либо выше
            return None

        if word[1] == word[2]:  # не меняем одинаковые буквы
            return None

        if word[2] in node.children:
            node = node.children[word[2]]
            if word[1] in node.children:
                right_word = self.__check_equivalent(word[3:], node.children[word[1]])
                if right_word is not None:
                    return right_word
        return None

    def __check_delete(self, word, node, change_list):
        if node == self.root:
            for first_node in node.children.values():
                right_word = self.__check_equivalent(word, first_node)
                if right_word is not None:
                    change_list.append(right_word)
            return

        if word[0] in node.children:  # дабы избежать повторного обнаружения слова при удалении парных букв
            return

        for child_node in node.children.values():
            if type(child_node) is str:
                continue
            right_word = self.__check_equivalent(word[1:], child_node)
            if right_word is not None:
                change_list.append(right_word)

    def __check_add(self, word, node, change_list):
        if len(word) == 1:
            if "end" in node.children:
                return node.children["end"]
            else:
                return

        # проверка на добавления символа на 1 место
        if (self.root is node) & (word[0] != word[1]):  # не обрабатываем ситуацию, когда вставили ту же букву в начало
            right_word = self.__check_equivalent(word[1:], node)
            if right_word is not None:
                change_list.append(right_word)
            return

        if len(word) == 2:  # проверка на добавление буквы в конец
            if "end" in node.children:
                change_list.append(node.children["end"])
            return

        if word[1] == word[2]:  # не проверяем дважды добавление сдвоенной буквы
            return

        if word[2] in node.children:
            right_word = self.__check_equivalent(word[2:], node)
            if right_word is not None:
                change_list.append(right_word)

    def __check_change(self, word, node, change_list):
        if len(word) == 1:
            for next_nodes in node.children.values():
                if type(next_nodes) is str:
                    continue
                if "end" in next_nodes.children:
                    change_list.append(next_nodes.children["end"])
            return

        if self.root is node:
            # проверка на изменение первой буквы:
            for first_node in node.children.values():
                if word[1] in first_node.children:
                    right_word = self.__check_equivalent(word[1:], first_node)
                    if right_word is not None:
                        change_list.append(right_word)
            return

        for child_node in node.children.values():
            if type(child_node) is str:
                continue
            if len(word) == 2:  # проверяем замену последней буквы
                if "end" in child_node.children:
                    change_list.append(child_node.children["end"])
                continue
            if (len(word) > 2) & (word[2] in child_node.children):
                right_word = self.__check_equivalent(word[2:], child_node)
                if right_word is not None:
                    change_list.append(right_word)

    def __check_all(self, word, node, change_list):
        right_word = self.__check_swap(word, node)
        if right_word is not None:
            change_list.append(right_word)

        self.__check_change(word, node, change_list)
        self.__check_delete(word, node, change_list)
        self.__check_add(word, node, change_list)

    def check_word(self, word):
        word = word.lower()
        change_list = list()
        error_flag = False
        self.__check_all(word, self.root, change_list)
        letter_pos = 0
        node = self.root
        while letter_pos < len(word):
            if word[letter_pos] in node.children:
                node = node.children[word[letter_pos]]
                if letter_pos < (len(word) - 1):
                    self.__check_all(word[letter_pos:], node, change_list)
                else:
                    if "end" not in node.children:
                        error_flag = True
                        # единственный вариант - удалили букву в конце слова
                        for last_node in node.children.values():
                            if "end" in last_node.children:
                                change_list.append(last_node.children["end"])
            else:
                if letter_pos != 0:
                    right_word = self.__check_swap(word[letter_pos:], node)
                    if right_word is not None:
                        change_list.append(right_word)
                error_flag = True
                break
            letter_pos += 1

        if error_flag:
            if not change_list:
                return "?"
            else:
                change_list.sort()
                return change_list
        else:
            return "ok"


dict_size = input()
if not dict_size.isdigit():
    print("error")
    exit()
i = 0
words = dict()
while i < int(dict_size):
    try:
        line = input()
        if len(line) == 0:
            continue
        line = line.lower()
        words[i] = line
        i += 1
    except EOFError:
        break

trie = Trie(words)
while True:
    try:
        line = input()
        if len(line) == 0:
            continue
        else:
            correct = trie.check_word(line)
            if type(correct) is str:
                if correct == "?":
                    print(line, "-?")
                elif correct == "ok":
                    print(line, "- ok")
            else:
                print(line, "-> ", end='')
                print(*correct, sep=', ')
    except EOFError:
        break
