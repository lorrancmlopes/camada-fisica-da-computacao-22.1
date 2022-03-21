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
        # informações padrozinadas
        tipo1, tipo2, tipo3, tipo4, tipo5, tipo6 = 1, 2, 3, 4, 5, 6 
        GET = True
        codigoReenvio = 3
        #  pacoteHandshake = [tipo, numeroPacote.to_bytes(2, "big"), totalPacotes, tamanhoPayload, origem, destino, EOP]
        origem, destino = 1, 1
        HOUVE_ERRO = {}
        arquivo = []
        ocioso = True
        totalPacotesRecebido = 0
        com1 = enlace('COM8') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Esperando handshake")
    
        time.sleep(.5)        
        
        while ocioso:
            rxBuffer, nRx = com1.getData(14) # pega handshake
            time.sleep(.01)

            if len(rxBuffer) != 0:
                # totalPacotesRecebido += 1
                print("Abrindo o pacote para ver se o tipo é 0 (handshake)")
                #if int.from_bytes(rxBuffer[0], 'big') == tipo1:
                if rxBuffer[0] == tipo1:
                    print("é do tipo 1")
                    # if int.from_bytes(rxBuffer[5], 'big') == 13:
                    if rxBuffer[5] == 13:
                        print("é para mim")
                        ocioso = False
                        time.sleep(1)
                    else:
                        time.sleep(1)

        print("Tipo handshake. Extraindo informações sobre a quantidade de pacotes.")
        # pacoteHandshake = [tipo, numeroPacote, totalPacotes, tamanhoPayload, origem, destino, EOP]
        #tipo = int.from_bytes(tipo2, 'big')
        # numeroPacote = int.from_bytes(rxBuffer[4], 'big')
        numeroPacote = rxBuffer[4]
        # totalPacotes = int.from_bytes(rxBuffer[3], 'big')
        totalPacotes = rxBuffer[3]
        print(f"Pacote atual: {numeroPacote}; Total: {totalPacotes}")
        h0 = tipo2.to_bytes(1, 'big')                            # tipo de mensagem
        h1, h2, h6, h7, h8, h9 = 1, 1, 0, 0, 0, 0                                           # livre
        h1, h2 = h1.to_bytes(1,'big'), h2.to_bytes(1, 'big')    # número total de pacotes no arquivos
        h3 = totalPacotes.to_bytes(1, 'big')                      # 
        h4 = 1
        h4 = h4.to_bytes(1, 'big')                            # número do pacote sendo enviado
        h5 = rxBuffer[5].to_bytes(1, 'big') # id do arquivo                        # tipo handshake = id do arquivo, tipo dados = tamanho payload
        h6 = h6.to_bytes(1, 'big')
        h7 = numeroPacote                            # pacote solicitado quando tem erro
        h7 = h7.to_bytes(1, 'big')                            # último pacote recebido com sucesso
        h8 = h8.to_bytes(1, 'big')                            # CRC
        h9 = h9.to_bytes(1, 'big') 
        HEAD = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
        EOP = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        pacote = HEAD + EOP
        txBuffer = b''.join(pacote)
        print(f"Enviando pacote de conferencia: {txBuffer}. Seu tamanho é {len(txBuffer)}")
        com1.sendData(np.asarray(txBuffer)) #dados as np.array
        time.sleep(0.05)            
        while GET:
            bytesGetData = 114
            print("-------------LOOP-----------")
            rxBufferHeader, nRx = com1.getData(10) #máximo permitido, head+payload+eop
            time.sleep(0.05)
            timer1 = time.time()
            timer2 = time.time()
            print(f"rxBuffer: {rxBuffer}")
            print(f"Tipo da msg recebida: tipo {rxBufferHeader[0]}")
            
            if rxBufferHeader[0] == tipo3:
                numeroPacote = rxBufferHeader[4]
                print("msg t3 recebida")
                print(f"Num. Pacote: {numeroPacote}, Total informado: {totalPacotes}")

                    #print(int.from_bytes(rxBufferHeader[2:4], 'big'))
                # if int.from_bytes(rxBufferHeader[2:4], 'big') == totalPacotes:
                if numeroPacote == totalPacotes:
                    print("ultimo pacote aqui")
                    # bytesGetData = int.from_bytes(rxBufferHeader[6:8],'big')
                    bytesGetData = rxBufferHeader[5]
                    print(f"Estamos pegando {bytesGetData} no GetData!")
                rxBufferPayLoad, nRx = com1.getData(bytesGetData) 
                time.sleep(0.5) #era 1 s
                eop, nRx = com1.getData(4)
                time.sleep(0.05)
                eop= int.from_bytes(eop, 'big')
                print(f"EOP: {eop}")
                #tipo = int.from_bytes(rxBuffer[0], 'big')
                # numeroPacoteRecebido = int.from_bytes(rxBufferHeader[4], 'big')
                numeroPacoteRecebido = rxBufferHeader[4]
                # totalPacotesRecebido = int.from_bytes(rxBufferHeader[3], 'big')
                print(f"Número pacote recebido: {numeroPacoteRecebido}. Numero pacote esperado: {(totalPacotesRecebido+1)}")
                
                
                # nominalSize = int.from_bytes(rxBufferHeader[5], 'big')
                nominalSize = rxBufferHeader[5]
                realSize = len(rxBufferPayLoad)

                if nominalSize != realSize:
                    print("ERRO: Tamanho informado não confere. Solicitando reenvio:")
                    #trabalhar aqui____________________________________
                    tamanhoPayload = 0
                    pacote = [codigoReenvio.to_bytes(2,'big'), numeroPacote.to_bytes(2,'big'), totalPacotes.to_bytes(2,'big'),tamanhoPayload.to_bytes(2,'big'), origem.to_bytes(1,'big'), destino.to_bytes(1,'big'), eop.to_bytes(4, 'big')]
                    txBuffer=b''.join(pacote)
                    print(f"Pacote dizendo 'Pedido Reenvio': {txBuffer}. Tamanho em bytes: {len(txBuffer)}")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    time.sleep(0.01)
                    
                    
                    if numeroPacoteRecebido == totalPacotes:
                        print("\n\n------------FINALIZANDO---------------")
                        GET = False
                else:
                    print("Payload correto")
                    


                if numeroPacoteRecebido == (totalPacotesRecebido+1):
                    print("pckg ok")
                    if eop == 2864434397:
                        print("EOP no lugar correto.")
                        print("Avisando o client que está ok")
                        bytesImagem.append(rxBufferPayLoad)
                        totalPacotesRecebido += 1

                        tamanhoPayload = 0
                        HEAD = [tipo4.to_bytes(1,'big'), h1, h2, totalPacotesRecebido.to_bytes(1, 'big'), numeroPacote.to_bytes(1,'big'), tamanhoPayload.to_bytes(1,'big'),h6,h7,h8,h9]
                        pacote = HEAD + EOP
                        txBuffer=b''.join(pacote)
                        #print(f"Pacote dizendo 'Recebimento OK': {txBuffer}. Tamanho em bytes: {len(txBuffer)}")
                        com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        time.sleep(0.01)
                        if numeroPacoteRecebido == totalPacotes:
                            print("\n\n------------FINALIZANDO---------------")
                            GET = False

                else:
                    print("Sequencia incorreta")
                    #trabalhar aqui____________________________________
                    tamanhoPayload = 0
                    esperado = totalPacotesRecebido + 1
                    h6 = esperado.to_bytes(1, 'big')
                    HEAD = [tipo6.to_bytes(1,'big'), h1, h2, totalPacotesRecebido.to_bytes(1, 'big'), numeroPacote.to_bytes(1,'big'), tamanhoPayload.to_bytes(1,'big'),h6,h7,h8,h9]
                    pacote = HEAD + EOP
                    txBuffer=b''.join(pacote)
                    print(f"Pedindo reenvio. Esperado era {esperado} Tamanho em bytes: {len(txBuffer)}")
                    com1.sendData(np.asarray(txBuffer)) #dados as np.array
                    time.sleep(0.01)
                    # totalPacotes += 1
                    # totalPacotesRecebido += 1
                    
                    if numeroPacoteRecebido == totalPacotes:
                        print("\n\n------------FINALIZANDO---------------")
                        GET = False
            else: 
                print("sleep 1s")
                time.sleep(1)
                #com1.rx.clearBuffer()
                #totalPacotesRecebido -= 1 # mudei 21/03
                if time.time()-timer2 > 20 and com1.rx.getBufferLen!=144:
                    ocioso = True
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
                    if time.time()-timer1 >2:
                        tamanhoPayload = 0
                        HEAD = [tipo4.to_bytes(1,'big'), h1, h2, totalPacotesRecebido.to_bytes(1, 'big'), numeroPacote.to_bytes(1,'big'), tamanhoPayload.to_bytes(1,'big'),h6,h7,h8,h9]
                        pacote = HEAD + EOP
                        txBuffer=b''.join(pacote)
                        #print(f"Pacote dizendo 'Recebimento OK': {txBuffer}. Tamanho em bytes: {len(txBuffer)}")
                        com1.sendData(np.asarray(txBuffer)) #dados as np.array
                        time.sleep(0.01)
                        timer1 = time.time()
            com1.rx.clearBuffer()             
                

        
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
