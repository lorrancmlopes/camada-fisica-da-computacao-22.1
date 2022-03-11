from email import header
from enlace import *
import time
import numpy as np


serialName = "COM6"    

def main():
    try:
        codigoOk = 2
        codigoReenvio = 3
        #  pacoteHandshake = [tipo, numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload, origem, destino, EOP]
        origem, destino = 1, 1
        HOUVE_ERRO = {}
        arquivo = []
        totalPacotesRecebido = 0
        com1 = enlace('COM6') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Esperando handshake")
    
        time.sleep(.5)        
        rxBuffer, nRx = com1.getData(14)
        
        time.sleep(.01)
        if len(rxBuffer) != 0:
            totalPacotesRecebido += 1
        print(f"Rxbuffer: {rxBuffer}")
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
            time.sleep(1)            
            while numeroPacote <= totalPacotes:
                rxBufferHeader, nRx = com1.getData(10) #máximo permitido, head+payload+eop
                time.sleep(0.05)
                rxBufferPayLoad, nRx = com1.getData(114) #máximo permitido, head+payload+eop
                time.sleep(0.05)
                eop, nRx = com1.getData(4)
                time.sleep(0.05)
                print(f"header {rxBufferHeader}, payload {rxBufferPayLoad}, eop {eop}")
                print(f"Tamanho payload: {int.from_bytes(rxBufferHeader[6:8], 'big')}")
                # print(rxBuffer)
                # header = rxBuffer[:10]
                # payLoad = rxBuffer[10:124]
                eop= int.from_bytes(eop, 'big')

                tipo = int.from_bytes(rxBuffer[0:2], 'big')
                numeroPacoteRecebido = int.from_bytes(rxBufferHeader[2:4], 'big')
                # totalPacotesRecebido = int.from_bytes(rxBufferHeader[4:6], 'big')
                print(f"Número pacote recebido: {numeroPacoteRecebido} (ou em bytes {rxBufferHeader[2:4]}). Numero pacote esperado: {(numeroPacote+1)}")
                if numeroPacoteRecebido == (totalPacotesRecebido+1):
                    print("sequência ok")
                    if eop == 2022:
                        print("EOP no lugar correto.")
                        print("Avisando o client que está ok")
                        totalPacotesRecebido += 1
                        #trabalhar aqui____________________________________
                        # tamanhoPayload = 0
                        # pacote = [codigoOk.to_bytes(2,'big'), numeroPacote.to_bytes(2,'big'), totalPacotes.to_bytes(2,'big'),tamanhoPayload.to_bytes(2,'big'), origem.to_bytes(1,'big'), destino.to_bytes(1,'big'), eop.to_bytes(4, 'big')]
                        # txBuffer=b''.join(pacote)
                        # com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        # time.sleep(1)

                else:
                    print("Sequencia incorreta")
                
                
        print("Olhe o client.py")
        time.sleep(10)
        

      
          


    
          
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
