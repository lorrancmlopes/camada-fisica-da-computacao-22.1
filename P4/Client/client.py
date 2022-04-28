from enlace import *
from math import ceil
import time
from datetime import date, datetime
import numpy as np
import random
import sys # para pegar o tamanho em bytes
from crccheck.crc import Crc16, CrcXmodem
from crccheck.checksum import ChecksumXor16



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
        log = "./log/Client5.txt" 
        logString = ""
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
        h4 = 0
        
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

        pacoteHandshake=b''.join(pacoteHandshake)
        txBuffer = pacoteHandshake

        
        CONT = None
        arquivoSeraEnviado = True
        inicio = time.time() 
        while HANDSHAKE:
            # Transmite dados
            print("Solicitando conexão com o server .... ")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            logString  += f"{date.today()} {datetime.now().time()}/envio/{tipo1}/{len(txBuffer)}\n"
            time.sleep(5)
            print("esperando resposta") 
            timer20 = time.time()
              
            rxBuffer, nRx = com1.getData(14, timer20)
            #print(f"rxbuffer: {rxBuffer}")
            try:
                if int((str(rxBuffer).split("\\"))[1][1:]) == tipo2: #se o 1° byte tem o valor tipo 2, indica q é handshake bem feito
                    logString  += f"{date.today()} {datetime.now().time()}/receb/{tipo2}/{len(rxBuffer)}\n"
                    print("Comunicação bem sucedida! (HANDSHAKE)")
                    HANDSHAKE = False
                    ATUALIZATIMER20 = True
                    CONT = 1
                    com1.rx.clearBuffer()
            except:
                pass
            if time.time() - inicio > 20:
                print("\n------------------------------")
                print("\n--------TIMEOUT HANDSHAKE-----")
                print("\n------------------------------")
                arquivoSeraEnviado = False
                break
                
        if not FIM:
            ERRO_ORDEM = False
            ERRO_CRC = False
            fatiamentoInicial = 0
            fatiamentoFinal = 114
            h0 = tipo3

            if arquivoSeraEnviado:
                print("---------------------")
                print("Início do envio do arquivo: \n")
                h4 = 1
                h4 = h4.to_bytes(1, 'big')
            else:
                #Variáveis erro para pular o while (handshake > 20 s sem resposta)
                h4 = int.from_bytes(h3, 'big')
                h4 += 1
                h4 = h4.to_bytes(1,'big')
            
            while int.from_bytes(h4, 'big') <= int.from_bytes(h3, 'big'):
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
                    #print(f"len data: {len(data)}, fatiamento: {fatiamentoInicial}/ {fatiamentoFinal} ")
                # fatiamentoInicial += 114
                # fatiamentoFinal += 114
                h0 = tipo3.to_bytes(1, 'big')
                #h4 = h4.to_bytes(1, 'big')
                HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                print(f"HEAD: {HEAD}")
                print("testandooo")
                print(f"Calc do CRC16: {Crc16.calc(PAYLOAD)}")
                crc = Crc16.calc(PAYLOAD)
                print(f"CRC: {crc}")
                print(f"CRC16 em bytes: {crc.to_bytes(2,'big')}")
                HEAD = HEAD[:8] + [crc.to_bytes(2,'big')]
                print(HEAD)
                
                # Situação 2
                if ERRO_ORDEM and int.from_bytes(h4, 'big') == 7:
                    h4Erro = 2
                    h4Erro = h4Erro.to_bytes(1, 'big')
                    ERRO_ORDEM = False
                    print("--------------------------------")
                    print("Forçando erro na ordem dos pckgs")
                    print("--------------------------------")
                    HEAD = [h0, h1, h2, h3, h4Erro, h5, h6, h7, h8, h9]

                #forçar erro crc
                if ERRO_CRC and int.from_bytes(h4, 'big') == 8:
                    crc = 2022
                    ERRO_CRC = False
                    print("--------------------------------")
                    print("Forçando erro no CRC")
                    print("--------------------------------")
                    HEAD[8:] = [crc.to_bytes(2, 'big')]

                
                PAYLOAD = [PAYLOAD]
                pacote = HEAD + PAYLOAD + EOP
                txBuffer = b''.join(pacote)
                print("\n ##################################")
                #print(f'tamanho pacote len(txbuffer): {len(txBuffer)}')
                print(f"Tipo da msg a ser enviada: tipo{txBuffer[0]}")
                
                print(f"CRC {crc}\n")
                com1.sendData(np.asarray(txBuffer)) #dados as np.array
                logString  += f"{date.today()} {datetime.now().time()}/envio/{tipo3}/{len(txBuffer)}/{int.from_bytes(h4, 'big')}/{int.from_bytes(h3, 'big')}/CRC {crc}\n"
                print("envia msg cont - msg t3")
                print(f"logString: {logString}")
                #timer2 = time.time() #set timer 2 (COLOCAR DENTRO DO enlaceTX)
                #Conferência de dados para envio do próximo pacote:
                print("Conferindo..")
                if ATUALIZATIMER20:
                    timer20 = time.time()
                rxBuffer, nRx = com1.getData(14, timer20)
                #print("fez o getData")
                
                if rxBuffer != [-5] and rxBuffer != [-7]:
                    tipo = rxBuffer[0]
                    print(f"Tipo: {tipo}")
    
                    if tipo == tipo4:
                        #print(f"Rxbuffer[4]: {rxBuffer[4]}. H4: {h4}")
                        logString  += f"{date.today()} {datetime.now().time()}/receb/{tipo4}/{len(rxBuffer)}/CRC\n"
                        print("Código de recebimento ok")
                        CONT += 1
                        h4 = int.from_bytes(h4, 'big')
                        h4  += 1
                        h4 = h4.to_bytes(1, 'big')
                        fatiamentoInicial += 114
                        fatiamentoFinal += 114

                    elif tipo == tipo6:
                        logString  += f"{date.today()} {datetime.now().time()}/receb/{tipo6}/{len(rxBuffer)}/CRC\n"
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("------Código de ERRO recebimento pacote----.\n")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print(rxBuffer[6])
                        numPacoteReenvio =rxBuffer[6]
                        print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                        fatiamentoInicial = (numPacoteReenvio-1)*114 
                        fatiamentoFinal = (numPacoteReenvio)*114 
                        print("Corrige contador")
                        h4 = numPacoteReenvio
                        print(f"h4 agora é: {h4}")
                        #CONT = numPacoteReenvio
                        h4 = h4.to_bytes(1,'big')
                        ATUALIZATIMER20 = True
                        print("Corrige timer")

                elif rxBuffer == [-5]: # se o return for [-5], t > 5s
                    logString  += f"{date.today()} {datetime.now().time()}/envio/{tipo3}/{len(txBuffer)}/{int.from_bytes(h4, 'big')}/{int.from_bytes(h3, 'big')}/CRC\n"
                    print("envia msg cont - msg t3")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    ATUALIZATIMER20 = False
                    rxBuffer = com1.getData(14, timer20) #getData == restart timer1

                    if rxBuffer == [-7]: # significa que t > 20s
                        print("Timed out")
                        h0 = tipo5.to_bytes(1, 'big')
                        HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                        pacote = HEAD + EOP
                         # Transmite pacote
                        txBuffer=b''.join(pacote)
                        print(f"Tamanho do payload: {int.from_bytes(txBuffer[5], 'big')}")
                        print(f"Enviando pacote de timed out 'tipo5' ... ")
                        com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        logString  += f"{date.today()} {datetime.now().time()}/envio/{tipo5}/{len(txBuffer)}/{int.from_bytes(h4, 'big')}/{int.from_bytes(h3, 'big')}/CRC\n"
                        com1.disable()
                        h4 = int.from_bytes(h4, 'big')
                        h4 = int.from_bytes(h3, 'big') + 1
                        break
                    else:
                        print("verifica se recebeu msg t6")
                        rxBuffer, nRx = com1.getData(14, timer20)
                        
                        print("fiz um getData")
                        tipo = rxBuffer[:1]
                        # print(f"Tipo: {int.from_bytes(tipo, 'big')} \n")
                        # print(f"Tipo: {int.from_bytes(tipo, 'big')} \n")
                        #print(int.from_bytes(tipo, 'big') == tipo6)
                        
                        if rxBuffer[0] == tipo6:
                            logString  += f"{date.today()} {datetime.now().time()}/receb/{tipo6}/{len(rxBuffer)}/CRC\n"
                            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            print("------Código de ERRO recebimento pacote----.\n")
                            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            print(rxBuffer[6])
                            numPacoteReenvio =rxBuffer[6]
                            print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                            print("AQUIIII 0")
                            fatiamentoInicial = (numPacoteReenvio-1)*114 
                            print("AQUIIII 1")
                            fatiamentoFinal = (numPacoteReenvio)*114 
                            print("Corrige contador")
                            h4 = numPacoteReenvio
                            print(f"h4 agora é: {h4}")
                            #CONT = numPacoteReenvio
                            h4 = h4.to_bytes(1,'big')
                            print("AQUIIII")
                            ATUALIZATIMER20 = True
                            # timer20 = time.time()
                            print("Corrige timer")

                elif rxBuffer[0] == tipo6:
                    logString  += f"{date.today()} {datetime.now().time()}/receb/{tipo6}/{len(rxBuffer)}/CRC\n"
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("------Código de ERRO recebimento pacote----.\n")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print(rxBuffer[6])
                    numPacoteReenvio =rxBuffer[6]
                    print(f"Enviar arquivo a partir do pacote n° {numPacoteReenvio}.")
                    print("AQUIIII 0")
                    fatiamentoInicial = (numPacoteReenvio-1)*114 
                    print("AQUIIII 1")
                    fatiamentoFinal = (numPacoteReenvio)*114 
                    print("Corrige contador")
                    h4 = numPacoteReenvio
                    print(f"h4 agora é: {h4}")
                    #CONT = numPacoteReenvio
                    h4 = h4.to_bytes(1,'big')
                    print("AQUIIII")
                    # timer20 = time.time()
                    ATUALIZATIMER20 = True
                    print("Corrige timer")

                elif rxBuffer == [-7]: # significa que t > 20s
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("--------------Timed out-----------------------")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    
                    h0 = tipo5.to_bytes(1, 'big')
                    HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                    pacote = HEAD + EOP
                        # Transmite pacote
                    txBuffer=b''.join(pacote)
                    print(f"Tamanho do payload: {txBuffer[5]}")
                    print(f"Enviando pacote de timed out 'tipo5' ... ")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    logString  += f"{date.today()} {datetime.now().time()}/envio/{tipo5}/{len(txBuffer)}/{int.from_bytes(h4, 'big')}/{int.from_bytes(h3, 'big')}/CRC\n"
                    com1.disable()
                    break
            
            f = open(log, 'w')
            f.write(logString)
            #Fecha arquivo de texto
            f.close()

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