
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas


#funcao para transformas intensidade acustica em dB
from suaBibSignal import signalMeu
import time
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import peakutils

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
    0:[1339,941],
    "X":[1206,941],
    "#":[1477,941],
    "A":[1633,697],
    "B":[1633,770],
    "C":[1633,852],
    "D":[1633,941],

}


def todB(s):
    sdB = 10*np.log10(s)

    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    sinalMeu = signalMeu() 
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate =  44100 
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print(f"A captura de som começará em {duration} segundos!")
    time.sleep(duration)
   
    #faca um print informando que a gravacao foi inicializada
    print("Começou!")
    
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs*duration*2
    freqDeAmostragem = fs
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    print(f"Audio: {audio}")
    
    #grave uma variavel com apenas a parte que interessa (dados)
    y = audio[:,0]
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    T = 1/freqDeAmostragem
    t = np.linspace(0,duration,numAmostras) 

    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = sinalMeu.calcFFT(y, fs)

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    # index = peakutils.peak.indexes(yf, thres=0.3, min_dist=1) FUNCIONAVA PARA NUMEROS
    index = peakutils.peak.indexes(yf, thres=0.3, min_dist=15)
    
    print(index, len(index))
    frequenciasPico = []
    print('As frequências de pico encontradas foram:')
    for i in index:
        if (xf[i]) > 600:
             #printe os picos encontrados! 
            print(xf[i])
            frequenciasPico.append(xf[i])
    print('----------------------------------')

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.

    minima = min(frequenciasPico)
    maxima = max(frequenciasPico)
    diferencas = {}
    for num, listaFreq in frequenciaPorNumero.items():
        diferencaMin = abs(minima-listaFreq[1])
        diferencaMax = abs(maxima-listaFreq[0])
        diferencas[num] = (diferencaMax+diferencaMin)/2

    print(f"O número digitado foi: {min(diferencas, key=diferencas.get)}")
    
    # Construa o gráfico do sinal emitido
    # Exibe gráficos
    figure, axis = plt.subplots(2)
    axis[0].plot(t,y)
    axis[0].title.set_text('Audio Recebido no tempo')
    axis[0].set_ylim(-0.1, 0.1)
    axis[0].set_xlim(0.5, 0.505)

    axis[1].plot(xf,yf)
    axis[1].set_xlim(0,1600)
    axis[1].grid()
    axis[1].title.set_text('Fourier Audio Recebido')
    plt.show()

if __name__ == "__main__":
    main()
