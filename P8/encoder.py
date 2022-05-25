from suaBibSignal import signalMeu
import time
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from funcoes_LPF import filtro
from scipy.io.wavfile import write
import soundfile as sf

    # function to normalize array
def normalize(item):
    print("normalizando...")
    return (item)/(np.max(np.abs(item)))


def encoder():
    print("_____________ D E C O D E R _____________\n\n")
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
    duration = 5  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
        # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
        #use um time.sleep para a espera


    numAmostras = fs*duration#duvida
    freqDeAmostragem = fs
    modoAudio = input("Você deseja usar o meme ou gravar um aúdio? \n Digite 1 para 'meme' ou 2 para gravar agora: ")
    if modoAudio == '1':
        memePath = 'meme.wav'
        audio, samplerate = sf.read(memePath)

    
    else:
        def countdown(num_of_secs):
            while num_of_secs:
                s = num_of_secs
                min_sec_format = 'A captura de som começará em {:02d} segundos'.format(s)
                print(min_sec_format, end='\r')
                time.sleep(1)
                num_of_secs -= 1
        countdown(duration)
        #faca um print informando que a gravacao foi inicializada
        print("\Começou!")
            #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
            #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
        
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
    print("Audio gravado sem filtrar:\n")
    sd.play(y, fs)
    sd.wait()
    print("Audio filtrado ainda audível:")
    sd.play(audioFiltrado, fs)
    sd.wait()

        
   
    
    #4. Module esse sinal de áudio em AM com portadora de 13.000 Hz. 
    #   (Essa portadora deve ser uma senoide começando em zero)
    t = np.linspace(0,duration,numAmostras) 
    xf, yf = meuSinal.calcFFT(y, fs) ## Calcula o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias


    print("Gerando senoide portadora")
    Amplitude = 1
    T = 5 #segundos
    fs = 44100
        # essa senoide tem que ter taxa de amostragem de 44100 amostras por segundo
    freqPortadora = 13000 # 13000 Hz
    x1, sPortadora = meuSinal.generateSin(freqPortadora, Amplitude, T, fs)
    sinalModulado = sPortadora*audioFiltrado
    print("Sinal Modulado:")
    # print(sinalModulado)
    # print(type(sinalModulado))

    # 5. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), 
    # de modo que todos os pontos do sinal permaneçam dentro do intervalo[-1,1].

    sinalModuladoNormalizado = normalize(sinalModulado)
    #print(sinalModuladoNormalizado, min(sinalModuladoNormalizado), max(sinalModuladoNormalizado))
    print("Audio Modulado Normalizado não perfeitamente audível:")
    sd.play(sinalModuladoNormalizado, fs)
    sd.wait()

    # Exibe gráficos
    figure, axis = plt.subplots(2,2)
    axis[0][0].plot(t,audioFiltrado)
    axis[0][0].title.set_text('Audio Filtrado no tempo')
    # axis[0].set_ylim(-0.1, 0.1)
    # axis[0].set_xlim(0.5, 0.505)

    axis[0][1].plot(xf,yf)
    axis[0][1].set_xlim(0,3500)
    #axis[1].grid()
    axis[0][1].title.set_text('Audio Filtrado FFT')

    numAmostras = fs*duration
    t = np.linspace(0,duration,numAmostras) 
    #t = np.linspace(0,3,44100) 
    axis[1][0].plot(t,sinalModulado)
    axis[1][0].title.set_text('Modulado normalizado no tempo')

    xf, yf = meuSinal.calcFFT(sinalModulado, fs) ## Calcula o Fourier
    axis[1][1].plot(xf,yf)
    axis[1][1].title.set_text('Modulado normalizado FTT')
    axis[1][1].set_xlim(10500,15500)
    plt.tight_layout()
    plt.show()

    #wv.write(r"C:\Users\lorra\OneDrive\Área de Trabalho\22.1\Camada\Projeto 2\camada-fisica-da-computacao-22.1\P8\recording\gravacaoX1.wav", sinalModuladoNormalizado, fs,sampwidth=1)
    write(r"C:\Users\lorra\OneDrive\Área de Trabalho\22.1\Camada\Projeto 2\camada-fisica-da-computacao-22.1\P8\recording\gravacaoX2.wav", rate = fs, data = np.int16(sinalModuladoNormalizado))
    #criando arquivo de áudio
    sf.write('ModularizadoNormalizado.wav', sinalModuladoNormalizado, fs)

encoder()


    
