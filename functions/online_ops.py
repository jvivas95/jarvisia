import pywhatkit as kit # Librería para realizar búsquedas en YouTube y otras funciones relacionadas con la web
import requests # Librería para realizar solicitudes HTTP, utilizada para obtener chistes aleatorios de una API

# Función para buscar en Google
def searchOnGoogle(query):
    """Función para realizar una búsqueda en Google."""
    kit.search(query)

def playOnYouTube(query):
    """Función para reproducir un video en YouTube."""
    kit.playonyt(query)

def sendWhatsAppMessage(phone_number, message):
    """Función para enviar un mensaje de WhatsApp a un número específico."""
    kit.sendwhatmsg_instantly(f'+34{phone_number}', message)

def getRandomJoke():
    """Función para obtener un chiste aleatorio."""
    response = {}
    headers = {'Accept': 'application/json'}
    res = requests.get('https://v2.jokeapi.dev/joke/Any?lang=es', headers=headers).json()
    if res['type'] == 'single':
        response['joke'] = res['joke']
        response['answer'] = ''
    else:
        response['joke'] = res['setup']
        response['answer'] = res['delivery']
    return response