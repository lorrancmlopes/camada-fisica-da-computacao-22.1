from scipy import rand
from sympy import N
from enlace import *
import time
import numpy as np
import random
import sys # para pegar o tamanho em bytes

serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        com1 = enlace('COM3') #inicializa enlace
        
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        print("Enviou o 1°")
        time.sleep(1) 
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Sucesso na comunicação")
         
        quantidadeComandos = random.randint(10,30) #.rand.randint(10,30)
        print(f"A quantidade sorteada é: {quantidadeComandos}.")  # (numero).to_bytes(1,byteorder='big')
        comandos = [b'\x00\xff\x00\xff', b'\x00\xff\xff\x00',b'\xff',b'\x00',b'\xff\x00', b'\x00\xff']
        comandosSorteados = random.choices(comandos, k=quantidadeComandos)
        bytesPorComando = []
        mensagem = [quantidadeComandos.to_bytes(1, 'big')]
        for comando in comandosSorteados:
            mensagem.append(len((comando)).to_bytes(1, 'big')) #len retorna se é 1, 2 ou 4 bytes. Salvamos na lista
            mensagem.append(comando) # salvamos o comando na lista
            
            bytesPorComando.append(len((comando)))

        numeroDeBytes = sum(bytesPorComando) #Guardamos o total nº de bytes que existem na sequência
        tamanhoTotal = 1 + sum(bytesPorComando) + (quantidadeComandos*1)
        tamanhoTotal = [tamanhoTotal.to_bytes(2, 'big')]
        mensagem = tamanhoTotal + mensagem 
        mensagem=b''.join(mensagem) 
        ''' mensagem = {Tamanho total (2 bytes) 
                        + quantidade comandos (1 byte) 
                        + [bytes do comando (1 byte) 
                        + comando (4 bytes)]*quantidade comandos vezes } 
        '''
        print(f"Tamanho total: {tamanhoTotal} \n")
        print(f"A mensagem a ser enviada é: \n {mensagem}")

        

        txBuffer = mensagem #big string
        
        
        # Transmite dados
        print("Transmitindo .... ")
        com1.sendData(np.asarray(txBuffer)) #dados as np.array
        time.sleep(0.5)
        txSize = com1.tx.getStatus()

       
        print(f"txSize {txSize}")
        time.sleep(0.1)
        print("esperando 1 byte de conferencia")        
        rxBuffer, nRx = com1.getData(1)
        if rxBuffer == [-5]:
            print(rxBuffer)
            print("Time out. Encerrando comunicação")
            com1.disable()
            print("Comunicação encerrada")
        else:
            print("pegou 1 byte")
            print("Seu valor é: {}.".format(int.from_bytes(rxBuffer, 'big')))
            if int.from_bytes(rxBuffer, 'big') == quantidadeComandos:
                print("Comunicação realizada com sucesso")
            else:
                print("Erro na conferência de comandos.")
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