import matplotlib.pyplot as plt

class Node234:
    def __init__(self):
        self.keys = []      # lista de chaves (1 a 3 chaves)
        self.children = []  # filhos (0 a 4 filhos)
        self.leaf = True

class Tree234:
    def __init__(self):
        self.root = Node234()

    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.leaf:
            return False
        return self.search(key, node.children[i])

    def split(self, parent, idx):
        node = parent.children[idx]
        mid = node.keys[1]

        left = Node234()
        right = Node234()

        left.keys = [node.keys[0]]
        right.keys = [node.keys[2]]

        if not node.leaf:
            left.children = node.children[:2]
            right.children = node.children[2:]
            left.leaf = right.leaf = False

        parent.keys.insert(idx, mid)
        parent.children[idx] = left
        parent.children.insert(idx + 1, right)

    def insert(self, key):
        root = self.root
        if len(root.keys) == 3:
            new_root = Node234()
            new_root.children.append(root)
            new_root.leaf = False
            self.split(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == 3:
                self.split(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def delete(self, key):
        self._delete(self.root, key)

        # Se a raiz ficou vazia e não é folha, desce um nível
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        # 1. Encontrar posição da chave ou onde ela seria inserida
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        
        # CASO 1 — chave encontrada em nó FOLHA
        
        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                node.keys.pop(i)
                return
            else:
                # CASO 2 — chave está em nó INTERNO
                return self._delete_internal(node, key, i)

        # Se chave não está no nó e ele é folha → não existe
        if node.leaf:
            return

        
        # CASO 3 — chave está em subárvore
        
        child = node.children[i]

        # Se o filho tem apenas 1 chave, consertar antes de descer
        if len(child.keys) == 1:
            self._fix_child(node, i)

        # Depois da correção, encontrar de novo o filho certo
        if i > len(node.keys):
            child = node.children[i-1]
        else:
            child = node.children[i]

        self._delete(child, key)

    
    # CASO DE REMOÇÃO EM NÓ INTERNO
    
    def _delete_internal(self, node, key, i):
        pred_child = node.children[i]
        succ_child = node.children[i+1]

        # CASO A — predecessor tem >= 2 chaves
        if len(pred_child.keys) > 1:
            pred_key = self._get_pred(pred_child)
            node.keys[i] = pred_key
            self._delete(pred_child, pred_key)

        # CASO B — sucessor tem >= 2 chaves
        elif len(succ_child.keys) > 1:
            succ_key = self._get_succ(succ_child)
            node.keys[i] = succ_key
            self._delete(succ_child, succ_key)

        # CASO C — ambos têm 1 chave → merge
        else:
            merged = Node234()
            merged.leaf = pred_child.leaf
            merged.keys = pred_child.keys + [key] + succ_child.keys
            if not pred_child.leaf:
                merged.children = pred_child.children + succ_child.children

            node.children[i] = merged
            node.keys.pop(i)
            node.children.pop(i+1)

            self._delete(merged, key)

    
    # Fix para filho com 1 chave
    
    def _fix_child(self, parent, idx):
        child = parent.children[idx]

        # Tenta pegar chave do irmão esquerdo
        if idx > 0 and len(parent.children[idx-1].keys) > 1:
            left = parent.children[idx-1]
            child.keys.insert(0, parent.keys[idx-1])
            parent.keys[idx-1] = left.keys.pop()
            if not left.leaf:
                child.children.insert(0, left.children.pop())

        # Tenta pegar chave do irmão direito
        elif idx < len(parent.children)-1 and len(parent.children[idx+1].keys) > 1:
            right = parent.children[idx+1]
            child.keys.append(parent.keys[idx])
            parent.keys[idx] = right.keys.pop(0)
            if not right.leaf:
                child.children.append(right.children.pop(0))

        # Caso contrário: merge
        else:
            if idx < len(parent.children)-1:
                right = parent.children[idx+1]
                child.keys += [parent.keys[idx]] + right.keys
                if not child.leaf:
                    child.children += right.children
                parent.keys.pop(idx)
                parent.children.pop(idx+1)
            else:
                left = parent.children[idx-1]
                left.keys += [parent.keys[idx-1]] + child.keys
                if not left.leaf:
                    left.children += child.children
                parent.keys.pop(idx-1)
                parent.children.pop(idx)

    
    # Predecessor e sucessor
    
    def _get_pred(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_succ(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    
    # Plotagem
    
    def plot(self):
        levels = []
        self._collect(self.root, 0, levels)

        fig, ax = plt.subplots()
        y = 0
        for level in levels:
            for x, node in enumerate(level):
                label = "[" + "|".join(str(k) for k in node.keys) + "]"
                ax.scatter([x], [y])
                ax.text(x, y, label, ha="center")
            y -= 1

        ax.set_axis_off()
        plt.title("Árvore 2-3-4")
        plt.show()

    def _collect(self, node, depth, levels):
        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node)
        if not node.leaf:
            for c in node.children:
                self._collect(c, depth+1, levels)


# Teste de demonstração

if __name__ == "__main__":
    t = Tree234()
    vals = [20,40,60,80,10,30,50,70,25,35,90,110,21,31,54,13,28,91,34,32,47]

    for v in vals:
        t.insert(v)

    print("Busca 25:", t.search(25))
    t.plot()

    # Remoção
    t.delete(40)
    t.delete(60)
    t.plot()
