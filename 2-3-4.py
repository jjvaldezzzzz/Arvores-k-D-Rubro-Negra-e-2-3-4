class Node234:
    def __init__(self):
        self.keys = []      # 1, 2 ou 3 chaves
        self.children = []  # 0 a 4 filhos

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 3


class Tree234:
    def __init__(self):
        self.root = Node234()

    def split(self, node, parent, index):
        """Divide um nó 4 e sobe a chave do meio."""
        middle_key = node.keys[1]

        left = Node234()
        left.keys = [node.keys[0]]

        right = Node234()
        right.keys = [node.keys[2]]

        if not node.is_leaf():
            left.children = node.children[:2]
            right.children = node.children[2:]

        # Inserindo o middle no pai
        parent.keys.insert(index, middle_key)
        parent.children[index] = left
        parent.children.insert(index + 1, right)

    def insert(self, key):
        root = self.root

        # Se a raiz está cheia, ela deve ser dividida
        if root.is_full():
            new_root = Node234()
            new_root.children.append(root)
            self.split(root, new_root, 0)
            self.root = new_root

        # Agora insere normalmente
        self._insert_nonfull(self.root, key)

    def _insert_nonfull(self, node, key):
        # Caso 1: nó folha
        if node.is_leaf():
            node.keys.append(key)
            node.keys.sort()
            return

        # Caso 2: nó interno → decidir qual filho descer
        for i, k in enumerate(node.keys):
            if key < k:
                child = node.children[i]

                if child.is_full():
                    self.split(child, node, i)
                    # Verifica para qual lado descer agora
                    if key > node.keys[i]:
                        child = node.children[i+1]

                self._insert_nonfull(child, key)
                return

        # Último filho
        child = node.children[-1]
        if child.is_full():
            self.split(child, node, len(node.keys)-1)
            if key > node.keys[-1]:
                child = node.children[-1]

        self._insert_nonfull(child, key)


# Uso:
tree = Tree234()
for x in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(x)

print("Árvore 2-3-4 construída com sucesso!")
