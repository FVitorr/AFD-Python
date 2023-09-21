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
        s = "AFD (E, A, T, I, F): \n"
        str_ = [str(self.estados),str(self.alfabeto),str(self.estados_final)]
        for st in str_:
            str_[str_.index(st)] = st.replace("[", "{").replace("]", "}")
        s += f"    E = {str_[0]} \n    A = {str_[1]} \n    T = {'{'}"
        for (e,a) in self.transicoes.keys():
            s += f" ({e},{a}) --> {self.transicoes[(e,a)]},"
        s += f" {'}'} \n    i = {self.estado_inicial} \n    F = {str_[2]}"
        return s
        
    def defEstados(self,estados:list):
        self.estados = estados

    def setEstadoInicial(self,estado):
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
        if valor not in self.alfabeto or len(valor) != 1: return False

        self.transicoes[(origem, valor)] = destino
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
            if (self.__estadoAtual, simbolo) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                return -1 
            
        return self.__estadoAtual

    def salvar(self, arquivo: str):
        with open(arquivo, "w") as arq:
            arq.write("Estados: " + str(self.estados) + "\n")
            arq.write(f"Transicoes: {str(self.transicoes)}")
            arq.write("Estados finais: " + str(self.estados_final) + "\n")

        return True
    
    def carregar(self, arquivo: str):
        try:
            #Reset=ar para move operacionar de forma adequada
            self.__estadoAtual = self.estado_inicial
            self.__deuErro = False

            with open(arquivo, "r") as arq:
                lines = arq.readlines()
                for line in lines:
                    if line.startswith("Estados:"):
                        estados = eval(line.split("Estados: ")[1])
                        self.defEstados(estados)
                    elif line.startswith("Transicoes:"):
                        transicoes = eval(line.split("Transicoes: ")[1])
                        self.transicoes = transicoes
                    elif line.startswith("Estados finais:"):
                        estados_finais = eval(line.split("Estados finais: ")[1])
                        self.setEstadoFinal(estados_finais)
                        return True
            return False
        except:
            return False

    def copyAFD(self):
        nAfd = AFD(self.alfabeto)
        nAfd.defEstados(self.estados.copy())
        nAfd.setEstadoInicial(self.estado_inicial)  # Copiar estado inicial
        nAfd.setEstadoFinal(self.estados_final.copy())  # Copiar estados finais
        nAfd.transicoes = self.transicoes.copy()  # Copiar dicionário de transições

        return nAfd

if __name__ == "__main__":
    af = AFD("ab")

    af.defEstados([1,2,3,4])
    af.setEstadoInicial(1)
    af.setEstadoFinal([1])

    af.setTransicao(1,'a',2)
    af.setTransicao(1,'b',3)

    af.setTransicao(2,'a',1)
    af.setTransicao(2,'b',4)

    af.setTransicao(3,'a',4)
    af.setTransicao(3,'b',1)

    af.setTransicao(4,'a',3)
    af.setTransicao(4,'b',2)

    if af.move("ababab") in af.estados_final:
        print("Sucess")
    else:
        print("Erro")

    print(af)

    n = af.copyAFD()
    n.resetEstadoFinal([4])
    n.setEstadoInicial(2)

    n.resetTransicao(2,'c',2)

    print(n)

    if n.move("ababab") in n.estados_final:
        print("Sucess")
    else:
        print("Erro")
    
