import soundfile as sf
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
from funcoes_LPF import filtro
import sounddevice as sd

def decoder():


    sd.default.samplerate =  44100 
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    audio, samplerate = sf.read('ModularizadoNormalizado.wav')

    meuSinal = signalMeu() 
    fs = 44100
    print(audio, len(audio))
    #Verifique que o sinal recebido tem a banda dentro de 10.500 Hz e 15.500 Hz (faça o Fourier).
    xf, yf = meuSinal.calcFFT(audio, samplerate) ## Calcula o Fourier do sinal audio.

    

    #Demodule o áudio enviado pelo seu colega.
    print("Gerando senoide portadora")
    Amplitude = 1
    T = 3 #segundos
    fs = 44100
        # essa senoide tem que ter taxa de amostragem de 44100 amostras por segundo
    freqPortadora = 13000 # 13000 Hz
    x1, sPortadora = meuSinal.generateSin(freqPortadora, Amplitude, T, 44100)
    sinalDemodulado = sPortadora*audio
    #signalMeu.plotFFT(meuSinal, sinalDemodulado, fs)

    #Filtre as frequências superiores a 2.500 Hz.
    cutOff = 2500 #2500 Hz
    audioFiltrado = filtro(sinalDemodulado, fs, cutOff)

    #Execute o áudio do sinal demodulado e verifique que novamente é audível. 
    print("Audio demodulado")
    sd.play(audioFiltrado, fs)
    sd.wait()


###########################
    figure, axis = plt.subplots(2,1)
    axis[0].plot(xf,yf)
    axis[0].title.set_text('Sinal demodulado FTT')
    axis[0].set_xlim(10500,15500)
    plt.tight_layout()


    xf, yf = meuSinal.calcFFT(audioFiltrado, samplerate) ## Calcula o Fourier do sinal audio.
    axis[1].plot(xf,yf)
    axis[1].title.set_text('Sinal demodulado e Filtrado FTT')
    #axis[1].set_xlim(10500,15500)
    plt.tight_layout()
    plt.show()



decoder()