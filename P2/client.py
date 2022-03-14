
from inspect import formatargvalues
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

serialName = "COM5"                  # Windows(variacao de)



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        com1 = enlace('COM5') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #endereço da imagem a ser transmitida
        imageR = "img/smallImage2.jpg"
        print("Carregando imagem para transmissão: ")
        print("-{}".format(imageR))
        print("-----------------")
        data = open(imageR, 'rb').read() #imagem em bytes!
        
        # calculo da quantidade de pacotes de 114
        quantidade = ceil(len(data)/114) # divide e arredonda pra cima
        quantidade +=1 # um pacote a mais para o handshake
        
        #contrução do head
        tipo, numeroPacote, totalPacotes, tamanhoPayload, origem, destino = None, None, None, None, None, None
        EOP = 2022 #vou deixar um número qualquer por enquanto
        recebimentoOK = 2
        recebimentoOK = recebimentoOK.to_bytes(2,'big')
        pedidoReenvio = 3
        pedidoReenvio = pedidoReenvio.to_bytes(2, 'big')
        
        #handShake
        HANDSHAKE = True
        FIM = False
        tipo  = 0
        tipo = tipo.to_bytes(2, 'big')
        totalPacotes = quantidade.to_bytes(2, 'big')
        tamanhoPayload = 0
        tamanhoPayload = tamanhoPayload.to_bytes(2, 'big')
        #print(f"tamanho payload: {tamanhoPayload}")
        origem, destino, numeroPacote = 1, 1, 1
        origem, destino = origem.to_bytes(1, "big"), destino.to_bytes(1, "big")
        EOP = 2022
        EOP = EOP.to_bytes(4, 'big')
        pacoteHandshake = [tipo, numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload, origem, destino, EOP]
        #print('pacote handshake')
        #print(pacoteHandshake)

        pacoteHandshake=b''.join(pacoteHandshake)
        txBuffer = pacoteHandshake

        
        
        while HANDSHAKE:
            tentarNovamente = None
            # Transmite dados
            print("Solicitando conexão com o server .... ")
            print(int.from_bytes(txBuffer[:2], 'big'))
            #print(f"txBuffer: {txBuffer}")
            #print(f"Len do txbuffer: {len(txBuffer)}")

            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            time.sleep(1)
            print("esperando resposta") 
              
            rxBuffer, nRx = com1.getData(14)
            #print(f"rxbuffer: {rxBuffer}")

            if rxBuffer == [-5]: #quando tempo de resposta é >= 5 seg
                tentarNovamente = input("Servidor inativo. Tentar novamente? S/N:  ")
                if tentarNovamente != "S":
                    HANDSHAKE = False
                    FIM = True
                    print("Encerrando...")
                    com1.disable()
                    break
                else:
                    com1.rx.clearBuffer()
            elif int((str(rxBuffer).split("\\"))[1][1:]+(str(rxBuffer).split("\\"))[2][1:], 16) == 0: #se os 2 primeiros bytes tem o valor 0, indica q é handshake
                print("Comunicação bem sucedida! (HANDSHAKE)")
                HANDSHAKE = False
        if not FIM:
            print("---------------------")
            print("Início do envio do arquivo: \n")
            fatiamentoInicial = 0
            fatiamentoFinal = 114

            time.sleep(1)

            while numeroPacote < int.from_bytes(totalPacotes, 'big'):
                print("entrouuuuuuu")
                pacoteHandshake = [tipo, numeroPacote, totalPacotes, tamanhoPayload, origem, destino, EOP]
                tipo = 0
                numeroPacote  += 1
                print(f"Numero do pacote: {numeroPacote}")
                tamanhoPayload = 114 # 114 bytes (maximo possível)
                if numeroPacote == int.from_bytes(totalPacotes, 'big'):
                    print("+++++++++++++++++++++++++++++++++")
                    print("Último pacote!")
                    payLoad = data[fatiamentoInicial:]
                    print(f"Len do último PayLoad: {len(payLoad)}")
                    tamanhoPayload = len(payLoad)

                    #muito crtl c + crtl v aqui agr
                else:
                    payLoad = data[fatiamentoInicial:fatiamentoFinal]
                fatiamentoInicial += 114
                fatiamentoFinal += 114
                pacote = [tipo.to_bytes(2,'big'), numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload.to_bytes(2, 'big'), origem, destino, payLoad, EOP]
                    # Transmite pacote
                txBuffer=b''.join(pacote)
                print(f"Tamanho do payload: {int.from_bytes(txBuffer[6:8], 'big')}")
                print(f"Enviando pacote n° {numeroPacote} de {int.from_bytes(totalPacotes, 'big')} ... ")
                print("##################################")
                print(f'tamanho pacote len(txbuffer): {len(txBuffer)} txBuffer {txBuffer}')

                com1.sendData(np.asarray(txBuffer)) #dados as np.array
                time.sleep(0.10)
                #Conferência de dados para envio do próximo pacote:
                print("Conferindo..")
                
                rxBuffer, nRx = com1.getData(14)
                time.sleep(0.03)
                tipo = rxBuffer[:2]
                print(f"Tipo: {int.from_bytes(tipo, 'big')}; Recebimento ok: {int.from_bytes(recebimentoOK, 'big')} \n")
                if tipo == recebimentoOK:
                    print("Código de recebimento ok")
                elif tipo == pedidoReenvio:
                    print("Reenvio")
                    totalPacotes = int.from_bytes(totalPacotes, 'big')
                    totalPacotes += 1
                    totalPacotes = totalPacotes.to_bytes(2,'big')
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