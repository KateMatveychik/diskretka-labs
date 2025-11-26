class Graph:
    # Конструктор: создаем граф с n вершинами
    def __init__(self, n):
        self.n = n #количество вершин
        self.graph = [[] for _ in range(n)] #список смежности: n пустых списков

    # Метод добавления ребра между вершинами i и j
    def add_edge(self, i, j):
        self.graph[i].append(j) # добавляем j в список соседей i
        self.graph[j].append(i) # добавляем i в список соседей j

    def print_graph(self):
        for i in range(self.n):
            print(f"{i}: {self.graph[i]}")

    # Метод получения соседей вершины
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

        graph.print_graph()

    return graph

def findMIS(graph):
    MIS = set()
    S = set()
    T = set(range(graph.n)) # все вершины
    stack = [(S, T)] # стек с начальным состоянием

    while stack:
        S, T = stack.pop()

        # проверим, пусто ли T
        if not T:
            if len(S) > len(MIS):
                MIS = S.copy()
        else:
            v = T.pop()

            # 1) Берём v
            S_new = S.copy()
            S_new.add(v)

            T_new = T.copy()
            for neighbor in graph.neighbors(v):
                T_new.discard(neighbor)

            stack.append((S_new, T_new))

            # 2) Не берём v
            stack.append((S, T.copy()))

    return MIS

def findMVC_from_MIS(graph, MIS):
    V = set(range(graph.n))
    return V - MIS


def write_results_to_file(filename, graph, MIS, MVC):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"вершины: {graph.n}\n")
        edge_count = sum(len(neigh) for neigh in graph.graph) // 2
        f.write(f"рёбра: {edge_count}\n")
        f.write(f"размер наибольшего независимого множества: {len(MIS)}\n")
        f.write(f"размер наименьшего вершинного покрытия: {len(MVC)}\n")
        f.write(f"наибольшее независимое множество: {MIS}\n")
        f.write(f"наименьшее вершинное покрытие: {MVC}\n")


if __name__ == "__main__":
    graph =  read_graph_from_file("input.txt")

    MIS = findMIS(graph)
    MVC = findMVC_from_MIS(graph, MIS)

    print("\n=== Результаты анализа ===")
    print(f"Наибольшее независимое множество (MIS): {MIS}")
    print(f"Размер MIS: {len(MIS)}")

    print(f"\nНаименьшее вершинное покрытие (MVC): {MVC}")
    print(f"Размер MVC: {len(MVC)}")

    write_results_to_file("output.txt", graph, MIS, MVC)
