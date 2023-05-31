#Round-Robin
#Lucas Prado
#--------------------------------------------

class Robin:
    def __init__(self):
        self.time = 0;
        self.process = []
        self.size = []
        self.arrival = []
        self.standby = []
        self.timeLine = []
        self.counter = 0;

        self.processos = []
        self.chegada = []
    
        file = open('process.txt', 'r')
        lines = file.readlines()
        file.close()
        i = 0
        for line in lines:
            if i == 0:
                self.time = int(line.strip())#tira a formatacao
            columns = line.split()
            if columns[0] == "Processo":
                self.process = list(columns[1:])
            elif columns[0] == "Tempo":
                self.size = list(map(int, columns[1:]))
            elif columns[0] == "Chegada":
                self.arrival = list(map(int, columns[1:]))
            i+=1
        self.test()
        self.processos = list(self.process)
        self.chegada = list(self.arrival)
        self.implementation()
        self.status()
    
    def test(self):
        print('Quantum', self.time)
        print("Processos:", self.process)
        print("Tempos:", self.size)
        print("Chegadas:", self.arrival)

    def implementation(self):
        #print(minimum, '\n', position)
        #print(self.process)
        while len(self.arrival) == 0 or (len(self.standby) > 0 and self.counter == 2):
            #print("Entrou no if")
            item = self.standby.pop(0)
            self.process.insert(0, item[0])
            self.size.insert(0, item[1])
            self.arrival.insert(0, item[2])
            if len(self.standby) == 0:
                self.counter = 0

        if len(self.arrival) != 0:
            minimum = min(self.arrival)
        else:
            minimum = self.standby[0][2]
            
        if (len(self.arrival) > 0 and (self.size[self.arrival.index(minimum)] <= self.time)):
            self.timeLine.append((self.size[self.arrival.index(minimum)], self.process[self.arrival.index(minimum)]))
            self.process.pop(self.arrival.index(minimum))
            self.size.pop(self.arrival.index(minimum))
            self.arrival.remove(minimum)
            if len(self.standby) > 0:
                self.counter+=1
        elif(len(self.arrival) > 0):
            self.timeLine.append((self.time, self.process[self.arrival.index(minimum)]))
            self.size[self.arrival.index(minimum)] = (self.size[self.arrival.index(minimum)] - self.time)
            #print(self.size)
            self.standby.append((self.process.pop(self.arrival.index(minimum)), self.size.pop(self.arrival.index(minimum)), self.arrival.pop(self.arrival.index(minimum))))
            self.counter+=1
        else:
            self.timeLine.append((self.standby[0][0], self.standby[0][1]))
        # print(self.size)
        # print(self.standby)
        # print(self.arrival)
        while len(self.process) > 0 or len(self.standby) > 0:
            self.implementation()

    def status(self):
        #TIMELINE
        counter = 0
        new_timeLine = []
        for tuple in self.timeLine:
            counter += tuple[0]
            new_timeLine.append((counter, tuple[1]))
        start = '0'
        copia_timeLine = list(new_timeLine)
        for i in range(len(new_timeLine)):
            start += '----[' + new_timeLine[i][1] + ']----' + str(new_timeLine[i][0])

        print(start)
        dicionario_tuplas = {}

        for tupla in copia_timeLine:
            key = tupla[1]
            value = tupla[0]

            if key not in dicionario_tuplas or value > dicionario_tuplas[key][0]:
                dicionario_tuplas[key] = tupla
        novo_array_tupla = sorted(list(dicionario_tuplas.values()))
        novo_array_tupla = sorted(novo_array_tupla, key=lambda x: x[1])
        #print(novo_array_tupla)
        # print(self.processos)

        #CALCULO DO TEMPO MEDIO DE RESPOSTA
        soma_resposta = sum([novo_array_tupla[i][0] - self.chegada[i] for i in range(len(novo_array_tupla))])
        media = soma_resposta / len(self.chegada)
        print('Tempo medio de resposta e:', media)


        #print(self.chegada)

        #tempo espera (termino do anterior - final do menor + termino do anterior(menor) - tempo chegada)
        resultado = []
        anterior = 0

        for item in copia_timeLine:
            valor = item[0] - anterior
            resultado.append(valor)
            anterior = item[0]

        resultado.pop()#remover o 2 que sobra
        copia_timeLine.pop(0)
        saida_trocada = [(resultado[i], item[1]) for i, item in enumerate(copia_timeLine)]

        #print(saida_trocada)

        nova_lista = []
        soma_anteriores = 0

        for tupla in saida_trocada:
            numero = tupla[0] + soma_anteriores
            nova_tupla = (numero, tupla[1])
            nova_lista.append(nova_tupla)
            soma_anteriores = numero

        #print(nova_lista)

        maiores_numeros = {}

        for tupla in nova_lista:
            numero, letra = tupla
            if letra not in maiores_numeros or numero > maiores_numeros[letra]:
                maiores_numeros[letra] = numero

        nova_lista_sem_repeticao = [(numero, letra) for letra, numero in maiores_numeros.items()]
        nova_lista_sem_repeticao.sort(key=lambda x: x[1])
        # print(new_timeLine)
        # print(nova_lista_sem_repeticao)

        # Criar um dicionário para armazenar a contagem das letras no new_timeLine
        contagem_letras = {}
        for item in new_timeLine:
            _, letra = item
            if letra in contagem_letras:
                contagem_letras[letra] += 1
            else:
                contagem_letras[letra] = 1

        # Subtrair 5 do primeiro array para cada letra repetida no new_timeLine
        nova_lista_corrigida = []
        for item in nova_lista_sem_repeticao:
            valor, letra = item
            if letra in contagem_letras and contagem_letras[letra] > 1:
                valor -= self.time
                contagem_letras[letra] -= 1
            nova_lista_corrigida.append((valor, letra))

        # Imprimir o resultado
        # print(nova_lista_corrigida)
        # print(self.chegada)

        media_espera = []
        for i in range(len(nova_lista_corrigida)):
            valor = nova_lista_corrigida[i][0] - self.chegada[i]
            letra = nova_lista_corrigida[i][1]
            media_espera.append((valor, letra))

        #print(media_espera) media cada um
        media_sem_letras = [tupla[0] for tupla in media_espera]
        media_esperaFinal = sum(media_sem_letras) / len(media_sem_letras)
        print('Tempo medio de resposta e:', media_esperaFinal)
        
robin = Robin()