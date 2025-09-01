import random
from graphviz import Digraph

# Representa um nó na árvore binária, contendo um valor e ponteiros para os filhos esquerdo e direito.
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.left = None
        self.right = None

# Implementa uma Árvore Binária de Busca (Binary Search Tree) com métodos para inserção, travessias
# (in-order, pre-order, post-order) e visualização gráfica.
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Insere um valor na árvore binária de busca, mantendo a propriedade de ordenação.
    def insert(self, valor):
        if self.root is None:
            self.root = Node(valor)
        else:
            self._insert(self.root, valor)

    def _insert(self, node, valor):
        if valor < node.valor:
            if node.left is None:
                node.left = Node(valor)
            else:
                self._insert(node.left, valor)
        else:
            if node.right is None:
                node.right = Node(valor)
            else:
                self._insert(node.right, valor)

    # Travessias --------------------------

    # Realiza a travessia in-order (Esquerda-Raiz-Direita) e retorna os valores em uma lista.
    def inorder(self, node=None, resultado=None):
        if resultado is None:
            resultado = []
        if node is None:
            node = self.root
        if node.left:
            self.inorder(node.left, resultado)
        resultado.append(node.valor)
        if node.right:
            self.inorder(node.right, resultado)
        return resultado

    # Realiza a travessia pre-order (Raiz-Esquerda-Direita) e retorna os valores em uma lista.
    def preorder(self, node=None, resultado=None):
        if resultado is None:
            resultado = []
        if node is None:
            node = self.root
        resultado.append(node.valor)
        if node.left:
            self.preorder(node.left, resultado)
        if node.right:
            self.preorder(node.right, resultado)
        return resultado

    # Realiza a travessia post-order (Esquerda-Direita-Raiz) e retorna os valores em uma lista.
    def postorder(self, node=None, resultado=None):
        if resultado is None:
            resultado = []
        if node is None:
            node = self.root
        if node.left:
            self.postorder(node.left, resultado)
        if node.right:
            self.postorder(node.right, resultado)
        resultado.append(node.valor)
        return resultado

    # Gera uma visualização gráfica da árvore binária de busca usando Graphviz.
    # Salva a visualização como um arquivo PNG com o nome especificado e o abre automaticamente.
    def gerar_grafo(self, nome_arquivo="arvore"):
        dot = Digraph(comment="Árvore Binária", format="png")
        self._adicionar_no(dot, self.root)
        dot.render(nome_arquivo, view=True)  # Gera e abre a imagem automaticamente

    def _adicionar_no(self, dot, node):
        if node is None:
            return
        dot.node(str(node.valor), str(node.valor))
        if node.left:
            dot.edge(str(node.valor), str(node.left.valor))
            self._adicionar_no(dot, node.left)
        if node.right:
            dot.edge(str(node.valor), str(node.right.valor))
            self._adicionar_no(dot, node.right)

# ------------------- Execução -------------------

# Demonstração do funcionamento da árvore binária de busca.
# Inclui uma árvore com valores fixos e uma árvore com valores aleatórios, com exemplos de inserção,
# travessias e visualização gráfica.

# 1) Árvore com valores fixos
valores_fixos = [55, 30, 80, 20, 45, 70, 90]
arvore_fixa = BinarySearchTree()
for v in valores_fixos:
    arvore_fixa.insert(v)

print("Árvore com valores fixos:")
print("In-Order (E-R-D):", arvore_fixa.inorder())
print("Pre-Order (R-E-D):", arvore_fixa.preorder())
print("Post-Order (E-D-R):", arvore_fixa.postorder())
arvore_fixa.gerar_grafo("arvore_fixa")

# 2) Árvore com valores aleatórios
valores_random = random.sample(range(1, 100), 10)
arvore_random = BinarySearchTree()
for v in valores_random:
    arvore_random.insert(v)

print("\nÁrvore com valores aleatórios:", valores_random)
print("In-Order (E-R-D):", arvore_random.inorder())
print("Pre-Order (R-E-D):", arvore_random.preorder())
print("Post-Order (E-D-R):", arvore_random.postorder())
arvore_random.gerar_grafo("arvore_random")