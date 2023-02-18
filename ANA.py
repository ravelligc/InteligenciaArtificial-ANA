import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
from bs4 import BeautifulSoup
import requests

#Reconocimiento de texto a voz
listener = sr.Recognizer() 
engine = pyttsx3.init()
voices = engine.getProperty('voices')   #Asignar propiedades de la voz
engine.setProperty('voice', voices[3].id)   #Seleccionar voz de las instaladas en Windows
engine.runAndWait()
listener.energy_threshold = 2000        #Sensibilidad para detectar silencio


def talk(text):     #Funcion para hablar
    engine.say(text)
    engine.runAndWait()
    
talk('Hola soy Ana! tu asistente virtual')

#Detectar vocales con tilde y sustituirlas por vocales sin tilde para reconocer comandos
def normalize(v):
    vocales = ( ("á","a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    
    for a, b in vocales:
        v = v.replace(a, b).replace(a.upper(), b.upper())
    v = v.lower()
    return v

def take_command():
    try:
        with sr.Microphone() as source:     #Escuchar comando
            print('Escuchando...')
            listener.pause_threshold = 0.75
            voice = listener.listen(source)
            command = listener.recognize_google(voice,language="es-VE")
            command = command.lower()
        return command
    except: talk('No te escuché, dilo de nuevo')
    return take_command()
    

def run_ana():
    command = normalize(take_command())
    print(command)
    if 'bitcoin' in command:        #Buscar precio actual del Bitcoin
        web = 'https://www.google.com/finance/quote/BTC-USD'
        response = requests.get(web)
        valor = response.text
        soup = BeautifulSoup(valor,'html.parser')
        btc = soup.find("div",class_="YMlKec fxKbKc").text
        print('US$ '+ btc)
        talk('El precio del Bitcoin en este momento es de US$' + btc )
          
    
    elif 'busca en google' in command:  #Buscar en google lo deseado
        buscar = command.replace('busca en google','')
        talk('Buscando en Google'+ buscar)
        pywhatkit.search(buscar)

    elif 'reproduce' in command:        #Reproducir cancion en YouTube
        song = command.replace('reproduce', '')
        talk('Reproduciendo' + song)
        pywhatkit.playonyt(song)
    
    elif 'hora' in command:     #Indicar la hora
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Son las ' + time)
        print(time)
    
    elif 'dia' in command:      #Indicar que dia es hoy
        dia = datetime.datetime.today().weekday() + 1
	    
        dia_dict = {1: 'Lunes', 2: 'Martes',
				3: 'Miercoles', 4: 'Jueves',
				5: 'Viernes', 6: 'Sabado',
				7: 'Domingo'}
        
        if dia in dia_dict.keys():
            dia_semana = dia_dict[dia]
            print(dia_semana)
            talk("Hoy es " + dia_semana)
    
    elif 'hola' in command:
        talk('Hola! en qué te puedo ayudar? ')
    
    elif 'como estas' in command:
        talk('me encuentro excelente, gracias por preguntar!')
    
    elif 'chao' in command:
        talk('Adiós! estimado individuo')
        exit()
    
    else:
        talk('Disculpa, no te entendí')
        return
        

while True:
    run_ana()