from email import header
from enlace import *
import time
import numpy as np


serialName = "COM5"    

def main():
    try:
        HOUVE_ERRO = {}
        arquivo = []
        com1 = enlace('COM5') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Esperando handshake")
    
        time.sleep(.5)        
        rxBuffer, nRx = com1.getData(14)
        time.sleep(.01)
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
            pacote = rxBuffer
            print(pacote, len(pacote))
                # Transmite pacote
            txBuffer = pacote
            print(f"Envianado pacote de conferencia")
            com1.sendData(np.asarray(txBuffer)) #dados as np.array
            time.sleep(0.05)

            while numeroPacote <= totalPacotes:
                rxBuffer, nRx = com1.getData(14+114) #máximo permitido, head+payload+eop
                time.sleep(.01)
                header = rxBuffer[:10]
                payLoad = rxBuffer[10:124]
                eop = rxBuffer[124:]
                eop= int.from_bytes(eop, 'big')
                tipo = int.from_bytes(rxBuffer[0:2], 'big')
                numeroPacoteRecebido = int.from_bytes(header[2:4], 'big')
                totalPacotesRecebido = int.from_bytes(header[4:6], 'big')
                if numeroPacoteRecebido == (numeroPacote+1):
                    print("sequência ok")
                    if eop == 2022:
                        print("EOP no lugar correto.")
                        print("Avisando o client que está ok")
                        header = header[:]

                else:
                    print("Sequencia incorreta")
                
                pass
                
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
