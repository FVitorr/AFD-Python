'''
1. Desenvolva um classe para AFD. Essa classe, dentre outros métodos, deve incluir:
... salvar o AFD em um arquivo texto;
... carregar o AFD de um arquivo texto;
... criar cópia do AFD.
'''

class AFD:
    def __init__(self, alfabeto):
        self.alfabeto = str(alfabeto)
        self.estados = []
        self.transicoes = dict()
        self.estado_inicial = None
        self.estados_final = []

        self.__estadoAtual = None
        self.__deuErro = False

    def __str__(self) -> str:
        s = "AFD (E, A, T, i, F): \n"
        str_ = [str(self.estados),str(list(self.alfabeto)),str(self.estados_final)]
        for st in str_:
            str_[str_.index(st)] = st.replace("[", "{").replace("]", "}")
        s += f"    E = {str_[0]} \n    A = {str_[1]} \n    T = {'{'}"
        for (e,a) in self.transicoes.keys():
            s += f" ({e}, {a}) --> {self.transicoes[(e,a)]},"
        s += f"{'}'} \n    i = {self.estado_inicial} \n    F = {str_[2]}"
        return s
        
    def defEstados(self,estados:list):
        self.estados = estados

    def setEstadoInicial(self,estado: str):
        if estado in self.estados:
            self.estado_inicial = estado
            self.__estadoAtual = estado
            return True
        return False
    
    def setEstadoFinal(self,estados: list):
        for i in estados: #Verificar se os elementos da lista passada se fazem parte dos estados pre estabelecidos
            if i not in self.estados:
                return False
        
        for estado in estados: self.estados_final.append(estado)
        return True
    
    def resetEstadoFinal(self,estados: list):
        self.estados_final = []
        self.setEstadoFinal(estados=estados)

    def setTransicao(self,origem,valor,destino):
        #Criar transição (origem, valor) -> destino
        if origem not in self.estados or destino not in self.estados: return False
        if str(valor) not in self.alfabeto or len(str(valor)) != 1: return False

        self.transicoes[(str(origem), str(valor))] = str(destino)
        return True

    def resetTransicao(self,origem,valor,destino):
        try:
            self.transicoes[(origem, valor)] = destino
            return True
        except:
            return False

    def move(self, cadeia):
        for simbolo in  cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                return -1
            if (str(self.__estadoAtual), str(simbolo)) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                return -1 
            
        return self.__estadoAtual

    def mult_move(self,cadeias : list):
        resul = {}
        for cadeia in cadeias:
            if (self.move(cadeia) in self.estados_final):
                resul[cadeia] = 'Valido'
            else:
                resul[cadeia] = 'Invalido'
        return resul

    def salvar(self, arquivo: str):
        with open(arquivo, "w") as arq:

            def con_string(dicionario: dict):
                return {(str(chave[0]),str(chave[1])): str(valor) for chave, valor in dicionario.items()}
            
            arq.write("Estados: " + str(self.estados) + "\n")
            arq.write("Alfabeto: '" + str((self.alfabeto)) + "'\n") 
            arq.write(f"Transicoes: {con_string(self.transicoes)}\n")
            arq.write("Estado Inicial: " + str(self.estado_inicial) + "\n")  
            arq.write("Estados finais: " + str(self.estados_final) + "\n")
        return True
    
    def carregar(self, arquivo: str):
        try:
            with open(arquivo, "r") as arq:
                dados = arq.read()

            dados = dados.split("\n")
            for linha in dados:
                if linha.startswith("Estados: "):
                    self.estados = eval(linha.split("Estados: ")[1])
                elif linha.startswith("Alfabeto: "):
                    self.alfabeto = eval(linha.split("Alfabeto: ")[1])
                elif linha.startswith("Transicoes: "):
                    self.transicoes = eval(linha.split("Transicoes: ")[1])
                elif linha.startswith("Estado Inicial: "):
                    self.estado_inicial = str(linha.split("Estado Inicial: ")[1])
                    self.__estadoAtual = self.estado_inicial
                elif linha.startswith("Estados finais: "):
                    self.estados_final = eval(linha.split("Estados finais: ")[1])
            return True
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return False

    def copyAFD(self):
        nAfd = AFD(self.alfabeto)
        nAfd.defEstados(self.estados.copy())
        nAfd.setEstadoInicial(self.estado_inicial)  # Copiar estado inicial
        nAfd.setEstadoFinal(self.estados_final.copy())  # Copiar estados finais
        nAfd.transicoes = self.transicoes.copy()  # Copiar dicionário de transições

        return nAfd
    
    '''
    2. Algoritmo de Minimização, incluindo:
    ... desenvolva um procedimento para calcular os estados equivalentes de um AFD.
    ... desenvolva um procedimento para testar a equivalência entre dois AFD fornecidos.
    ... desenvolva um procedimento para calcular o autômato minimizado para um AFD fornecido.
    '''

if __name__ == "__main__":
    
    nAfd = AFD("01")
    nAfd.carregar("afd.txt")
    print(nAfd)

    r = nAfd.mult_move(["011","101001","11101","01100101"])
    print(f"Multiplos Teste: {r}")
