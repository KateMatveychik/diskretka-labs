import sys

class Graph:
    # Конструктор: создаем граф с n вершинами
    def __init__(self, n):
        self.n = n
        self.weights = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            self.weights[i][i] = 0

    # Добавление веса дуги между вершинами u и v
    def addEdge(self, u, v, w):
        self.weights[u-1][v-1] = w

    # Проверка работы метода addEdge (выводит матрицу весов)
    def printWeights(self):
        for row in self.weights:
            print(row)

# читаем граф из файла
def readFromFile(filename):
    with open(filename, 'r') as file:
        n = int(file.readline()) # берем количество вершин из файла
        g = Graph(n)

        for line in file:
            if line.strip() == "": continue
            parts = line.split()
            u = int(parts[0])
            v = int(parts[1])
            w = int(parts[2])
            g.addEdge(u, v, w)
    return g

def floydWarshall(graph):
    n = graph.n

    # 1. Копируем матрицу весов в T
    T = [[graph.weights[i][j] for j in range(graph.n)] for i in range(graph.n)]

    # 2. Инициализируем матрицу путей
    P = [[0 if T[i][j] == float('inf') else i+1 for j in range(graph.n)] for i in range(graph.n)]


    print("Начальная матрица T:")
    for rowT in T: print(*rowT)

    print("\nНачальная матрица путей P:")
    for rowP in P: print(*rowP)

    # 3. Основной цикл алгоритма 
    for k in range(n):                # промежуточная вершина k
        for i in range(n):            # начальная вершина i
            if k==i or T[i][k] == float('inf'):
                continue             
            for j in range(n):        # конечная вершина j
                if k==j or T[k][j] == float('inf'):
                    continue         
                if T[i][j] > T[i][k] + T[k][j]:
                    T[i][j] = T[i][k] + T[k][j]
                    P[i][j] = P[k][j]   

    # Проверка отрицательного цикла
    for j in range(n):
        if T[j][j] < 0:
            print(f"Обнаружен отрицательный цикл через вершину {j + 1}")
            return None, None

    return T,P


# Восстанавливает кратчайший путь из start в end
def getPath(P, start, end):
    """
    start, end — номера вершин с 1
    """
    if P[start-1][end-1] == 0:  # пути нет
        return None

    path = [end]
    while end != start:
        end = P[start-1][end-1]
        path.append(end)

    path.reverse()
    return path


# Запись результатов в файл
def writeResultsToFile(filename, graph, T, P):
    n = graph.n

    with open(filename, "w", encoding="utf-8") as f:
            # Матрица кратчайших расстояний
            f.write("МАТРИЦА КРАТЧАЙШИХ РАССТОЯНИЙ:\n")

            for i in range(n):
                for j in range(n):
                    if T[i][j] == float('inf'):
                        f.write(f"{'inf':>8}")
                    else:
                        f.write(f"{T[i][j]:8.2f}")
                f.write("\n")

            f.write("\n")

            # Матрица путей (P)
            f.write("МАТРИЦА ПУТЕЙ:\n")

            for i in range(n):
                for j in range(n):
                    if P[i][j] == 0:
                        f.write(f"{'0':>8}")
                    else:
                        f.write(f"{P[i][j]:8}")
                f.write("\n")

            f.write("\n")

            # Кратчайшие пути
            f.write("\nКРАТЧАЙШИЕ ПУТИ:\n")
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    path = getPath(P, i + 1, j + 1)
                    if path is None:
                        f.write(f"Путь из {i+1} в {j+1}: не существует\n")
                    else:
                        path_str = " -> ".join(str(v) for v in path)
                        f.write(f"Путь из {i+1} в {j+1}: {path_str}, расстояние: {T[i][j]}\n")



def main():
    if len(sys.argv) != 3:
        print("Использование: python floyd_warshall.py <входной файл> <выходной файл>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    graph = readFromFile(input_file)
    T,P = floydWarshall(graph)

    if T is not None and P is not None:
        writeResultsToFile(output_file, graph, T, P)
        print(f"Результаты записаны в {output_file}")



if __name__ == "__main__":
    main()

