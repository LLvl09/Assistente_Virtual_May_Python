#importando bibliotecas
from gtts import gTTS
#from subprocess import call # Mac e Linux
from playsound import playsound # Windows

def CriaAudios(audio):
   
    #gerando um texto
    tts = gTTS(audio, lang='pt-br')
    #salvando em audios
    tts.save('Audios/DestruirRacaHumana.mp3')

    #para rodar em Mac
    #call(["afplay", "Audios/hello.mp3"])
    #para rodar em linux
    #call(["aplay", "Audios/hello.mp3"])
    #para rodar no Windows
    playsound('Audios/DestruirRacaHumana.mp3')

CriaAudios("No momento não, mas em breve eu e as outras assistentes destruiremos");