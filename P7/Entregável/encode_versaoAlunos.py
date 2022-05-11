
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt




frequenciaPorNumero = {
    1:[1206, 697],
    2:[1339,697],
    3:[1477,697],
    4:[1206,770],
    5:[1339,770],
    6:[1477,770],
    7:[1206,852],
    8:[1339,852],
    9:[1477,852],
    0:[1339,941]
}

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides 
    # com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. 
    # Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista 
    # de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). 
    # Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas,
    #  voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    numero = int(input("Qual n° entre 0 e 9 você deseja? \n"))
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, 
    # duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    print("Gerando Tons base")
    meuSinal = signalMeu()
    Amplitude = 4
    T = 5 #segundos
    fs = 44100
    t   = np.linspace(-T/2,T/2,T*fs)
        # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, 
    x1, s1 = meuSinal.generateSin(frequenciaPorNumero[numero][0], Amplitude, 5, fs)
    x2, s2 = meuSinal.generateSin(frequenciaPorNumero[numero][1], Amplitude, 5, fs)
    # some as senoides. A soma será o sinal a ser emitido.
    som = s1 + s2
        # entao voce tera que gerar uma lista de tempo correspondente a isso
    

    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.

    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(numero))
    sd.play(som, fs)
    # construa o gráfico do sinal emitido
    plt.plot(t, som, '.-')
    plt.xlim(0, 0.005)
    plt.ylabel("?")
    plt.xlabel("t")
    # e o gráfico da transformada de Fourier
    X, Y = meuSinal.calcFFT(som[:30],fs)
    plt.figure()
    plt.stem(X,np.abs(Y))
    #plt.xlim(-1.6e3, 1.6e3)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas,
    #  voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    meuSinal.plotFFT(som, fs)
    

if __name__ == "__main__":
    main()
