
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas


#funcao para transformas intensidade acustica em dB
from suaBibSignal import signalMeu
import time
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import peakutils


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
    duration = 4  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


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
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    T = 1/freqDeAmostragem
    t = np.linspace(-T/2,T/2,numAmostras) # t   = np.linspace(-T/2,T/2,T*fs)

    # plot do gravico  áudio vs tempo!
   
    y = audio[:,0]
    print(audio.shape)
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = sinalMeu.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.xlim(0,1600)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.peak.indexes(yf, thres=0.8, min_dist=1)
    
    #printe os picos encontrados! 
    print(index, len(index))
    for i in index:
        print(xf[i])

    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
