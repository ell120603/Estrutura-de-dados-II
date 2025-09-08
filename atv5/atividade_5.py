class No:
    """
    Representa um nó na Árvore AVL.
    Cada nó armazena uma chave, referências para os filhos e sua altura.
    """
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1 # A altura de um novo nó (folha) é sempre 1

class ArvoreAVL:
    """
    Implementa a estrutura e as operações de uma Árvore AVL.
    """
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # TAREFA 0: IMPLEMENTAR MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================

    def obter_altura(self, no):
        """
        Calcula a altura de um nó. Se o nó for nulo, a altura é 0.
        """
        """implementar"""
        return no.altura if no else 0
    

    def obter_fator_balanceamento(self, no):
        """
        Calcula o fator de balanceamento de um nó (altura da subárvore esquerda - altura da subárvore direita).
        """
        """implementar"""
        if no is None:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)
    

    def _atualizar_altura(self, no):
        """
        Atualiza a altura de um nó com base na altura máxima de seus filhos.
        A altura é 1 + max(altura(esquerda), altura(direita)).
        """
        """implementar"""
        if no:
            no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))
        return no.altura if no else 0
    

    def obter_no_valor_minimo(self, no):
        """
        Encontra o nó com o menor valor em uma subárvore (o nó mais à esquerda).
        """
        """implementar"""
        if no is None or no.esquerda is None:
            return no
        return self.obter_no_valor_minimo(no.esquerda)
    

    def _rotacao_direita(self, no_pivo):
        """
        Realiza uma rotação para a direita em torno do no_pivo.
        """
        """implementar"""
        # no_pivo é y na notação clássica; x = y.esquerda
        x = no_pivo.esquerda
        T2 = x.direita if x else None

        # Rotação
        x.direita = no_pivo
        no_pivo.esquerda = T2

        # Atualiza alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(x)

        # Retorna nova raiz da subárvore
        return x
    

    def _rotacao_esquerda(self, no_pivo):
        """
        Realiza uma rotação para a esquerda em torno do no_pivo.
        """
        """implementar"""
        # no_pivo é x na notação clássica; y = x.direita
        y = no_pivo.direita
        T2 = y.esquerda if y else None

        # Rotação
        y.esquerda = no_pivo
        no_pivo.direita = T2

        # Atualiza alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(y)

        # Retorna nova raiz da subárvore
        return y

    # ===============================================================
    # TAREFA 1: IMPLEMENTAR INSERÇÃO E DELEÇÃO COM BALANCEAMENTO
    # ===============================================================

    def inserir(self, chave):
        """Método público para inserir uma chave na árvore."""
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        # Passo 1: Realiza a inserção padrão de uma BST.
        # (Se o nó atual for nulo, cria um novo nó e o retorna)
        # (Se a chave for menor, continua a busca na subárvore esquerda)
        # (Se a chave for maior, continua a busca na subárvore direita)
        # (Se a chave for igual, lança um erro, pois não permitimos duplicatas)
        if no_atual is None:
            return No(chave)

        if chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            raise ValueError("Chave duplicada não permitida em árvore AVL.")

        # ---- LÓGICA DE BALANCEAMENTO AVL (A IMPLEMENTAR) ----
        # Passo 2: Atualiza a altura do nó atual (ancestral) após a inserção.
        self._atualizar_altura(no_atual)
        # Passo 3: Calcula o fator de balanceamento para verificar se o nó ficou desbalanceado.
        balance = self.obter_fator_balanceamento(no_atual)
        # Passo 4: Verifica se o nó ficou desbalanceado e aplica as rotações corretas.
        # Caso 1: Desbalanceamento à Esquerda-Esquerda (Rotação Simples à Direita)
        if balance > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)
        # Caso 2: Desbalanceamento à Direita-Direita (Rotação Simples à Esquerda)
        if balance < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)
        # Caso 3: Desbalanceamento à Esquerda-Direita (Rotação Dupla)
        if balance > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)
        # Caso 4: Desbalanceamento à Direita-Esquerda (Rotação Dupla)
        if balance < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        # Retorna o nó (potencialmente a nova raiz da subárvore após rotação).
        return no_atual

    def deletar(self, chave):
        """Método público para deletar uma chave da árvore."""
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        # Passo 1: Realiza a deleção padrão de uma BST.
        # (Se o nó atual for nulo, retorna o próprio nó)
        # (Navega para a esquerda ou direita para encontrar o nó a ser deletado)
        # (Quando o nó é encontrado, trata os três casos de deleção)
            # Caso 1: Nó com um filho ou nenhum filho.
            # Caso 2: Nó com dois filhos (encontra o sucessor, copia e deleta o sucessor).
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else:
            # Nó encontrado
            # Caso 1: Nó com um filho ou nenhum filho.
            if no_atual.esquerda is None:
                temp = no_atual.direita
                no_atual = None
                return temp
            elif no_atual.direita is None:
                temp = no_atual.esquerda
                no_atual = None
                return temp
            # Caso 2: Nó com dois filhos (encontra o sucessor, copia e deleta o sucessor).
            temp = self.obter_no_valor_minimo(no_atual.direita)
            no_atual.chave = temp.chave
            no_atual.direita = self._deletar_recursivo(no_atual.direita, temp.chave)

        # ---- LÓGICA DE BALANCEAMENTO AVL APÓS DELEÇÃO (A IMPLEMENTAR) ----
        # Passo 2: Atualiza a altura do nó atual.
        if no_atual is None:
            return no_atual

        self._atualizar_altura(no_atual)
        # Passo 3: Calcula o fator de balanceamento.
        balance = self.obter_fator_balanceamento(no_atual)
        # Passo 4: Verifica o desbalanceamento e aplica as rotações.
        # Left Left
        if balance > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)
        # Left Right
        if balance > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)
        # Right Right
        if balance < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)
        # Right Left
        if balance < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        # Retorna o nó (potencialmente a nova raiz da subárvore).
        return no_atual

    # ===============================================================
    # TAREFA 2 E 3: IMPLEMENTAR BUSCAS
    # ===============================================================

    def encontrar_nos_intervalo(self, chave1, chave2):
        """
        Encontra e retorna uma lista com todas as chaves no intervalo [chave1, chave2].
        """
        """implementar"""
        resultado = []

        def inorder_intervalo(no):
            if no is None:
                return
            # Se possível, explorar esquerda (somente se houver chance de encontrar valores >= chave1)
            if no.chave > chave1:
                inorder_intervalo(no.esquerda)
            # Se o nó atual está no intervalo, adiciona
            if chave1 <= no.chave <= chave2:
                resultado.append(no.chave)
            # Se possível, explorar direita (somente se houver chance de encontrar valores <= chave2)
            if no.chave < chave2:
                inorder_intervalo(no.direita)

        inorder_intervalo(self.raiz)
        return resultado
        

    def obter_profundidade_no(self, chave):
        """
        Calcula a profundidade (nível) de um nó com uma chave específica.
        A raiz está no nível 0. Se o nó não for encontrado, retorna -1.
        """
        """implementar"""
        nivel = 0
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return nivel
            elif chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
            nivel += 1
        return -1

# --- Bloco de Teste e Demonstração da Atividade AVL ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()
    
    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")
    
    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
        # Dica: Implemente um percurso (em-ordem, por exemplo) para verificar a estrutura da árvore.
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        if nos_no_intervalo is not None:
            print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade is not None:
            if profundidade != -1:
                print(f"O nó 6 está no nível/profundidade: {profundidade}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `obter_profundidade_no` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")
