# Carga de librerías del modelo
import json
import pyaudio # Librería para manejar el audio del micrófono
import vosk # Modelo de reconocimiento de voz
import pyttsx3 # Motor de síntesis de voz
import re # Librería para manejar expresiones regulares

from datetime import datetime # Importación de la clase datetime para obtener la hora actual
from functions.os_ops import(
    openCalculator,
    openCursor
    )  # Importación de la función para abrir la calculadora desde un módulo personalizado
from functions.online_ops import(
    searchOnGoogle,
    playOnYouTube,
    sendWhatsAppMessage,
    getRandomJoke
    ) # Importación de la función para realizar búsquedas en Internet desde un módulo personalizado

# Variables
USERNAME = 'Jeff' # Nombre del usuario para personalizar las respuestas
BOTNAME = 'Jarvis' # Nombre del asistente de voz para personalizar las respuestas
state = {
    'inactivity': 0, # Variable para controlar el tiempo de inactividad
    'greet': False, # Variable para controlar si se ha dado el saludo inicial
    'dialog': False # Variable para controlar si se ha iniciado un diálogo
}
inactivityMax = 3 # Tiempo máximo de inactividad antes de finalizar el diálogo

# Motor de sintesis de voz
engine = pyttsx3.init('sapi5') # Inicialización del motor de síntesis de voz
engine.setProperty('rate', 120) # Configuración de la velocidad de habla
engine.setProperty('voice', 'spanish') # Configuración del idioma de la voz

# Carga del modelo de Vosk para el reconocimiento de voz en español, asegurándose de que el modelo esté ubicado en la carpeta 'model' del proyecto
model = vosk.Model('model')

# Configuración del micrófono utilizando PyAudio para capturar el audio de entrada del usuario
pa = pyaudio.PyAudio() # Inicialización de PyAudio
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096) # Configuración del micrófono

def speak(text):
    engine.say(text) # Mensaje de bienvenida
    engine.runAndWait() # Ejecución del mensaje de bienvenida

def listen():
    """Función para escuchar y reconocer voz utilizando el modelo de Vosk."""
    rec = vosk.KaldiRecognizer(model, 16000) # Frecuencia de muestreo del micrófono
    
    stream.start_stream() # Apertura del flujo de entrada de audio
    
    print("Estoy escuchando...") # Mensaje de inicio de escucha
    
    while True: # Bucle para escuchar continuamente hasta que se detecte el silencio
        data = stream.read(4096, exception_on_overflow=False) # Lectura de datos del micrófono y manejo de posibles desbordamientos
        if rec.AcceptWaveform(data): # Procesamiento de los datos de audio
            result = rec.Result() # Obtención del resultado del reconocimiento
            stream.stop_stream() # Detención del flujo de entrada de audio
            return result # Retorno del resultado del reconocimiento hasta el silencio

def greet_user():
    global greet
    
    hour = datetime.now().hour # Obtención de la hora actual
    if 0 <= hour < 12:
        speak(f'Buenos días, {USERNAME}. Soy {BOTNAME}, tu asistente de voz. ¿En qué puedo ayudarte?') # Saludo matutino
    elif 12 <= hour < 18:
        speak(f'Buenas tardes, {USERNAME}. Soy {BOTNAME}, tu asistente de voz. ¿En qué puedo ayudarte?') # Saludo vespertino
    else:
        speak(f'Buenas noches, {USERNAME}. Soy {BOTNAME}, tu asistente de voz. ¿En qué puedo ayudarte?') # Saludo nocturno
    # speak(f'Soy {BOTNAME}, tu asistente de voz. ¿En qué puedo ayudarte?') # Mensaje de bienvenida
    state['greet'] = True # Establecimiento de la variable de saludo a verdadero para indicar que se ha dado el saludo inicial

def listenToText():
    """Función para convertir el resultado de la escucha en texto."""
    resultado = listen() # Llamada a la función de escucha
    try:
        estructura = json.loads(resultado) # Conversión del resultado a un diccionario de Python
        return estructura.get('text', '') # Extracción del texto reconocido
    except:
        return resultado # Retorno del resultado original en caso de error en la conversión

def byeBye():
    hour = datetime.now().hour # Obtención de la hora actual
    if hour >= 21 or hour < 6:
        speak(f'Buenas noches, {USERNAME}. Fue un placer ayudarte. ¡Hasta luego!') # Despedida nocturna
    elif 6 <= hour < 12:
        speak(f'Buenos días, {USERNAME}. Fue un placer ayudarte. ¡Hasta luego!') # Despedida matutina
    else:
        speak(f'Buenas tardes, {USERNAME}. Fue un placer ayudarte. ¡Hasta luego!') # Despedida vespertina
    print(hour) # Impresión de la hora actual para depuración
    state['greet'] = False # Establecimiento de la variable de saludo a falso para indicar que se ha dado la despedida
    state['dialog'] = False # Establecimiento de la variable de diálogo a falso para indicar que se ha finalizado el diálogo

