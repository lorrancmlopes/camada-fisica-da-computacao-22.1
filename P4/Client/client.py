
from enlace import *
from math import ceil
import time
import numpy as np
import random
import sys # para pegar o tamanho em bytes

serialName = 'COM5'                  # Windows(variacao de)



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        com1 = enlace('COM5') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #endereço da imagem a ser transmitida
        imageR = "img\smallImage2.jpg" #"C:\Users\lorra\OneDrive\Área de Trabalho\22.1\Camada\Projeto 2\camada-fisica-da-computacao-22.1\P4\Client\img\smallImage1.png"
        print("Carregando imagem para transmissão: ")
        print("-{}".format(imageR))
        print("-----------------")
        data = open(imageR, 'rb').read() #imagem em bytes!
        # calculo da quantidade de pacotes de 114
        quantidade = ceil(len(data)/114) # divide e arredonda pra cima
        # quantidade -=1 # um pacote a mais para o handshake
       

        # informações padrozinadas
        tipo1, tipo2, tipo3, tipo4, tipo5, tipo6 = 1, 2, 3, 4, 5, 6 
        #contrução do head
        h1, h2, h3, h4, h5, h6, h7, h8, h9 = None, None, None, None, None, 0, 0, 0, 0
        EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        recebimentoOK = 2
        recebimentoOK = recebimentoOK.to_bytes(2,'big')
        pedidoReenvio = 3
        pedidoReenvio = pedidoReenvio.to_bytes(2, 'big')
        
        #handShake
        HANDSHAKE = True
        FIM = False
        h0  = tipo1 # tipo1 == handshake
        h0 = tipo1.to_bytes(1, 'big') 
                                # tipo de mensagem
        h1, h2 = 1, 1                                           # livre
        h1, h2 = h1.to_bytes(1,'big'), h2.to_bytes(1, 'big')    # número total de pacotes no arquivos
        h3 = quantidade.to_bytes(1, 'big')  
                          # 
        h4 = 1
        print("aqui")
        h4 = h4.to_bytes(1, 'big')                            # número do pacote sendo enviado
        
        h5 = 13 # id do arquivo ( estamos montando o handshake)
        
        h5 = h5.to_bytes(1, 'big')                            # tipo handshake = id do arquivo, tipo dados = tamanho payload
         
        h6 = h6.to_bytes(1, 'big')                            # pacote solicitado quando tem erro
        h7 = h7.to_bytes(1, 'big')                            # último pacote recebido com sucesso
        h8 = h8.to_bytes(1, 'big')                            # CRC
        h9 = h9.to_bytes(1, 'big')                            # CRC
        
        PAYLOAD = None

        #print(f"tamanho payload: {tamanhoPayload}")
        EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
        pacoteHandshake = HEAD + EOP
        print('pacote handshake')
        print(pacoteHandshake)

        pacoteHandshake=b''.join(pacoteHandshake)
        txBuffer = pacoteHandshake

        
        CONT = None
        while HANDSHAKE:
            print("handshake")
            tentarNovamente = None
            # Transmite dados
            print("Solicitando conexão com o server .... ")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            time.sleep(5)
            print("esperando resposta") 
              
            rxBuffer, nRx = com1.getData(14)
            #print(f"rxbuffer: {rxBuffer}")

            if int((str(rxBuffer).split("\\"))[1][1:]) == tipo2: #se o 1° byte tem o valor tipo 2, indica q é handshake bem feito
                print("Comunicação bem sucedida! (HANDSHAKE)")
                HANDSHAKE = False
                CONT = 1
                
        if not FIM:

            print("---------------------")
            print("Início do envio do arquivo: \n")
            fatiamentoInicial = 0
            fatiamentoFinal = 114
            h0 = tipo3
            #h4 = int.from_bytes(h4, 'big')
            while int.from_bytes(h4, 'big') <= int.from_bytes(h3, 'big'):
                print("entrouuuuuuu")
                print(f"Numero do pacote: {int.from_bytes(h4, 'big')}")
                print(f"Numero total: {int.from_bytes(h3, 'big')}")
                
                if int.from_bytes(h4, 'big') == int.from_bytes(h3, 'big'):
                    print("+++++++++++++++++++++++++++++++++")
                    print("Último pacote!")
                    PAYLOAD = data[fatiamentoInicial:]
                    
                    print(f"Len do último PayLoad: {len(PAYLOAD)}")
                    h5 = len(PAYLOAD).to_bytes(1, 'big') # h5 passa a ser tamanho do payload

                else:
                    PAYLOAD = data[fatiamentoInicial:fatiamentoFinal]
                    h5 = len(PAYLOAD).to_bytes(1, 'big') # h5 passa a ser tamanho do payload
                    print(f"len data: {len(data)}, fatiamento: {fatiamentoInicial}/ {fatiamentoFinal} ")
                # fatiamentoInicial += 114
                # fatiamentoFinal += 114
                h0 = tipo3.to_bytes(1, 'big')
                #h4 = h4.to_bytes(1, 'big')
                HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                PAYLOAD = [PAYLOAD]
                pacote = HEAD + PAYLOAD + EOP
                txBuffer = b''.join(pacote)
                print("##################################")
                print(f'tamanho pacote len(txbuffer): {len(txBuffer)}')
                print(f"Tipo da msg a ser enviada: tipo{txBuffer[0]}")

                com1.sendData(np.asarray(txBuffer)) #dados as np.array
                print("envia msg cont - mdg t3")
                timer1 = time.time() #set timer 1
                timer2 = time.time() #set timer 2 (COLOCAR DENTRO DO enlaceTX)
                #Conferência de dados para envio do próximo pacote:
                print("Conferindo..")
                
                rxBuffer, nRx = com1.getData(14)
                print("fez o getData")
                
                tipo = rxBuffer[0]
                print(f"Tipo: {tipo}")
                print(f"Timer 1: {time.time() - timer1}")
                if tipo == tipo4:
                    print("Código de recebimento ok")
                    CONT += 1
                    h4 = int.from_bytes(h4, 'big')
                    h4  += 1
                    h4 = h4.to_bytes(1, 'big')
                    fatiamentoInicial += 114
                    fatiamentoFinal += 114
                    # recebimento ok tbm tem que ter o numero do ultimo pacote aferido pelo server
                # elif tipo == pedidoReenvio:
                #     print("Reenvio por pedido")
                #     h3 = int.from_bytes(h3, 'big')
                #     h3 += 1
                #     h3 = h3.to_bytes(2,'big')
                #     fatiamentoInicial -= 114
                #     fatiamentoFinal -= 114

                # elif tipo == tipo6:
                #     print("Código de ERRO recebimento pacote.\n")
                #     numPacoteReenvio = rxBuffer[6]
                #     print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                #     fatiamentoInicial = (numPacoteReenvio-1)*114
                #     fatiamentoFinal = (numPacoteReenvio)*114
                #     h4 = numPacoteReenvio-1
                #     h4 = h4.to_bytes(1,'big')
                #     CONT = numPacoteReenvio
                #     print("chegou aqui")

                elif time.time()-timer1 >5:
                    print("envia msg cont - msg t3")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    timer1 = time.time()
                    print("restart timer1")
                    print(f"Timer 2 está em: {time.time()-timer2}")
                    if time.time()-timer2 >20 and com1.rx.getBufferLen() != 14: # teste 
                        print("Timed out")
                        h0 = tipo5.to_bytes(1, 'big')
                        HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                        pacote = HEAD + EOP
                         # Transmite pacote
                        txBuffer=b''.join(pacote)
                        print(f"Tamanho do payload: {int.from_bytes(txBuffer[5], 'big')}")
                        print(f"Enviando pacote de timed out 'tipo6' ... ")
                        com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        time.sleep(0.01)
                        com1.disable()
                        break
                    else:
                        print("ENTROU NO ELSE")
                        rxBuffer, nRx = com1.getData(14)
                        print("fiz um getData")
                        tipo = rxBuffer[:1]
                        # print(f"Tipo: {int.from_bytes(tipo, 'big')} \n")
                        print(tipo)
                        # print(f"Tipo: {int.from_bytes(tipo, 'big')} \n")
                        #print(int.from_bytes(tipo, 'big') == tipo6)
                        
                        if rxBuffer != [-5]:
                            if int.from_bytes(tipo, 'big'):
                                print("Código de ERRO recebimento pacote.\n")
                                print(rxBuffer[6])
                                numPacoteReenvio =rxBuffer[6]
                                print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                                print("AQUIIII 0")
                                fatiamentoInicial = (numPacoteReenvio-1)*114 
                                print("AQUIIII 1")
                                fatiamentoFinal = (numPacoteReenvio)*114 
                                print("Corrige contador")
                                h4 = numPacoteReenvio
                                #CONT = numPacoteReenvio
                                h4 = h4.to_bytes(1,'big')
                                print("AQUIIII")
                                timer1 = time.time()
                                timer2 = time.time()
                                print("Corrige os timers")
                        else:
                            print("else: \n pass")
                elif (time.time() - timer2) <= 20:
                    rxBuffer, nRx = com1.getData(14)
                    print("fiz um getData")
                    tipo = rxBuffer[:1]
                    # print(f"Tipo: {int.from_bytes(tipo, 'big')} \n")
                    print(f"Tipo: {tipo} \n")
                    print(tipo == tipo6)
                    if tipo == tipo6:
                        print("Código de ERRO recebimento pacote.\n")
                        numPacoteReenvio =int.from_bytes(rxBuffer[6], 'big')
                        print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                        print("AQUIIII 00")
                        fatiamentoInicial = (numPacoteReenvio-1)*114
                        print("AQUIIII 11")
                        fatiamentoFinal = (numPacoteReenvio)*114 
                        print("Corrige contador")
                        #h4 = numPacoteReenvio-1
                        #CONT = numPacoteReenvio
                        #h4 = h4.to_bytes(1,'big')
                        print("AQUIIII 22")
                        timer1 = time.time()
                        timer2 = time.time()
                        print("Corrige os timers")
                else:
                    print("Timed out")
                    h0 = tipo5.to_bytes(1, 'big')
                    HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                    pacote = HEAD + EOP
                        # Transmite pacote
                    txBuffer=b''.join(pacote)
                    print(f"Tamanho do payload: {int.from_bytes(txBuffer[5], 'big')}")
                    print(f"Enviando pacote de timed out 'tipo6' ... ")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    time.sleep(0.01)
                    com1.disable()
                    break  


                            
                
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