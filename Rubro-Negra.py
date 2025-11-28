RED = True
BLACK = False

class RBNode:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color      # True = vermelho, False = preto
        self.left = None
        self.right = None
        self.parent = None

def is_red(node):
    return node is not None and node.color == RED

class RedBlackTree:
    def __init__(self):
        self.root = None

    # Rotação à esquerda
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    # Rotação à direita
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def insert(self, key):
        """Insere um nó e depois corrige violações."""
        new_node = RBNode(key)
        parent = None
        current = self.root

        # Inserção estilo BST
        while current:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Corrige as cores/rotações
        self.fix_insert(new_node)

    def fix_insert(self, z):
        """Resolve conflitos após inserção."""
        while z.parent and is_red(z.parent):
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                # Caso 1: tio vermelho → recolorir
                if is_red(uncle):
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent

                else:  # tio preto
                    # Caso 2: linha quebrada → rotação
                    if z == z.parent.right:
                        z = z.parent
                        self.rotate_left(z)

                    # Caso 3: linha reta → rot dir
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_right(z.parent.parent)

            else:
                uncle = z.parent.parent.left

                if is_red(uncle):
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rotate_right(z)

                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_left(z.parent.parent)

        self.root.color = BLACK


# Exemplo de uso:
tree = RedBlackTree()
for x in [10, 20, 30, 15, 25, 5]:
    tree.insert(x)

print("Inserção concluída (árvore balanceada).")
