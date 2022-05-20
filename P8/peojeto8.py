from turtle import shape
from suaBibSignal import signalMeu
import time
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import peakutils
from funcoes_LPF import filtro



    # function to normalize array
def normalize(item):
    print("normalizando...")
    return (item)/(np.max(np.abs(item)))


def main():
    # 1. Faça a leitura de um arquivo de áudio .wav de poucos segundos (entre 2 e 5) 
    #    previamente gravado com uma taxa de amostragem de 44100 Hz.



        #declare um objeto da classe da sua biblioteca de apoio (cedida)
    meuSinal = signalMeu() 
        #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
        #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
        # os seguintes parametros devem ser setados:
    
    sd.default.samplerate =  44100 
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
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
     # 2. Filtre e elimine as frequências acima de 2500 Hz.
    cutOff = 2500 #2500 Hz
    audioFiltrado = filtro(y, sd.default.samplerate, cutOff)
    #3. Reproduza o sinal e verifique que continua audível (com menos qualidade).
    sd.play(audioFiltrado, fs)

        
   
    
    #4. Module esse sinal de áudio em AM com portadora de 13.000 Hz. 
    #   (Essa portadora deve ser uma senoide começando em zero)
    t = np.linspace(0,duration,numAmostras) 
    xf, yf = meuSinal.calcFFT(y, fs) ## Calcula o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias


    print("Gerando senoide portadora")
    Amplitude = 1
    T = 3 #segundos
    fs = 44100
        # essa senoide tem que ter taxa de amostragem de 44100 amostras por segundo
    freqPortadora = 13000 # 13000 Hz
    x1, sPortadora = meuSinal.generateSin(freqPortadora, Amplitude, T, fs)
    sinalModulado = sPortadora*yf
    print("Sinal Modulado:")
    print(sinalModulado)
    print(type(sinalModulado))

    # 5. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), 
    # de modo que todos os pontos do sinal permaneçam dentro do intervalo[-1,1].

    sinalModuladoNormalizado = normalize(sinalModulado)
    print(sinalModulado, min(sinalModuladoNormalizado), max(sinalModuladoNormalizado))





main()


    
