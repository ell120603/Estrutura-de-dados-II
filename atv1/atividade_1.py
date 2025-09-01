import re, random
from graphviz import Digraph
from math import isclose

# Nó da árvore
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Tokenizador simples: divide a expressão em números e operadores, ignorando espaços.
def tokenize(expr):
    return re.findall(r'\d+|[()+\-*/]', expr.replace(' ', ''))

# Shunting-yard -> postfix: converte uma expressão infixa para notação pós-fixa (RPN),
# utilizando uma pilha para gerenciar a precedência dos operadores.
def infix_to_postfix(tokens):
    prec = {'+':1, '-':1, '*':2, '/':2}
    out = []
    stack = []
    for t in tokens:
        if re.fullmatch(r'\d+', t):
            out.append(t)
        elif t in prec:
            while stack and stack[-1] in prec and prec[stack[-1]] >= prec[t]:
                out.append(stack.pop())
            stack.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(':
                out.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
    while stack:
        out.append(stack.pop())
    return out

# Constrói uma árvore binária a partir de uma expressão em notação pós-fixa (RPN).
def build_tree_from_postfix(postfix):
    st = []
    for t in postfix:
        if re.fullmatch(r'\d+', t):
            st.append(Node(int(t)))
        else:
            r = st.pop()
            l = st.pop()
            st.append(Node(t, l, r))
    return st[0]

# Converte uma árvore binária para uma string em notação infixa, adicionando parênteses.
def tree_to_infix(node):
    if isinstance(node.value, int):
        return str(node.value)
    return f'({tree_to_infix(node.left)}{node.value}{tree_to_infix(node.right)})'

# Avalia a árvore binária e retorna o valor numérico da expressão.
# Nota: assume que a entrada é válida e não verifica divisores zero.
def eval_tree(node):
    if isinstance(node.value, int):
        return node.value
    L = eval_tree(node.left)
    R = eval_tree(node.right)
    if node.value == '+': return L + R
    if node.value == '-': return L - R
    if node.value == '*': return L * R
    if node.value == '/':
        # cuidado divisão por zero
        return L / R

# Desenha a árvore binária usando Graphviz e salva o resultado como um arquivo PNG.
def draw_tree(node, filename='tree'):
    g = Digraph(engine='dot')
    g.attr('graph', rankdir='TB')            # top->bottom
    g.attr('node', shape='circle', style='filled', fillcolor='white', fontsize='12')

    def rec(n):
        nid = str(id(n))
        label = str(n.value)
        # folhas (operandos) como elipse (mais estreita)
        if isinstance(n.value, int):
            g.node(nid, label, shape='ellipse')
        else:
            g.node(nid, label, shape='circle')
        if n.left:
            g.edge(nid, str(id(n.left)))
            rec(n.left)
        if n.right:
            g.edge(nid, str(id(n.right)))
            rec(n.right)

    rec(node)
    out = g.render(filename, format='png', cleanup=True)  # gera filename.png
    return out

# ---------- FIXED expression (como string) ----------
fixed_expr = '(((7+3)*(5-2))/(10*20))'   # expressão original
tokens = tokenize(fixed_expr)
postfix = infix_to_postfix(tokens)
fixed_tree = build_tree_from_postfix(postfix)

fixed_val = eval_tree(fixed_tree)
print('Fixed expression:', fixed_expr)
print('Postfix:', postfix)
print('Avaliação (valor numérico):', fixed_val)   # deve ser 0.15

fixed_png = draw_tree(fixed_tree, 'fixed_tree')
print('Árvore fixa salva em:', fixed_png)

# Verificação numérica (30 / 200 = 0.15)
assert isclose(fixed_val, 0.15, rel_tol=1e-9), f'Valor inesperado: {fixed_val}'

# ---------- RANDOM expression generator ----------
# gera uma árvore binária com exatamente k operadores (logo k+1 operandos)
def gen_tree_with_k_ops(k):
    if k == 0:
        return Node(random.randint(1, 20))
    op = random.choice(['+','-','*','/'])
    left_k = random.randint(0, k-1)
    right_k = k-1 - left_k
    left = gen_tree_with_k_ops(left_k)
    right = gen_tree_with_k_ops(right_k)
    # evita divisor zero se op for '/'
    if op == '/' and isinstance(right.value, int) and right.value == 0:
        right.value = random.randint(1, 20)
    return Node(op, left, right)

# pedimos ao menos 2 operadores (requisito)
rand_ops = 2
random_tree = gen_tree_with_k_ops(rand_ops)
random_expr_str = tree_to_infix(random_tree)
random_val = eval_tree(random_tree)

print('\nRandom expression (from tree):', random_expr_str)
print('Valor da expressão randômica:', random_val)

random_png = draw_tree(random_tree, 'random_tree')
print('Árvore randômica salva em:', random_png)
