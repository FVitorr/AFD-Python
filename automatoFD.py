'''
1. Desenvolva um classe para AFD. Essa classe, dentre outros métodos, deve incluir:
... salvar o AFD em um arquivo texto;
... carregar o AFD de um arquivo texto;
... criar cópia do AFD.
'''
import random
letras = 'abcdefghijklmnopqrstuvwxyz'  # Sequência de letras minúsculas



class AFD:
    def __init__(self, alfabeto: str):
        self.alfabeto = str(alfabeto)
        self.estados = []
        self.transicoes = dict()
        self.estado_inicial = None
        self.estados_final = []

        self.__estadoAtual = None
        self.__deuErro = False

    def __str__(self) -> str: #Metodo que permite chamar print(afd)
        s = "AFD (E, A, T, i, F): \n"
        str_ = [str(self.estados),str(list(self.alfabeto)),str(self.estados_final)]
        for st in str_:
            str_[str_.index(st)] = st.replace("[", "{").replace("]", "}")
        s += f"    E = {str_[0]} \n    A = {str_[1]} \n    T = {'{'}"
        for (e,a) in self.transicoes.keys():
            s += f" ({e}, {a}) --> {self.transicoes[(e,a)]},"
        s += f"{'}'} \n    i = {self.estado_inicial} \n    F = {str_[2]}"
        return s
        
    def defEstados(self, estados: list):
        self.estados = [str(estado) for estado in estados]

    def newEstado(self,estado : str):
        self.estados.append(estado)

    def setEstadoInicial(self,estado: str):
        if str(estado) in str(self.estados):
            self.estado_inicial = str(estado)
            self.__estadoAtual = str(estado)
            return True
        return False
    
    def setEstadoFinal(self,estados: list):
        for i in estados: #Verificar se os elementos da lista passada se fazem parte dos estados pre estabelecidos
            if i not in self.estados:
                return False
        
        for estado in estados: self.estados_final.append(str(estado))
        return True
    
    def resetEstadoFinal(self,estados: list):
        self.estados_final = []
        self.setEstadoFinal(estados=estados)

    def setTransicao(self,origem,valor,destino):
        #Criar transição (origem, valor) -> destino
        if str(origem) not in self.estados or str(destino) not in self.estados: return False
        if str(valor) not in self.alfabeto or len(str(valor)) != 1: return False

        self.transicoes[(str(origem), str(valor))] = str(destino)
        return True

    def resetTransicao(self,origem,valor,destino):
        try:
            self.transicoes[(origem, valor)] = destino
            return True
        except:
            return False
        
    def ref_afd(self,n_estado: list):
        if len(n_estado) != len(self.estados): return False
        #Criar dic Old_name: New_name
        rename = {}
        i = 0
        for est in sorted(self.estados):
            rename[est] = n_estado[i]
            i+=1
        #print(rename)       
        r_afd = AFD(self.alfabeto)
        r_afd.defEstados(n_estado)
        r_afd.setEstadoFinal([rename[est] for est in self.estados_final])
        r_afd.setEstadoInicial(rename[self.estado_inicial])

        for key in self.transicoes.keys():
            r_afd.transicoes[(rename[key[0]],key[1])] = rename[self.transicoes[key]]

        return r_afd

    def move(self, cadeia):
        self.__estadoAtual = self.estado_inicial
        for simbolo in  cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                return -1
            if (str(self.__estadoAtual), str(simbolo)) in self.transicoes.keys():
                novoEstado = self.transicoes[(str(self.__estadoAtual), str(simbolo))]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                return -1 
            
        return self.__estadoAtual

    def mult_move(self,cadeias : list):
        resul = {}
        for cadeia in cadeias:
            if str(self.move(cadeia)) in map(lambda x: str(x), self.estados_final):
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
        nAfd.setEstadoInicial(self.estado_inicial)
        nAfd.setEstadoFinal(self.estados_final.copy())  # Copiar estados finais
        nAfd.transicoes = self.transicoes.copy()  # Copiar dicionário de transições

        return nAfd
    
    '''
    2. Algoritmo de Minimização, incluindo:
    ... desenvolva um procedimento para calcular os estados equivalentes de um AFD.
    ... desenvolva um procedimento para testar a equivalência entre dois AFD fornecidos.  --> FAZER AINDA
    ... desenvolva um procedimento para calcular o autômato miD fornecido.
    nimizado para um AF
    -> Requisitos:
        1- Estados Inacessíveis são Indiferentes ao processo (Devem ser Ignorados)
        2- O automato deve ser completo (Todas as função de transição presente)
    '''
    def remE_Inace(self):
        n_afd = self.copyAFD()
        acess = set(n_afd.transicoes[destino] for destino in n_afd.transicoes)
        rem_state = [estado for estado in n_afd.estados if str(estado) != str(n_afd.estado_inicial) and str(estado) not in acess]

        for rem_stat in rem_state:
            n_afd.estados.remove(rem_stat)
            for letter in n_afd.alfabeto:
                n_afd.transicoes.pop((rem_stat, letter), None)

        return n_afd

    def Compl_afd(self):
        def estadoErro():
            while(1):
                err = "ee"
                if str(err) not in self.estados:
                    self.newEstado(str(err))
                    for i in self.alfabeto:
                        self.setTransicao(str(err), i, str(err))
                    return err
        for estado in self.estados:
            for letra in self.alfabeto:
                if (str(estado), str(letra)) not in self.transicoes:
                    self.setTransicao(estado,letra, estadoErro())

    def ver_equal(self):
        est = sorted(self.estados)  # Ordena os estados

        def create_dict():
            dic = {}
            key_list = []
            for i in range(1, len(est)):
                for j in range(0, i):
                    if est[i] != est[j]:
                        dic[(str(est[i]), str(est[j]))] = 0
                        key_list.append((str(est[i]), str(est[j])))
            return dic, key_list

        def print_table(table):
            str_ = ''
            for i in range(1, len(est)):
                str_ += '\n'
                for j in range(0, i):
                    if est[i] != est[j]:
                        str_ += str(table[(str(est[i]), str(est[j]))])
            return str_

        # 1ª - Marcar estados não equivalentes inicialmente
        non_final_states = set([estado for estado in self.estados if estado not in self.estados_final])
        key = [set((str(j), str(i))) for j in non_final_states for i in self.estados_final]

        table, key_list = create_dict()
        for key_ in table.keys():
            if set(key_) in key:
                table[key_] = 1

        # 2ª - Criar dicionário de quem chega ao estado
        # "Nome_do_estado" : [("qm_chega_A")("qm_chega_B")]
        # chega = {1: [('0', 'b'), ('1', 'a')], 2: [('0', 'a'), ('4', 'b'), ('5', 'a')]}
        chega = dict()
        alphabet = sorted(list(self.alfabeto))

        for est_ in est:
            for key in self.transicoes.keys():
                if self.transicoes[key] == str(est_):
                    if str(est_) not in chega.keys():
                        chega[str(est_)] = [key]
                    else:
                        chega[str(est_)].append(key)

        # 3ª - Analisar a "Tabela"
        an = []
        while True:
            changes = False  # Variável para rastrear se houve mudanças nesta iteração
            for key_ in key_list: #Key_list variaveis marcadas na primeira etapa
                if table[key_] >= 1: #Se for 0 não deve ser analisado
                    ch, ch1 = key_ #Chave para encontrar qm_chega ao estado com 1 simbolo
                    for i in chega[ch]:
                        for j in chega[ch1]:
                            if (i[1] == j[1]): #verificar se são mesma letras
                                pair = (j[0], i[0])
                                if pair not in an: 
                                    an.append(pair)
                                    for keys in table.keys():
                                        if set(keys) == set(pair):
                                            table[keys] += 1 #incrementar um a chave encontrada com a concatenção dos estados
                                    changes = True  # Marcamos que houve uma mudança
            if not changes:
                break  # Se não houver mudanças nesta iteração, saia do loop

        #print(an)

        print(print_table(table=table))
        # 4ª - Criar um novo AFD minimizado
        estados_eq = [key_ for key_ in table.keys() if table[key_] == 0]
        # n_est = [str(elemento) for elemento in est]

        # for est_eq in estados_eq:
        #     for i in est_eq:
        #         try:
        #             n_est.remove(i)
        #         except:
        #             pass
        # estados_eq.append(n_est)

        # print(estados_eq)
        return estados_eq


    def min_afd(self):
        #Remover Inacessiveis e completar o automato
        nAFD = self.remE_Inace()
        nAFD.Compl_afd()
        #Determinar estados
        estado_eq = nAFD.ver_equal()
        ren_estados = {} # old_valor : new_valor
        n_est = [str(elemento) for elemento in nAFD.estados]

        for el in estado_eq:
            key1,key2 = el
            ren_estados[key1] = el[0]
            ren_estados[key2] = el[0]
        
        for est in n_est:
            if est not in ren_estados:
                ren_estados[ str(est)] = str(est)

        #print(ren_estados)
        #Novos estados Obtidos
        n_estados = [ren_estados[key] for key in ren_estados.keys()]
        n_estados = sorted(list(set(n_estados)))
        #print(n_estados)
        #Refazer transiçoes
        n_trans = {}
        for trans, value in nAFD.transicoes.items():
            estado = ren_estados[trans[0]]
            letter = trans[1]
            destino = ren_estados[value]

            n_trans[(estado,letter)] = destino
        #print(n_trans)

        #Novo AFD MINIMIZADO
        n_AFD = AFD(nAFD.alfabeto)
        n_AFD.transicoes = n_trans
        
        n_AFD.defEstados(n_estados)
        n_AFD.setEstadoInicial(ren_estados[nAFD.estado_inicial])
        est_F = [ren_estados[str(est)] for est in nAFD.estados_final]
        n_AFD.setEstadoFinal(list(set(est_F)))

        return n_AFD
    


    def eq_AFD(self,afd):
        #remover estados sem acesso
        self = self.remE_Inace()
        afd = afd.remE_Inace()
        #Verificar se os estados tem nomes iguais
        if (set(self.estados) == set (afd.estados)):
            #Mudar os estados de um automoto para evitar conflito na hora de verificar a equivalenia
            afd = afd.ref_afd([ "q" +str(n) for n in range(0,len(afd.estados))])

        #Criar um automo que possua a uniao dos estados dos automatos
        uAFD = self.copyAFD()
        if uAFD.alfabeto not in afd.alfabeto:
            uAFD.alfabeto = uAFD.alfabeto + afd.alfabeto
        
        uAFD.estados = uAFD.estados + afd.estados
        uAFD.estados_final = uAFD.estados_final + afd.estados_final
        
        for key in afd.transicoes.keys():
            uAFD.transicoes[key] = afd.transicoes[key]

        #Verificar Equivalencia entre os estados
        est_eq = uAFD.ver_equal()
        if (afd.estado_inicial,uAFD.estado_inicial) in est_eq:
            return True
        else:
            return False
        

    '''
    3. Algoritmos para operar com linguagens (conjuntos), incluindo:
    ... desenvolva um procedimento para multiplicar dois AFDs
    ... desenvolva procedimentos para união, intercessão, complemento e diferença
    '''

    def mult_afd(self,sAFD):
        #Verificar se tem mesmo alfabeto:
        if set(list(self.alfabeto)) != set(list(sAFD.alfabeto)):
            return -1
        
        #Minimizar os automatos antes de multiplicar
        afd1 = self.min_afd()
        afd2 = sAFD.min_afd()
        
        n = AFD(self.alfabeto)

        p_estado = afd1.estados
        s_estado = afd2.estados

        # Multiplicação dos conjuntos
        mult_estados = set([(str(x) , str(y)) for x in p_estado for y in s_estado])

        transicao = {}
        for i in mult_estados:
            n.estados.append(str(i[0])+str(i[1]))
            for letter in afd1.alfabeto:
                key_one = afd1.transicoes[(i[0],letter)]
                key_two = afd2.transicoes[(i[1],letter)]

                transicao[(i[0]+i[1],letter)] = key_one + key_two
        
        #Definir estados Iniciais
        n.setEstadoInicial(afd1.estado_inicial + afd2.estado_inicial)
        #Definir Transiçoes
        n.transicoes = transicao
        return n,(afd1.estados_final,afd2.estados_final)


    def uniao(self,sAfd):
        #Selecionar Estados Finais 
        afd, est_f = self.mult_afd(sAFD=sAfd)
        estF_uniao = set()

        for estado in afd.estados:
            for final in est_f[0]:
                if final in estado:
                    estF_uniao.add(estado)

            for final in est_f[1]:
                if final in estado:
                    estF_uniao.add(estado)
        
        afd.estados_final = list(estF_uniao)
        print("Uniao: ",afd)
        return afd
 
    def intercessao(self,sAfd):
        #Selecionar Estados Finais 
        afd, est_f = self.mult_afd(sAFD=sAfd)
        est_ft = set([str(i) + str(j) for i in est_f[0] for j in est_f[1]])
        #Garantir q o estado existe no AFD
        estF_int = set()
        for p_estadoFinal in est_ft:
            if p_estadoFinal in afd.estados:
                estF_int.add(p_estadoFinal)

        afd.estados_final = list(estF_int)
        return afd

    def complemento(self):
        afd = self.copyAFD()
        #Garantir q o AFD é Completo
        afd.Compl_afd()
        afd.estados_final = [estado for estado in afd.estados if estado not in afd.estados_final ]            
        print(afd)
        return afd
        
    def diferença(self,subtraendo_AFD):
        # B - A = Os estados finais de B com os estados não finais de A
        sAFD = subtraendo_AFD.complemento()
        return self.intercessao(sAFD)


                      

if __name__ == "__main__":
    
    nAfd = AFD("01")
    nAfd.carregar("afd1.txt")

    mul = AFD("01")
    mul.carregar("afd2.txt")
    print(mul)

    print(nAfd)
    #nAfd.mult_afd(mul)

    # nAfd.uniao(mul)
    # nAfd.intercessao(mul)

    # print(mul.complemento())

    # print(nAfd.diferença(mul))

    if (mul.eq_AFD(mul)):
        print("Equivalente")
    else:
        print("n Equivalente")
    #mul.ref_afd(["A","B","C","D"])
    
    
