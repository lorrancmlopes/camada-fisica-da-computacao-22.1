#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5') #inicializa enlace
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Sucesso na comunicação")
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        



        #endereço da imagem a ser transmitida
        imageR = "./img/smallImage2.jpg"
        #endereço da imagem a ser salva
        imageW = "./img/recebidaCopia.jpg"
        print("Carregando imagem para transmissão: ")
        print("-{}".format(imageR))
        print("-----------------")
        txBuffer = open(imageR, 'rb').read() #imagem em bytes!
        txLen    = len(txBuffer)
        print(txLen)

        # Transmite imagem
        print("Transmitindo .... {} bytes".format(txLen))
        start = time.time()
        com1.sendData(np.asarray(txBuffer))
        end = time.time()
        print("tempo de transmissão: {} ".format(end-start))
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
      
  
        # txBuffer = #dados
        # espera o fim da transmissão
        # para pegar o tempo: usar o time, fazer final - start. 
       

        # Atualiza dados da transmissão
        txSize = com1.tx.getStatus()

       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        print(f"txSize {txSize}")
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        print(f"TxtxLen {txLen}")
        startReceb = time.time()
        rxBuffer, nRx = com1.getData(txLen)
        endReceb = time.time()
        #print(f"tempo de recebimento: {endReceb-startReceb}")
        print("recebeu {}" .format(rxBuffer))# log
        print ("Lido              {} bytes ".format(nRx))

        
        # Salva imagem recebida em arquivo
        print("-------------------------")
        print("Salvando dados no arquivo: ")
        print("-{}".format(imageW))
        f = open(imageW, 'wb')
        f.write(rxBuffer)
        #Fecha arquivo de imagem
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