# Validar si contiene alguna de las palabras
def isContain(textEntrada, seeds, debug=False):
    """Función para verificar si el texto de entrada contiene alguna de las palabras clave."""
    if not textEntrada or not seeds:
        if debug:
            print(f'La función isContain: No contiene textEntrada o seeds',
                f'textEntrada: {textEntrada}, seeds: {seeds}') # Mensaje de depuración en caso de falta de texto de entrada o palabras clave
            return False # Retorno de falso si no se proporciona texto de entrada o palabras clave
    
    textoLimpio = str(textEntrada).strip() # Eliminación de espacios en blanco al inicio y al final del texto de entrada
    textoSuperLimpio = re.sub(r'\s+', ' ', textoLimpio) # Reemplazo de múltiples espacios por un solo espacio
    minSuperTexto = textoSuperLimpio.lower() # Conversión del texto a minúsculas para comparación
    
    if debug:
        print(f'La función isContain: Texto limpio: {textoLimpio}, Texto super limpio: {textoSuperLimpio}, Texto en minúsculas: {minSuperTexto}') # Mensaje de depuración con el texto procesado1
        print(f'Palabras clave: {seeds}') # Mensaje de depuración con las palabras clave
    
    # Validación de coincidencias
    for seed in seeds:
        if seed:
            seedLimpio = str(seed).strip().lower() # Eliminación de espacios en blanco al inicio y al final de la palabra clave
            
            # Buscar o filtrar del seed limpio en el texto super limpio
            encontrado = seedLimpio in minSuperTexto # Verificación de si la palabra clave está presente en el texto procesado
            if debug:
                print(f'Función isContain: El seed limpio {seedLimpio} Se ha encontrado? {encontrado}') # Mensaje de depuración con el resultado de la búsqueda de la palabra clave
            
            if encontrado:
                return True # Retorno de verdadero si se encuentra la palabra clave en el texto de entrada
    if debug:
        print(f'No se ha encontrado ninguna conincidencia')
    
    return False # Retorno de falso si no se encuentra ninguna palabra clave en el texto de entrada

def inDialog():
    stringEntrada = listenToText() # Llamada a la función de escucha para obtener el texto de entrada
    if isContain(stringEntrada, ['hola', 'jarvis', 'hola jarvis', 'hey jarvis','ok jarvis', 'oye jarvis']): # True para el DEBUG
        # Verificación de si el texto de entrada contiene alguna de las palabras clave para iniciar el diálogo
        state['dialog'] = True # Establecimiento de la variable de diálogo a verdadero para indicar que se ha iniciado un diálogo

def outDialog():
    speak(f'Quiere que le ayude con algo más, {USERNAME}?') # Pregunta de seguimiento antes de finalizar el diálogo por inactividad
    stringEntrada = listenToText() # Llamada a la función de escucha para obtener el texto de entrada y permitir al usuario responder a la pregunta de seguimiento
    if isContain(stringEntrada, ['sí', 'si', 'claro', 'por supuesto', 'efectivamente', 'sí por favor']): # Verificación de si el texto de entrada contiene alguna de las palabras clave para continuar el diálogo después de la pregunta de seguimiento
        speak(f'¿En qué puedo ayudarte, {USERNAME}?') # Mensaje de continuación del diálogo después de la pregunta de seguimiento
        state['dialog'] = True # Establecimiento de la variable de diálogo a verdadero para indicar que se ha continuado el diálogo después de la pregunta de seguimiento
        state['inactivity'] = 0 # Reinicio del contador de inactividad después de la pregunta de seguimiento
    else:
        speak(f'Encantado de haberte ayudado, {USERNAME}. Si necesitas algo más, no dudes en llamarme. ¡Hasta luego!') # Mensaje de despedida por inactividad
        byeBye() # Llamada a la función de despedida

