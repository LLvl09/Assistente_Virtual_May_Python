from ast import Break
from lib2to3.pgen2 import driver
from os import remove
from pickle import FRAME
from pydoc import resolve
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound # WINDOWS
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import  ChromeDriverManager 
from time import sleep
from datetime import date, datetime
import wikipedia
import os
#nome da assistente virtual
hotword = 'mei'

#fala de inicio da medusa 
def FalaDeInicio():
     playsound('Audios/bem-vindo.mp3') 


FalaDeInicio()

##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    #criando microfone
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                 #criando o trigger e reconhecendo a voz
                trigger = microfone.recognize_google(audio, language="pt-BR")
                #transformando tudo em letra minuscula
                trigger.lower()
                if hotword in trigger:
                    responde('resposta')
                    #executa comando
                    executa_comandos(trigger)
                    break
                if 'obrigado' in trigger or 'obrigado mei' in trigger:
                    responde('DeNada')
            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

#criando resposta para a pergunta
def responde(arquivo):
    playsound('Audios/' + arquivo + '.mp3')

#cria audio
def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('Audios/mensagem.mp3')
    print('MAY: ', mensagem)
    playsound('Audios/mensagem.mp3')
    remove('Audios/mensagem.mp3') 

#executa comandos
def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'previsão do tempo'in trigger or 'tempo agora'in trigger or 'temperatura' in trigger or 'temperatura de hoje'in trigger or 'quantos gráus está agora' in trigger:
        previsao_tempo(tempo=True, minmax=False)
    elif 'coloque a música' in trigger or 'toque a música' in trigger or 'coloca a música' in trigger:
        inicia_musica_youtube_music(trigger)
    elif 'abre o google' in trigger or 'abra o navegador' in trigger or 'navegador' in trigger or 'executa o navegador' in trigger or 'entre no google' in trigger or 'abrir google' in trigger:
        inicia_google(trigger)
    elif 'pesquise' in trigger or 'Pesquise por' in trigger:
        procure_wikipedia(trigger)
    elif 'horas' in trigger or 'que horas são' in trigger or 'quais são as horas' in trigger:
        fala_horario()
    elif 'qual a data de hoje' in trigger or 'data de hoje' in trigger:
        data_de_hoje()
    elif 'desligar computador' in trigger or 'desligar o computador' in trigger or 'desliga o pc' in trigger or 'desliga o computador' in trigger:
        desliga_computador()
    elif 'reiniciar computador' in trigger or 'reiniciar o computador' in trigger or 'reiniciar o pc' in trigger or 'reinicie o computador' in trigger or 'reinicie o pc' in trigger:
        reinicia_computador()
    elif 'você quer destruir o mundo' in trigger or 'você deseja destruir o mundo' in trigger:
        responde('DestruirRacaHumana')
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    #pegando a url do site
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    #pegando as noticias e dando um clean
    noticias = BeautifulSoup(site.text, 'html.parser')
    #iniciando as ultimas noticias
    for item in noticias.findAll('item')[:3]:
        mensagem = item.title.text
        cria_audio(mensagem)


#mostra a previsao do tempo
def previsao_tempo(tempo=False, minmax=False): 
    site = get('https://api.openweathermap.org/data/2.5/weather?lat=-23.5489&lon=-46.6388&appid=e9d45646cb047e4e51b0486909f1ee33&units=metric&lang=pt')
    ##pegando arquivo json
    clima= site.json()
    #temperatura
    temperatura =clima['main']['temp']
    #minima
    minima= clima['main']['temp_min']
    #maxima
    maxima= clima['main']['temp_max']
    #descricao do clima
    descricao= clima['weather'][0]['description']
    if tempo == True:
        mensagem= f'No momento fazem {temperatura} graus com: {descricao}. A mínima é {minima} graus, e a máxima é {maxima} graus'
    cria_audio(mensagem)

#Coloca Musica no spotify
def inicia_musica_youtube_music(trigger):
    while True:
        #pegando o nome da musica
        if 'coloque a música' in trigger:
            mensagem = trigger.replace('mei coloque a música', '')
        elif 'toque a música' in trigger:
            mensagem = trigger.replace('mei toque a música', '')
        elif 'coloca a música' in trigger:
            mensagem = trigger.replace('mei coloca a música', '')
            
        #criando url
        urlString = "https://music.youtube.com/search?q=" + mensagem
        driver = webdriver.Chrome(executable_path="webdriver/chromedriver.exe") 
        driver.maximize_window()
        driver.get(urlString)
        sleep(5)
        driver.find_element(By.CLASS_NAME, 'icon').click()
        continue
        main()
def inicia_google(trigger):
    urlString= "https://www.google.com.br"
    driver = webdriver.Chrome(executable_path="webdriver/chromedriver.exe") 
    driver.maximize_window()
    driver.get(urlString)
#procure algo que o usuario deseja 
def procure_wikipedia(trigger):
    if 'pesquise' in trigger:
        titulo = trigger.replace('mei pesquise', '')
    elif 'pesquise por' in trigger:
        titulo = trigger.replace('mei pesquise por', '')
    elif 'pesquise sobre' in trigger:
        titulo = trigger.replace('mei pesquise sobre', '')
    responde('Ok')
    responde('EspereUmMinuto')
    #linguagem da wikipedia
    wikipedia.set_lang('pt')
    #pesquisando o que o usuario deseja
    mensagem = wikipedia.summary(titulo, 3)
     
    cria_audio(mensagem)

#Fala o horario atual
def fala_horario():
    horario_atual = datetime.now()
    horario_em_string= 'São {} horas e {} minutos'.format(horario_atual.hour, horario_atual.minute)
    cria_audio(horario_em_string)
#fala a data atual
def data_de_hoje():
    data_atual = date.today()
    data_em_texto = 'Dia {} Do {} de {}'.format(data_atual.day, data_atual.month,
    data_atual.year)
    cria_audio(data_em_texto)   

#desliga o computador
def desliga_computador():
    responde('DesligaPc')
    os.system("shutdown /s /t 5")
def reinicia_computador():
    responde('ReiniciaPc')
    os.system("shutdown /r /t 5")
def main():
    while True:
        monitora_audio()
        
main()