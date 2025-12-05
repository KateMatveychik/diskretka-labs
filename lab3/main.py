import sys
from collections import deque

class Graph:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = 0 # хранит число ребер (для проверки древочисленности)

    def add_edge(self, i, j):
        self.graph[i].append(j)
        self.graph[j].append(i)
        self.edges += 1

    def neighbors(self, v):
        return self.graph[v]


def read_graph_from_file(filename):
    with open(filename, "r") as file:
        n = int(file.readline())  # читаем количество вершин
        graph = Graph(n)  # создаём граф

        for line in file:
            parts = line.split() # делим строку по пробелам: ["0", "1"]
            i = int(parts[0])
            j = int(parts[1])
            graph.add_edge(i, j)  # добавляем ребро

    return graph

# функция подсчета компонент связности
def count_components(graph):
    visited = [False] * graph.n
    components = []

    for v in range(graph.n):
        if not visited[v]:
            # здесь реализуем BFS прямо в функции
            queue = deque([v])
            visited[v] = True
            comp_vertices = []

            while queue:
                vertex = queue.popleft()
                comp_vertices.append(vertex)

                for u in graph.neighbors(vertex):
                    if not visited[u]:
                        visited[u] = True
                        queue.append(u)

            components.append(comp_vertices)  # двумерный список, где каждый элемент — компонента связности

    return len(components), components

# функция для поиска цикла в графе
def find_cycle(graph):
    visited = [False] * graph.n # отмечаем вершины, которые уже посещен
    parent = [None] * graph.n
    #stack = []

    for v in range(graph.n):
        if not visited[v]: # делаем обход из каждой непосещенной вершины (тк граф может быть несвязным)
            stack = [(v, None)] # (текущая вершина, родитель)
            while stack:
                u, p = stack.pop()
                if visited[u]:
                    continue # если уже обработана - пропускаем

                visited[u] = True
                parent[u] = p

                # перебираем соседей вершины u
                for x in graph.neighbors(u):
                    if not visited[x]:
                        stack.append((x, u)) # не посещен - идем дальше
                    else:
                        if x != p:
                            # найден цикл: нужно восстановить путь от u до x через parent
                            cycle = [u]
                            cur = parent[u]
                            while cur is not None and cur != x:
                                cycle.append(cur)
                                cur = parent[cur]

                                # если cur == x, добавляем x и замыкаем цикл
                            if cur == x:
                                cycle.append(x)
                                # замыкаем цикл, добавив начальную вершину ещё раз
                                cycle.append(u)
                                # возвращаем цикл в удобном порядке, например от x до x:
                                cycle = cycle[::-1]  # разворачиваем, чтобы начинать с x
                                return cycle
                            else:
                                pass

    return None


def is_tree(graph):

    # 1. Проверка связности
    comp_count, _ = count_components(graph)
    if comp_count != 1:
        return False

    # 2. Проверка ацикличности
    cycle = find_cycle(graph)
    if cycle is not None:
        return False

    return True

# проверка древочисленности
def has_tree_edge_count(graph):
    return graph.edges == graph.n - 1


def check_tree_properties(filename, graph):
    check = chr(0x2714)
    cross = chr(0x2718)
    comp_count, comps = count_components(graph)
    cycle = find_cycle(graph)
    edge_condition = has_tree_edge_count(graph)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== СПИСОК СМЕЖНОСТИ ГРАФА  ===\n")
        for i in range(graph.n):
            f.write(f"{i}: {graph.neighbors(i)}\n")

        f.write("\n=== ПРОВЕРКА СВОЙСТВ ГРАФА ===\n")

        # 1. Связность
        if comp_count == 1:
            f.write(f"Связность: {check} граф связный\n")
        else:
            f.write(f"Связность: {cross} граф НЕ связный\n")
            f.write(f"Компоненты связности: {comps}\n")

        # 2. Ацикличность
        if cycle is None:
            f.write(f"Ацикличность: {check} циклов нет\n")
        else:
            f.write(f"Ацикличность: {cross} найден цикл: {cycle}\n")

        # 3. Древочисленность
        if edge_condition:
            f.write(f"Древочисленность: {check} q = {graph.edges}, p - 1 = {graph.n - 1}\n")
        else:
            f.write(f"Древочисленность: {cross} q = {graph.edges}, p - 1 = {graph.n - 1}\n")

        # Финальный вывод
        if comp_count == 1 and cycle is None:
            f.write(f"\nИТОГ: Граф является деревом {check}\n")
        else:
            f.write(f"\nИТОГ: Граф НЕ является деревом {cross}\n")

def main():
    if len(sys.argv) != 3:
        print("Использование: python main.py <входной файл> <выходной файл>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    graph = read_graph_from_file(input_file)

    check_tree_properties(output_file, graph)

if __name__ == "__main__":
    main()
