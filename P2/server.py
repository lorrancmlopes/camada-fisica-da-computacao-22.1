from email import header

from sklearn.metrics import top_k_accuracy_score
from enlace import *
import time
import numpy as np


serialName = "COM8"    

def main():
    try:

         #endereço da imagem a ser salva
        imageW = "./img/recebidaCopia.jpg"
        bytesImagem = []

        codigoOk = 2
        GET = True
        codigoReenvio = 3
        #  pacoteHandshake = [tipo, numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload, origem, destino, EOP]
        origem, destino = 1, 1
        HOUVE_ERRO = {}
        arquivo = []
        totalPacotesRecebido = 0
        com1 = enlace('COM8') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Esperando handshake")
    
        time.sleep(.5)        
        rxBuffer, nRx = com1.getData(14)
        
        time.sleep(.01)
        if len(rxBuffer) != 0:
            totalPacotesRecebido += 1
        print("Abrindo o pacote para ver se o tipo é 0 (handshake)")
        print(int.from_bytes(rxBuffer[:2], 'big'))
        if int.from_bytes(rxBuffer[:2], 'big') != 0:
            print("Tipo diferente. Comunicação errada")
        elif int.from_bytes(rxBuffer[:2], 'big') == 0:
            print("Tipo handshake. Extraindo informações sobre a quantidade de pacotes.")
            # pacoteHandshake = [tipo, numeroPacote, totalPacotes, tamanhoPayload, origem, destino, EOP]
            tipo = int.from_bytes(rxBuffer[0:2], 'big')
            numeroPacote = int.from_bytes(rxBuffer[2:4], 'big')
            totalPacotes = int.from_bytes(rxBuffer[4:6], 'big')
            print(f"Pacote atual: {numeroPacote}; Total: {totalPacotes}")
            pacote = rxBuffer
            # print(pacote, len(pacote))
                # Transmite pacote
            txBuffer = pacote
            print(f"Enviando pacote de conferencia")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            time.sleep(0.05)            
            while GET:
                bytesGetData = 114
                print("-------------LOOP-----------")
                rxBufferHeader, nRx = com1.getData(10) #máximo permitido, head+payload+eop
                time.sleep(0.05)
                if rxBufferHeader != [-5]:
                    numeroPacote += 1
                    print(f"Num. Pacote: {numeroPacote}, Total informado: {totalPacotes}")
                    #print(int.from_bytes(rxBufferHeader[2:4], 'big'))
                if int.from_bytes(rxBufferHeader[2:4], 'big') == totalPacotes:
                    #print("ultimo pacote aqui")
                    bytesGetData = int.from_bytes(rxBufferHeader[6:8],'big')
                    #print(f"Estamos pegando {bytesGetData} no GetData!")
                rxBufferPayLoad, nRx = com1.getData(bytesGetData) #máximo permitido, head+payload+eop
                time.sleep(1)
                eop, nRx = com1.getData(4)
                time.sleep(0.05)
                # print(f"header {rxBufferHeader}, payload {rxBufferPayLoad}, eop {eop}")
                eop= int.from_bytes(eop, 'big')
                tipo = int.from_bytes(rxBuffer[0:2], 'big')
                numeroPacoteRecebido = int.from_bytes(rxBufferHeader[2:4], 'big')
                # totalPacotesRecebido = int.from_bytes(rxBufferHeader[4:6], 'big')
                print(f"Número pacote recebido: {numeroPacoteRecebido}. Numero pacote esperado: {(totalPacotesRecebido+1)}")
                
                
                '''Faça uma simulação onde o tamanho real do payload de um pacote não corresponde ao informado no 
                head. Mostre a resposta do servidor. '''
                nominalSize = int.from_bytes(rxBufferHeader[6:8], 'big')
                realSize = len(rxBufferPayLoad)
                if numeroPacoteRecebido == 3:
                    realSize = -2

                if nominalSize != realSize:
                    print("ERRO: Tamanho informado não confere. Solicitando reenvio:")
                    #trabalhar aqui____________________________________
                    tamanhoPayload = 0
                    pacote = [codigoReenvio.to_bytes(2,'big'), numeroPacote.to_bytes(2,'big'), totalPacotes.to_bytes(2,'big'),tamanhoPayload.to_bytes(2,'big'), origem.to_bytes(1,'big'), destino.to_bytes(1,'big'), eop.to_bytes(4, 'big')]
                    txBuffer=b''.join(pacote)
                    print(f"Pacote dizendo 'Pedido Reenvio': {txBuffer}. Tamanho em bytes: {len(txBuffer)}")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    time.sleep(0.01)
                    totalPacotes += 1
                    #totalPacotesRecebido += 1
                    
                    
                    if int.from_bytes(rxBufferHeader[2:4], 'big') == totalPacotes:
                        print("\n\n------------FINALIZANDO---------------")
                        GET = False
                    

                
                ''''Uma simulação onde o client erre o número do pacote. Mostre a resposta do servidor perante o envio 
                    fora de ordem. '''
                # Ex.: pacote 3 não passar na consição de ser um a mais que o anterior: 
                # para isso, inserimos 'and numeroPacoteRecebido != 3' na conferência de ordem:

                if numeroPacoteRecebido == (totalPacotesRecebido+1):
                    print("sequência ok")
                    if eop == 2022:
                        print("EOP no lugar correto.")
                        print("Avisando o client que está ok")
                        bytesImagem.append(rxBufferPayLoad)
                        totalPacotesRecebido += 1
                        #trabalhar aqui____________________________________
                        tamanhoPayload = 0
                        pacote = [codigoOk.to_bytes(2,'big'), numeroPacote.to_bytes(2,'big'), totalPacotes.to_bytes(2,'big'),tamanhoPayload.to_bytes(2,'big'), origem.to_bytes(1,'big'), destino.to_bytes(1,'big'), eop.to_bytes(4, 'big')]
                        txBuffer=b''.join(pacote)
                        #print(f"Pacote dizendo 'Recebimento OK': {txBuffer}. Tamanho em bytes: {len(txBuffer)}")
                        com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        time.sleep(0.01)
                        if int.from_bytes(rxBufferHeader[2:4], 'big') == totalPacotes:
                            print("\n\n------------FINALIZANDO---------------")
                            GET = False

                else:
                    print("Sequencia incorreta")
                    #trabalhar aqui____________________________________
                    tamanhoPayload = 0
                    pacote = [codigoReenvio.to_bytes(2,'big'), numeroPacote.to_bytes(2,'big'), totalPacotes.to_bytes(2,'big'),tamanhoPayload.to_bytes(2,'big'), origem.to_bytes(1,'big'), destino.to_bytes(1,'big'), eop.to_bytes(4, 'big')]
                    txBuffer=b''.join(pacote)
                    print(f"Pedindo reenvio. Tamanho em bytes: {len(txBuffer)}")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    time.sleep(0.01)
                    totalPacotes += 1
                    totalPacotesRecebido += 1
                    
                    if int.from_bytes(rxBufferHeader[2:4], 'big') == totalPacotes:
                        print("\n\n------------FINALIZANDO---------------")
                        GET = False

        
        bytesImagem =b''.join(bytesImagem)
        f = open(imageW, 'wb')
        f.write(bytesImagem)
        #Fecha arquivo de imagem
        f.close()
        print("\n\n SUCESSO NA TRANSMISSÃO!")
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