def actions(stringEntrada):
    """Función para gestionar las acciones del asistente de voz en función del texto de entrada del usuario."""
    if isContain(stringEntrada, ['test', 'prueba', 'demo', 'ejemplo']):
        speak(f'Esto es una prueba de funcionamiento')
    elif isContain(stringEntrada, ['calculadora', 'abre calculadora', 'abre la calculadora', 'inicia calculadora', 'inicia la calculadora']):
        speak(f'Abriendo la calculadora')
        openCalculator() # Llamada a la función para abrir la calculadora
    elif isContain(stringEntrada, ['cursor', 'abre cursor', 'abre el cursor', 'inicia cursor', 'inicia el cursor']):
        speak(f'Abriendo Cursor')
        openCursor() # Llamada a la función para abrir Cursor
    elif isContain(stringEntrada, ['busca en google', 'busca en internet', 'haz una búsqueda en google', 'haz una búsqueda en internet']):
        speak('Que tengo que buscar en Google?')
        query = listenToText()
        if query:
            speak(f'Buscando {query} en Google')
            searchOnGoogle(query) # Llamada a la función para realizar una búsqueda en Google con el texto de entrada del usuario como consulta
        else:
            speak('No he entendido tu consulta para Google.')
    elif isContain(stringEntrada, ['reproduce en youtube', 'busca en youtube', 'haz una búsqueda en youtube', 'youtube', 'you tub', 'yu', 'tub']):
        speak('Que quieres reproducir en YouTube?')
        video = listenToText()
        if video:
            speak(f'Reproduciendo {video} en YouTube')
            playOnYouTube(video) # Llamada a la función para reproducir un video en YouTube con el texto de entrada del usuario como consulta
        else:
            speak('No he entendido tu consulta para YouTube.')
    elif isContain(stringEntrada, ['envía un mensaje', 'envía un whatsapp', 'manda un mensaje', 'manda un whatsapp', 'envía un mensaje de whatsapp', 'manda un mensaje de whatsapp']):
        speak('¿A que número quieres enviar?')
        number = listenToText()
        speak('¿Qué mensaje quieres enviar?')
        message = listenToText()
        if number and message:
            speak(f'Enviando mensaje {message} al número {number} por WhatsApp')
            sendWhatsAppMessage(number, message) # Llamada a la función para enviar un mensaje de WhatsApp con el número de teléfono y el mensaje obtenidos del texto de entrada del usuario
        else:
            speak('No he entendido tu consulta para WhatsApp.')
    elif isContain(stringEntrada, ['cuéntame un chiste', 'dime un chiste', 'quiero escuchar un chiste', 'chiste'], True):
        joke = getRandomJoke()
        speak('Te cuento un chiste')
        speak(joke['joke'])
        if joke['answer']:
            speak(joke['answer'])
        speak('ja ja ja ja')
    else:
        speak(f'Lo siento, no he podido procesar tu petición.')

# Llamado principal
try:
    while True:
        # Chek para saber si estamos dentro del dialogo
        if state['dialog']:
            if state['inactivity'] == 0 and not state['greet']: greet_user() # Llamada a la función de saludo al usuario
            stringEntrada = listenToText() # Llamada a la función de escucha para obtener el texto de entrada
            
            if isContain(stringEntrada, ['adiós', 'hasta luego', 'nos vemos', 'gracias jarvis' + BOTNAME]):
                # Verificación de si el texto de entrada contiene alguna de las palabras clave para finalizar el diálogo
                # print('Dialogo finalizado por el usuario') # Mensaje de finalización del diálogo por parte del usuario
                byeBye() # Llamada a la función de despedida
                continue
            else:
                # Sequencia de despedida por inactividad
                if state['inactivity'] < inactivityMax and stringEntrada == '': # Verificación de si el texto de entrada está vacío y el contador de inactividad es menor que el máximo permitido
                    speak(f'¿Necesitas algo más, {USERNAME}?') # Pregunta de seguimiento por inactividad
                    state['inactivity'] += 1 # Incremento del contador de inactividad
                
                elif stringEntrada != 0: # Verificación de si se ha obtenido un texto de entrada válido para evitar finalizar el diálogo por inactividad en caso de errores en la escucha
                    print(f'En breve gestiono tu solicitud') # Mensaje de gestión de la solicitud del usuario
                    actions(stringEntrada) # Llamada a la función de gestión de acciones con el texto de entrada del usuario
                    state['inactivity'] = 0 # Reinicio del contador de inactividad después de gestionar la solicitud del usuario
                
                else:
                    outDialog() # Llamada a la función para finalizar el diálogo por inactividad
                    state['inactivity'] = 0 # Reinicio del contador de inactividad
                
            print(f"Fin del ciclo, {state['inactivity']}") # Mensaje de finalización del ciclo de escucha
                
        else:
            print('In Standby...') # Mensaje de espera
            inDialog() # Llamada a la función para verificar si se ha iniciado un diálogo

except KeyboardInterrupt:
    print('Programa finalizado por el usuario') # Mensaje de finalización del programa por parte del usuario
    byeBye() # Llamada a la función de despedida
    stream.close() # Cierre del flujo de entrada de audio
    pa.terminate() # Terminación de PyAudio