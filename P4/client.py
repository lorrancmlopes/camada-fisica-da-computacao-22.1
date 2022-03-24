
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

serialName = 'COM4'                  # Windows(variacao de)



def main():
    try:
        #declaramos um objeto do h0 enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        com1 = enlace('COM4') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #endereço da imagem a ser transmitida
        imageR = "img/smallImage1.png"
        print("Carregando imagem para transmissão: ")
        print("-{}".format(imageR))
        print("-----------------")
        data = open(imageR, 'rb').read() #imagem em bytes!
        
        # calculo da quantidade de pacotes de 114
        quantidade = ceil(len(data)/114) # divide e arredonda pra cima
        quantidade +=1 # um pacote a mais para o handshake
        
        #contrução do head
        h0,h1, h2, h3, h4, h5, h6, h7, h8, h9 = None, None, None, None, None, None, None, None, None, None
        EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        recebimentoOK = 2
        recebimentoOK = recebimentoOK.to_bytes(2,'big')
        pedidoReenvio = 3
        pedidoReenvio = pedidoReenvio.to_bytes(2, 'big')
        
        #handShake
        HANDSHAKE = True
        FIM = False
        h0  = 0
        h0 = h0.to_bytes(1, 'big')                            # h0 de mensagem
        h1, h2 = 1, 1                                           # livre
        h1, h2 = h1.to_bytes(1,'big'), h2.to_bytes(1, 'big')    # número total de pacotes no arquivos
        h3 = quantidade.to_bytes(1, 'big')                      # 
        h4 = h4.to_bytes('1', 'big')                            # número do pacote sendo enviado
        h5 = h5.to_bytes('1', 'big')                            # h0 handshake = id do arquivo, h0 dados = tamanho payload
        h6 = h6.to_bytes('1', 'big')                            # pacote solicitado quando tem erro
        h7 = h7.to_bytes('1', 'big')                            # último pacote recebido com sucesso
        h8 = h8.to_bytes('1', 'big')                            # CRC
        h9 = h9.to_bytes('1', 'big')                            # CRC
       
        PAYLOAD = 0

        #print(f"tamanho payload: {tamanhoPayload}")
        EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        HEAD = [h0,h1, h2, h3, h4, h5, h6, h7, h8, h9]
        pacoteHandshake = HEAD + PAYLOAD + EOP
        #print('pacote handshake')
        #print(pacoteHandshake)

        pacoteHandshake=b''.join(pacoteHandshake)
        txBuffer = pacoteHandshake

        
        
        while HANDSHAKE:
            tentarNovamente = 0
            # Transmite dados
            print("Solicitando conexão com o server .... ")
            print(int.from_bytes(txBuffer[:1], 'big'))
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

            while h4 < int.from_bytes(h3, 'big'):
                print("entrouuuuuuu")
                h0 = 0
                h4  += 1
                print(f"Numero do pacote: {h4}")
                tamanhoPayload = 114 # 114 bytes (maximo possível)
                
                if h4 == int.from_bytes(h3, 'big'):
                    print("+++++++++++++++++++++++++++++++++")
                    print("Último pacote!")
                    PAYLOAD = data[fatiamentoInicial:]
                    print(f"Len do último PayLoad: {len(PAYLOAD)}")
                    tamanhoPayload = len(PAYLOAD)

                else:
                    PAYLOAD = data[fatiamentoInicial:fatiamentoFinal]

                fatiamentoInicial += 114
                fatiamentoFinal += 114
                HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                pacote = HEAD + PAYLOAD + EOP
                
                # Transmite pacote
                txBuffer=b''.join(pacote)
                
                print(f"Tamanho do payload: {int.from_bytes(txBuffer[5], 'big')}")
                print(f"Enviando pacote n° {h4} de {int.from_bytes(h3, 'big')} ... ")
                print("##################################")
                print(f'tamanho pacote len(txbuffer): {len(txBuffer)} txBuffer {txBuffer}')

                com1.sendData(np.asarray(txBuffer)) #dados as np.array
                time.sleep(0.10)
                #Conferência de dados para envio do próximo pacote:
                print("Conferindo..")
                
                rxBuffer, nRx = com1.getData(14)
                time.sleep(0.03)
                h0 = rxBuffer[0]
                print(f"Tipo: {int.from_bytes(h0, 'big')}; Recebimento ok: {int.from_bytes(recebimentoOK, 'big')} \n")
                if h0 == recebimentoOK:
                    print("Código de recebimento ok")
                elif h0 == pedidoReenvio:
                    print("Reenvio")
                    h3 = int.from_bytes(h3, 'big')
                    h3 += 1
                    h3 = h3.to_bytes(2,'big')
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
