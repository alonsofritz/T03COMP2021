import sys
import os.path
import string
import lex as l
import stack as s
import pandas as pd      # Para manipular os dados da Tabela Excel .xlsx

""" Classe que representa o analisador léxico """
""" Bottom-up => LR(1) """
""" LR(1)     => Redução pelo lado esquerdo """


class Syntactic():

    def __init__(self):

        # Start léxico
        self.lex = l.Lex()
        self.lex.start()
        self.lex.printTokenList()

        # Tabela sintática
        self.tableExcel = pd.read_excel(
            './stuffs/table/table.xlsx', skiprows=1, index_col=0)
        self.tableSyntax = self.tableExcel.to_numpy()

        # Arquivo de saída do sintático
        self.output_file = "sync.txt"
        self.output_file = open(self.output_file, 'w')

        # Pilha para análise sintática
        self.stack = s.Stack()
        self.stack.push(0)

        # Quantidade de elementos gerados por uma produção
        self.sizeProduction = [1,  2,  1,  2,  2,  1,  1,  1,  2,  4,  4,  5,  1,  1,  1,
                               2,  3,  1, 1, 1, 3, 3, 3, 2, 9, 8, 10, 1, 1, 5, 5, 1, 1, 1, 2, 4, 8, 7, 4, 2]

        # Produções existentes
        self.productions = [
            'Stmts',
            'Stmts',
            'Stmts',
            'Stmts',
            'Stmt',
            'Stmt',
            'Stmt',
            'Stmt',
            'Stmt',
            'If',
            'If',
            'Else',
            'Else',
            'Expr',
            'Expr',
            'Expr',
            'Arit',
            'Arit',
            'Factor',
            'Factor',
            'Factor',
            'Rel',
            'Log',
            'Log',
            'For',
            'For',
            'Forexpr',
            'Postfix',
            'Postfix',
            'Read',
            'Write',
            'Type',
            'Type',
            'Type',
            'Declaration',
            'Declaration',
            'Function',
            'Function',
            'Params',
            'Params'
        ]

        # self.error = False

    def terminals(self, x):
        if x == 'DEL_LP':
            return 0
        elif x == 'DEL_RP':
            return 1
        elif x == 'OP_PP':
            return 2
        elif x == 'DEL_COM':
            return 3
        elif x == 'OP_MM':
            return 4
        elif x == 'DEL_SC':
            return 5
        elif x == 'OP_ASS':
            return 6
        elif x == 'KW_an':
            return 7
        elif x == 'boolean':
            return 8
        elif x == 'KW_car':
            return 9
        elif x == 'KW_cela':
            return 10
        elif x == 'KW_entulesse':
            return 11
        elif x == 'KW_hyaline':
            return 12
        elif x == 'id':
            return 13
        elif x == 'KW_ista':
            return 14
        elif x == 'KW_liltengwa':
            return 15
        elif x == 'KW_note':
            return 16
        elif x == 'number':
            return 17
        elif x == 'OP_ADD' or x == 'OP_DIV' or x == 'OP_MIN' or x == 'OP_MOD' or x == 'OP_MUL':
            return 18
        elif x == 'OP_ar' or x == 'OP_hela' or x == 'OP_helaer' or x == 'OP_la':
            return 19
        elif x == 'OP_EQ' or x == 'OP_GE' or x == 'OP_GT' or x == 'OP_LE' or x == 'OP_LT' or x == 'OP_NE':
            return 20
        elif x == 'KW_qui':
            return 21
        elif x == 'KW_sarme':
            return 22
        elif x == 'string':
            return 23
        elif x == 'KW_yulmavene':
            return 24
        elif x == 'DEL_LCB':
            return 25
        elif x == 'DEL_RCB':
            return 26
        elif x == '$':
            return 27

    def notTerminals(self, X):
        if X == 'Stmts':
            return 28
        elif X == 'Stmt':
            return 29
        elif X == 'If':
            return 30
        elif X == 'Else':
            return 31
        elif X == 'Expr':
            return 32
        elif X == 'Arit':
            return 33
        elif X == 'Factor':
            return 34
        elif X == 'Rel':
            return 35
        elif X == 'Log':
            return 36
        elif X == 'For':
            return 37
        elif X == 'Forexpr':
            return 38
        elif X == 'Postfix':
            return 39
        elif X == 'Read':
            return 40
        elif X == 'Write':
            return 41
        elif X == 'Type':
            return 42
        elif X == 'Declaration':
            return 43
        elif X == 'Function':
            return 44
        elif X == 'Params':
            return 45

    # Semântico => S-Atribuído
    # O que vai ser avaliado de aspecto semântico? (Especificação)
    #
    #   Tabela de Símbolos (constrói conforme roda o sintático)
    #       Ex: x + y
    #           x já foi declarado? olha na tabela
    #           y já foi declarado? olha na tabela
    #           eles são do mesmo tipo? preciso converter? pode parar ou fazer um cast
    #               Especificar que operações só podem com tipos iguais !!!
    #               Pode-se fazer uma coerção tbm

    def start(self):
        # Verificar erros léxicos
        print("\n")

        buffer = 0

        while True:
            top = self.stack.items[len(self.stack.items)-1]
            print("top: ", top)

            # Olha o topo da lista de tokens
            action = self.tableSyntax[top][self.terminals(
                self.lex.tokens_list[buffer].getType())]

            print(self.lex.tokens_list[buffer].getType())

            if action[0] == 's':
                self.shift(int(action[1:]), buffer)
                buffer += 1
            elif action[0] == 'r':
                self.reduce(int(action[1:]), buffer)
            elif action[0] == 'e':
                print("Error State...")
            else:
                print("Something is wrong...")

            # 0, hyaline, 9
            # 0, hyaline, 9, 'main', 23
            # 0, hyaline, 9, 'main', 23, (, 40
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15, 'sum', 36
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15, 'sum', 36, =, 52
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15, 'sum', 36, =, 52, '5', 34 => R23
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15, 'sum', 36, =, 52, N
            # 0, hyaline, 9, 'main', 23, (, 40, ), 57, {, 82, note, 15, 'sum', 36, =, 52, N, 74
            # OBS.: 74 com '+' não tem na tabela da gramática, verificar problema!

    def shift(self, state, buffer):
        print('Sstate: ', state)
        print('Sbuffer', buffer)

        self.stack.push(self.lex.tokens_list[buffer].getLexema())
        self.stack.push(state)
        print(self.stack.items)

    def reduce(self, state, buffer):
        # Reduce => exemplo: R3
        # Vai para a produção 3
        # Desempilha num de coisas do lado direito * 2
        # Substitui pelo oq ta no lado esquerdo
        # Da match com os dois últimos elementos da pilha
        # Grava o resultado na pilha

        for x in range(0, self.sizeProduction[state]):
            self.stack.pop()
            self.stack.pop()

        self.stack.push(self.productions[state])
        action = int(self.tableSyntax[self.stack.items[len(
            self.stack.items)-2]][self.notTerminals(self.stack.items[len(self.stack.items)-1])])
        self.stack.push(action)

        print(self.stack.items)


sync = Syntactic()
sync.start()
