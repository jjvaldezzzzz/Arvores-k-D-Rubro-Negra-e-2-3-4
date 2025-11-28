class KDNode:
    def __init__(self, point, depth=0):
        self.point = point          # Ex: ponto 2D (x,y) ou 3D (x,y,z)
        self.left = None
        self.right = None
        self.depth = depth          # Profundidade do nó (qual eixo usar)

class KDTree:
    def __init__(self, k):
        self.k = k      # Número de dimensões
        self.root = None

    def insert(self, point):
        """Insere recursivamente um ponto na k-d tree."""
        self.root = self._insert_recursive(self.root, point, depth=0)

    def _insert_recursive(self, node, point, depth):
        # Caso base: posição vazia → cria nó
        if node is None:
            return KDNode(point, depth)

        # Define o eixo de comparação (x, y, z...)
        axis = depth % self.k

        # Decide se vai para esquerda ou direita conforme o eixo atual
        if point[axis] < node.point[axis]:
            node.left = self._insert_recursive(node.left, point, depth + 1)
        else:
            node.right = self._insert_recursive(node.right, point, depth + 1)

        return node

    def print_tree(self, node=None, level=0):
        """Imprime a árvore de forma simples."""
        if node is None:
            node = self.root
        if node is None:
            return

        print("   " * level, node.point)
        if node.left:
            self.print_tree(node.left, level+1)
        if node.right:
            self.print_tree(node.right, level+1)


# Exemplo de uso:
tree = KDTree(k=2)
points = [(3,6), (17,15), (13,15), (6,12), (9,1), (2,7)]
for p in points:
    tree.insert(p)

tree.print_tree()
