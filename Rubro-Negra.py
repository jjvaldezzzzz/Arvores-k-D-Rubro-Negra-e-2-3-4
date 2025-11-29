# red_black_simple_with_delete.py
# Árvore Rubro-Negra SIMPLIFICADA com inserção, remoção, busca e plotagem.

import matplotlib.pyplot as plt

RED = True
BLACK = False

class Node:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.NIL = Node(None, BLACK)
        self.root = self.NIL

    # ---------------------------------------------------
    # INSERÇÃO
    # ---------------------------------------------------
    def insert(self, key):
        new = Node(key)
        new.left = self.NIL
        new.right = self.NIL

        parent = None
        cur = self.root

        while cur != self.NIL:
            parent = cur
            if new.key < cur.key:
                cur = cur.left
            else:
                cur = cur.right

        new.parent = parent

        if parent is None:
            self.root = new
        elif new.key < parent.key:
            parent.left = new
        else:
            parent.right = new

        new.color = RED
        self.fix_insert(new)

    def fix_insert(self, z):
        while z != self.root and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                tio = z.parent.parent.right
                if tio.color == RED:  # Caso tio vermelho
                    z.parent.color = BLACK
                    tio.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:  # tio preto
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                tio = z.parent.parent.left
                if tio.color == RED:
                    z.parent.color = BLACK
                    tio.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)

        self.root.color = BLACK

    # ---------------------------------------------------
    # REMOÇÃO SIMPLIFICADA
    # ---------------------------------------------------
    def delete(self, key):
        z = self.search_node(self.root, key)
        if z == self.NIL:
            return  # não existe

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            # mínimo da subárvore direita
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == BLACK:
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right

                if w.color == RED:  # Caso 1
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED      # Caso 2
                    x = x.parent
                else:
                    if w.right.color == BLACK:   # Caso 3
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right

                    # Caso 4
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # CASOS ESPELHADOS
                w = x.parent.left

                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = BLACK

    # ---------------------------------------------------
    # FUNÇÕES AUXILIARES
    # ---------------------------------------------------
    def search_node(self, node, key):
        while node != self.NIL:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return self.NIL

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # ---------------------------------------------------
    # ROTAÇÕES
    # ---------------------------------------------------
    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
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

    def right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.NIL:
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

    # ---------------------------------------------------
    # PLOTAGEM
    # ---------------------------------------------------
    def plot(self):
        pos = {}
        self._assign(self.root, 0, 0, pos, [0])

        fig, ax = plt.subplots()

        for node, (x, y) in pos.items():
            if node.left != self.NIL:
                xl, yl = pos[node.left]
                ax.plot([x, xl], [y, yl])
            if node.right != self.NIL:
                xr, yr = pos[node.right]
                ax.plot([x, xr], [y, yr])

        for node, (x, y) in pos.items():
            ax.scatter([x], [y])
            label = f"{node.key}\n{'R' if node.color else 'B'}"
            ax.text(x, y, label, ha="center")

        ax.invert_yaxis()
        ax.set_axis_off()
        plt.title("Árvore Rubro-Negra (Simplificada)")
        plt.show()

    def _assign(self, node, x, y, pos, c):
        if node == self.NIL:
            return
        self._assign(node.left, x, y + 1, pos, c)
        pos[node] = (c[0], y)
        c[0] += 1
        self._assign(node.right, x, y + 1, pos, c)


# --------------------------------------------------
# DEMONSTRAÇÃO
# --------------------------------------------------
if __name__ == "__main__":
    tree = RBTree()
    valores = [10, 20, 30, 15, 25, 5, 1, 8, 12]

    for v in valores:
        tree.insert(v)

    tree.plot()

    tree.delete(20)
    tree.delete(10)

    tree.plot()
