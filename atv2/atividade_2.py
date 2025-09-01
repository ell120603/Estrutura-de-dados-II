from graphviz import Digraph
import random

# Representa um nó na árvore binária, contendo um valor e ponteiros para os filhos esquerdo e direito.
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Implementa uma Árvore Binária de Busca (Binary Search Tree) com métodos para inserção, busca, remoção,
# cálculo de altura, profundidade e visualização gráfica.
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Insere um valor na árvore binária de busca, mantendo a propriedade de ordenação.
    def insert(self, value):
        def _insert(node, value):
            if not node:
                return Node(value)
            if value < node.value:
                node.left = _insert(node.left, value)
            elif value > node.value:
                node.right = _insert(node.right, value)
            return node
        self.root = _insert(self.root, value)

    # Busca um valor na árvore binária de busca.
    # Retorna True se o valor for encontrado, caso contrário, retorna False.
    def search(self, value):
        def _search(node, value):
            if not node:
                return False
            if value == node.value:
                return True
            if value < node.value:
                return _search(node.left, value)
            else:
                return _search(node.right, value)
        return _search(self.root, value)

    # Remove um nó com o valor especificado da árvore.
    # Casos tratados:
    # 1. Nó folha: simplesmente remove o nó.
    # 2. Nó com um filho: substitui o nó pelo filho.
    # 3. Nó com dois filhos: substitui o valor do nó pelo menor valor da subárvore direita
    #    e remove o nó correspondente na subárvore direita.
    def delete(self, value):
        def _min_value_node(node):
            current = node
            while current.left:
                current = current.left
            return current

        def _delete(node, value):
            if not node:
                return node
            if value < node.value:
                node.left = _delete(node.left, value)
            elif value > node.value:
                node.right = _delete(node.right, value)
            else:
                # caso 1: folha
                if not node.left and not node.right:
                    return None
                # caso 2: um filho
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                # caso 3: dois filhos
                temp = _min_value_node(node.right)
                node.value = temp.value
                node.right = _delete(node.right, temp.value)
            return node

        self.root = _delete(self.root, value)

    # Calcula a altura da árvore binária de busca.
    # A altura é definida como o número máximo de arestas do nó raiz até uma folha.
    def height(self):
        def _height(node):
            if not node:
                return -1
            return 1 + max(_height(node.left), _height(node.right))
        return _height(self.root)

    # Calcula a profundidade de um nó com o valor especificado.
    # A profundidade é definida como o número de arestas do nó raiz até o nó especificado.
    def depth(self, value):
        def _depth(node, value, d):
            if not node:
                return None
            if node.value == value:
                return d
            if value < node.value:
                return _depth(node.left, value, d+1)
            else:
                return _depth(node.right, value, d+1)
        return _depth(self.root, value, 0)

    # Gera uma visualização gráfica da árvore binária de busca usando Graphviz.
    # Salva a visualização como um arquivo PNG com o nome especificado.
    def visualize(self, filename="bst_tree"):
        g = Digraph()

        def _visualize(node):
            if not node:
                return
            g.node(str(id(node)), str(node.value))
            if node.left:
                g.edge(str(id(node)), str(id(node.left)))
                _visualize(node.left)
            if node.right:
                g.edge(str(id(node)), str(id(node.right)))
                _visualize(node.right)

        _visualize(self.root)
        g.render(filename, format="png", cleanup=True)
        print(f"Árvore salva em {filename}.png")

# ---------------- DEMONSTRAÇÃO ----------------

# Demonstração do funcionamento da árvore binária de busca.
# Inclui uma árvore fixa e uma árvore gerada aleatoriamente, com exemplos de inserção, busca, remoção,
# cálculo de altura e profundidade, e visualização gráfica.

# Árvore fixa
print("=== Árvore Fixa ===")
valores_fixos = [55, 30, 80, 20, 45, 70, 90]
bst_fixa = BinarySearchTree()
for v in valores_fixos:
    bst_fixa.insert(v)

# Visualizar
bst_fixa.visualize("bst_fixa")

# Busca
print("Buscar 45:", bst_fixa.search(45))

# Remover 30 e inserir 60
print("Removendo 30...")
bst_fixa.delete(30)
print("Inserindo 60...")
bst_fixa.insert(60)
bst_fixa.visualize("bst_fixa_after")

# Altura e profundidade
print("Altura da árvore:", bst_fixa.height())
print("Profundidade do nó 45:", bst_fixa.depth(45))

# Árvore randômica
print("\n=== Árvore Randômica ===")
valores_rand = random.sample(range(1, 200), 15)
print("Valores aleatórios:", valores_rand)

bst_rand = BinarySearchTree()
for v in valores_rand:
    bst_rand.insert(v)

bst_rand.visualize("bst_rand")
print("Altura da árvore randômica:", bst_rand.height())