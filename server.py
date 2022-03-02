from enlace import *
import time
import numpy as np


serialName = "COM6"    

def main():
    try:
        com1 = enlace('COM6') #inicializa enlace
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
        print("pegou 1 byte")
        com1.rx.clearBuffer()
        print("limpando o buffer")
        time.sleep(.1)
        print("sleep")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Sucesso na comunicação")

   


        #acesso aos bytes recebidos
        # int.from_bytes(rxBuffer, 'big')
        rxBuffer, nRx = com1.getData(2) #pega os dois 1°s bytes que contem o tamanho total
        time.sleep(0.5)
        print("segundo sleep")
        print("recebeu o valor: {} (tamanho total em bytes)".format(int.from_bytes(rxBuffer, 'big')) )# log
        tamanhoComanados = int.from_bytes(rxBuffer, 'big')
        time.sleep(0.5)
        print("sleep")
        rxBuffer, nRx = com1.getData(tamanhoComanados) #pega o restante (os comandos)
        print("Recebeu a mensagem. É ela: \n\n\n {}\n\n\n".format(rxBuffer))

        #decodificação da mensagem:
        stringzona = str(rxBuffer)
        dividida = stringzona.split("\\")
        dividida = dividida[2:]
        comandos = []
        i = 0
        for byte in dividida:
            if byte[2] == '1' or byte[2] == '2' or byte[2] == '4':
                comando = dividida[i+1:i+int(byte[2])+1]
                comandos.append("".join(comando))
            i+= 1
        size = len(comandos)
        comandos[size-1] = comandos[size-1][:len(comandos[size-1])-1]
        print("Decodificou os comandos ({0}). São eles: \n\n\n {1}".format(size,comandos))

        #conferencia de bytes:
        #forçar erro de conferencia de bytes
        #size = 9
        mensagem = [size.to_bytes(1, 'big')]
        txBuffer = mensagem 
        print("Transmitindo a quantidade de comandos recebida .... ")
        
        #forçar timeout
        #time.sleep(11)
        com1.sendData(np.asarray(txBuffer)) #dados as np.array
      
          


    
          
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
