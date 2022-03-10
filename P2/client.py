
from ntpath import join
from os import kill
from scipy import rand
from sqlalchemy import false
from enlace import *
from math import ceil
import time
import numpy as np
import random
import sys # para pegar o tamanho em bytes

serialName = "COM3"                  # Windows(variacao de)



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        com1 = enlace('COM3') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        # time.sleep(.2)
        # com1.sendData(b'00')
        # print("Enviou o 1°")
        # time.sleep(1) 
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        # print("Sucesso na comunicação")

        #endereço da imagem a ser transmitida
        imageR = "img/smallImage2.png"
        print("Carregando imagem para transmissão: ")
        print("-{}".format(imageR))
        print("-----------------")
        data = open(imageR, 'rb').read() #imagem em bytes!
        print(data[:114], len(data[:114]))
        
        # calculo da quantidade de pacotes de 114
        quantidade = ceil(len(data)/114) # divide e arredonda pra cima
        quantidade +=1 # um pacote a mais para o handshake
        
        #contrução do head
        type, numeroPacote, totalPacotes, tamanhoPayload, origem, destino = None, None, None, None, None, None
        EOP = 2022 #vou deixar um número qualquer por enquanto
        recebimentoOK = 2
        recebimentoOK = recebimentoOK.to_bytes(2,'big')
        pedidoReenvio = 3
        pedidoReenvio = pedidoReenvio.to_bytes(2, 'big')
        
        #handShake
        HANDSHAKE = True
        tipo  = 0
        tipo = tipo.to_bytes(2, 'big')
        totalPacotes = quantidade.to_bytes(2, 'big')
        tamanhoPayload = 0
        tamanhoPayload = tamanhoPayload.to_bytes(2, 'big')
        print(f"tamanho payload: {tamanhoPayload}")
        origem, destino, numeroPacote = 1, 1, 1
        origem, destino = origem.to_bytes(1, "big"), destino.to_bytes(1, "big")
        EOP = 2022
        EOP = EOP.to_bytes(4, 'big')
        pacoteHandshake = [tipo, numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload, origem, destino, EOP]
        pacoteHandshake=b''.join(pacoteHandshake)
        txBuffer = pacoteHandshake
        print(totalPacotes)
        barra = '\ '
        barra = barra.strip()
        print((str(pacoteHandshake).split("\\")))
        print("b'"+barra+(str(pacoteHandshake).split("\\"))[6]+barra+(str(pacoteHandshake).split("\\"))[7]+"'")
        
        print(barra)
        payL = (str(pacoteHandshake).split("\\"))[1][1:]+(str(pacoteHandshake).split("\\"))[2][1:]
        print(payL, int(payL, 16))
        print(int.from_bytes(b'\x00\x00', 'big'))
        while HANDSHAKE:
            tentarNovamente = None
            # Transmite dados
            print("Solicitando conexão com o server .... ")
            print(int.from_bytes(txBuffer[:2], 'big'))
            print(f"txBuffer: {txBuffer}")
            print(f"Len do txbuffer: {len(txBuffer)}")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            time.sleep(1)
            print("esperando resposta") 
              
            rxBuffer, nRx = com1.getData(14)
            print(f"rxbuffer: {rxBuffer}")
            print(int((str(rxBuffer).split("\\"))[1][1:]+(str(rxBuffer).split("\\"))[2][1:], 16))     
            if rxBuffer == [-5]: #quando tempo de resposta é >= 5 seg
                tentarNovamente = input("Servidor inativo. Tentar novamente? S/N:  ")
                if tentarNovamente != "S":
                    HANDSHAKE = False
                    print("Encerrando...")
                else:
                    com1.rx.clearBuffer()
            elif int((str(rxBuffer).split("\\"))[1][1:]+(str(rxBuffer).split("\\"))[2][1:], 16) == 0: #se os 2 primeiros bytes tem o valor 0, indica q é handshake
                print("Comunicação bem sucedida! (HANDSHAKE)")
                HANDSHAKE = False
        print("---------------------")
        print("Início do envio do arquivo: \n")
        fatiamentoInicial = 0
        fatiamentoFinal = 114
    
        while numeroPacote < int.from_bytes(totalPacotes, 'big'):
            print("entrouuuuuuu")
            pacoteHandshake = [tipo, numeroPacote, totalPacotes, tamanhoPayload, origem, destino, EOP]
            tipo = 0
            numeroPacote  += 1
            tamanhoPayload = 114 # 114 bytes (maximo possível)
            if numeroPacote == totalPacotes:
                payLoad = data[fatiamentoInicial:]
            else:
                payLoad = data[fatiamentoInicial:fatiamentoFinal]
            fatiamentoInicial += 114
            fatiamentoFinal += 114
            pacote = [tipo.to_bytes(2,'big'), numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload.to_bytes(2, 'big'), origem, destino, payLoad, EOP]
                # Transmite pacote
            txBuffer = pacote
            print(f"Enviando pacote n° {numeroPacote} de {int.from_bytes(totalPacotes, 'big')} ... ")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            print(txBuffer)
            time.sleep(0.05)
            #Confereência de dados para envio do próximo pacote:
            print("Conferindo..")
            
            rxBuffer, nRx = com1.getData(14)
            tipo = rxBuffer[:2]
            print(f"Tipo: {tipo}; Recebimento ok: {int.from_bytes(recebimentoOK, 'big')} \n")
            if tipo == recebimentoOK:
                pass
            if tipo == pedidoReenvio:
                totalPacotes += 1
                fatiamentoInicial -= 114
                fatiamentoFinal -= 114
                    
              # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()