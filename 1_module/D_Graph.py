import sys
from collections import deque


class Graph:
    def __init__(self):
        try:
            while True:
                line = input().strip('\n')
                if line != "":
                    break
            if (line[0:2] == "u ") | (line[0:2] == "d "):
                self.__graph_type = line[0]
            else:
                print("uncorrected graph type")
                sys.exit()

            self.__start_vertex = line[2:-2]

            if (line[-2:] == " b") | (line[-2:] == " d"):
                self.__search_type = line[-1]
            else:
                print("uncorrected search type")
                sys.exit()
            self.__graph_map = {}
        except EOFError:
            print("")

    def make_graph(self):
        while True:
            try:
                line = input().rstrip('\n')
                if line != "":
                    vertex_list = line.split()
                    if vertex_list[0] in self.__graph_map:
                        self.__graph_map[vertex_list[0]].append(vertex_list[1])
                    else:
                        self.__graph_map.update({vertex_list[0]: [vertex_list[1]]})
                    if self.__graph_type == 'u':
                        if vertex_list[1] in self.__graph_map:
                            self.__graph_map[vertex_list[1]].append(vertex_list[0])
                        else:
                            self.__graph_map.update({vertex_list[1]: [vertex_list[0]]})
            except EOFError:
                break
        for key in self.__graph_map:
            self.__graph_map[key].sort()
        return

    def search(self):
        if self.__search_type == 'b':
            self.__width_search()
        elif self.__search_type == 'd':
            self.__deep_search()

    def __width_search(self):
        visited = set()
        vertexes = deque()
        vertexes.append(self.__start_vertex)
        while vertexes:  # not empty
            this_vertex = vertexes.popleft()
            if this_vertex not in visited:
                visited.add(this_vertex)
                print(this_vertex)
            if this_vertex in self.__graph_map:
                for v in self.__graph_map[this_vertex]:
                    if v not in visited:
                        vertexes.append(v)
        return

    def __deep_search(self):
        visited = set()
        vertexes = deque()
        vertexes.append(self.__start_vertex)
        while vertexes:  # not empty
            this_vertex = vertexes.pop()
            if this_vertex not in visited:
                visited.add(this_vertex)
                print(this_vertex)
            if this_vertex in self.__graph_map:
                for v in reversed(self.__graph_map[this_vertex]):
                    if v not in visited:
                        vertexes.append(v)
        return


graph = Graph()
graph.make_graph()
graph.search()
